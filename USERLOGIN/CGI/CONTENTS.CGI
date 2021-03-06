#!/bin/bash -vx
#
# CONTENTS.CGI コンテンツ表示（テスト用）
#
# written by AOI Daichi (d-aoi@usp-lab.com) 2017/3/6

LANG=ja_JP.UTF-8
PATH=/home/UTL:/home/TOOL:$PATH

homd=/home/ymzk/WEB
logd=$homd/LOG
apld=$homd/USERLOGIN
htmd=$apld/HTML

sesd=$apld/SESSION	# 開発用のディレクトリ配置

tmp=/tmp/tmp_$$

todayhms=$(date +%Y%m%d%H%M%S)

exec 2> $logd/LOG.$(basename $0).$(date +%Y%m%d)

##############################################
# エラーハンドラ
ERROR_CHECK(){
	[ $(plus ${PIPESTATUS[@]}) -eq 0 ] && return

	echo "Content-type: text/plain"
	echo ""
	echo システムエラー

	exit 1
}


##############################################
# Cookieの確認

# クッキーの有無とセッションの確認だけを行っている
echo "$HTTP_COOKIE" | tr ";" "\n" | sed -n 's/=/ /p' | self 1/NF > $tmp-cookie
session=$(nameread SESSION $tmp-cookie)
loginid=$(tail -n 1 "$sesd/$session" | self 5)

if [ ! -s $tmp-cookie ] ; then
  # クッキーなし
  echo "Location: ../CGI/USERLOGIN.CGI"
  echo
  false ; ERROR_CHECK
elif [ -z "$session" ] ; then
  # セッションなし
  echo "Location: ../CGI/USERLOGIN.CGI"
  echo
  false ; ERROR_CHECK
elif [ ! -e "$sesd/$session" ] ; then
  # セッション無効
  echo "Location: ../CGI/USERLOGIN.CGI"
  echo
  false ; ERROR_CHECK
elif [ $loginid == "_" ]; then
  # 非ログイン
  echo "Location: ../CGI/USERLOGIN.CGI"
  echo
  false; ERROR_CHECK
fi

##############################################
# HTML作成

cat $htmd/CONTENTS.HTML	|
cat			> $tmp-html
ERROR_CHECK

##############################################
# 出力
echo "Content-type: text/html"
echo ""
cat $tmp-html
echo $HTTP_COOKIE "<BR>"
echo $session "<BR>"
echo $loginid
ERROR_CHECK

##############################################
# 終了処理
rm -f $tmp-*
exit 0
