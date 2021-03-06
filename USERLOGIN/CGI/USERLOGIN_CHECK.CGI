#!/bin/bash -vx
#
# USERLOGIN_CHECK.CGI ログイン情報の確認
#
# written by AOI Daichi (d-aoi@usp-lab.com) 2017/3/6

LANG=ja_JP.UTF-8
PATH=/home/UTL:/home/TOOL:$PATH

homd=/home/ymzk/WEB
logd=$homd/LOG
apld=$homd/USERLOGIN
htmd=$apld/HTML

sesd=$apld/SESSION	# 開発用のディレクトリ配置
lv3d=$apld/DATA/LV3	# 開発用のディレクトリ配置

tmp=/tmp/tmp_$$

todayhms=$(date +%Y%m%d%H%M%S)

exec 2> $logd/LOG.$(basename $0).$(date +%Y%m%d)

##############################################
# エラーハンドラ
ERROR_CHECK(){
	[ $(plus ${PIPESTATUS[@]}) -eq 0 ] && return

	echo "Content-type: text/plain"
	echo ""
	echo "システムエラー CHECK"

	exit 1
}

##############################################
# POSTデータの受け取り
if [ ! -z "$CONTENT_LENGTH" ] ; then
	dd bs=$CONTENT_LENGTH   |
	cgi-name -n_ -s_ -e_	|
	cat			> $tmp-name
	ERROR_CHECK

else
	# POSTデータがなければシステムエラーとする
	false
	ERROR_CHECK
fi

##############################################
# 入力値チェック
cat << FIN > $tmp-check
USERID x12
PASSWORD x40
FIN
ERROR_CHECK

# check_attr_name は入力値チェックエラーの場合1を返すが、これをエラーとはしない
check_attr_name $tmp-check $tmp-name > $tmp-result
if [ $? -ne 0 -a $? -ne 1 ] ; then
	false
	ERROR_CHECK
fi

##############################################
# 登録チェック

# 単純に、ユーザーの登録データと一致しているかどうかを見ているだけ
# 暗号化していないので、実装時には暗号化したデータで行う必要がある。

cat $tmp-name			|
self 2				|
yarr				|
# 1:ユーザー名 2:パスワード
join0 key=1/2 $lv3d/USER -	|
cat				> $tmp-touroku-result
ERROR_CHECK

##############################################
# 画面遷移

if [ -s $tmp-result ] ; then
	# 入力チェックエラー時は再びログイン画面へ
	echo "Location: ../CGI/USERLOGIN.CGI"
	echo
	# 上でページが遷移しないのは何らかのエラー
	false ; ERROR_CHECK

elif [ ! -s $tmp-touroku-result ] ; then
	# 登録チェックエラー時も再びログイン画面へ
	echo "Location: ../CGI/USERLOGIN.CGI"
	echo
	# 上でページが遷移しないのは何らかのエラー
	false ; ERROR_CHECK

else
	# 入力チェックOK時

	############################
	# セッション発行

	# セッションキー作成（作り方は一例）
	session=$(echo $todayhms.USP.$HOSTNAME.$$ | md5sum | self 1)
	ERROR_CHECK
	
	# セッションを記録
	touch $sesd/$session
	ERROR_CHECK
	
	# ユーザー名の取得
	userid=$(nameread USERID $tmp-name)
	ERROR_CHECK
	
	# 有効期限（30分後に設定）
	expires=$(date -uR -d "$(date -R --date='+30min')")
	ERROR_CHECK
	
	echo $session $todayhms $HOSTNAME $(basename $0) $userid _ >> $sesd/$session
	# 1:セッションキー 2:年月日時分秒 3:サーバ名 4:CGI名 5:ユーザーID 6:モード
	ERROR_CHECK
	
	############################
	# Cookieの作成
	
	# 下記のCookieに含める項目は一例
	echo "Set-Cookie: SESSION=$session; expires=$expires;" > $tmp-cookie
	ERROR_CHECK

fi

##############################################
# HTML作成

cat $htmd/USERLOGIN_CHECK_OK.HTML	|
cat					> $tmp-html
ERROR_CHECK

##############################################
# 出力
echo "Content-type: text/html"
cat $tmp-cookie
echo ""
cat $tmp-html
ERROR_CHECK

cat $tmp-cookie > /tmp/ymzktemp
##############################################
# 終了処理
rm -f $tmp-*
exit 0
