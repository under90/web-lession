#!/bin/bash -vx
#
# USERLOGIN.CGI ログイン
#
# written by AOI Daichi (d-aoi@usp-lab.com) 2017/3/6

LANG=ja_JP.UTF-8
PATH=/home/UTL:/home/TOOL:$PATH

homd=/home/aoi/WEB
logd=$homd/LOG
apld=$homd/USERLOGIN
htmd=$apld/HTML

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
# HTML作成

cat $htmd/USERLOGIN.HTML	|
cat				> $tmp-html
ERROR_CHECK

##############################################
# 出力
echo "Content-type: text/html"
echo ""
cat $tmp-html
ERROR_CHECK

##############################################
# 終了処理
rm -f $tmp-*
exit 0
