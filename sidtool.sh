#!/bin/bash
function help(){
	echo "sidtool v1.0"
	echo "============"
	echo "使い方"
	echo "sidtool.sh	| ヘルプ(この画面)を表示する"
	echo "sidtool.sh {sid}	| sidに対応するURLを表示する"
}

function url_calculation(){
	date_unix=$(($(echo ${1} | cut -c3- -)*100))
	ym=$(date --date @$date_unix +"%Y/%-m/")
	day=$(date --date @$date_unix +"%-d")
	URL1="https://rescdn.dokidokilive.com/doki/record_m3u8/"$ym$day"/"${1}"/"${1}
	URL2="https://rescdn.dokidokilive.com/doki/record_m3u8/"$ym$(($day+1))"/"${1}"/"${1}
	echo -e "URL1:	"$URL1".m3u8\nURL2:	"$URL2".m3u8\n"
}

function downloader_boot(){
	type "ffmpeg" > /dev/null 2>&1 || (echo "ffmpegをインストールしてください"; read -p "インストール後、Enterで続けます: "; downloader_boot)
	type "wget" > /dev/null 2>&1 || (echo "wgetをインストールしてください"; read -p "インストール後、Enterで続けます: "; downloader_boot)
	read -p "ダウンロード先にする新しいディレクトリを作成するパスを入力してください: " dlpath
	mkdir -p $dlpath
	if [ -n "$(ls -A $dlpath)" ]; then
		echo "すでにファイルが存在するディレクトリにダウンロードすることはできません。"
		downloader_boot
 	fi
	cd $dlpath
	j="True"
	downloader $URL1
}

function downloader(){
for i in $(seq -f "%05g" 0 99999); do
		printf "\r${i}をダウンロード中"
		wget -q ${1}"-"${i}".ts" #cURLだとNoSuchKeyのxmlもDLする
		sleep 1
		if [ $? -ne 0 ]; then
			echo $j
			if [ j == "True" ]; then
				j="False"
				echo "URL2でのダウンロード"
				downloader $URL2
			else
				echo "ファイルのダウンロードが完了しました"
				read -p "このまま動画をmp4に変換しますか? (y/N): " yn
				case "$yn" in
					[yY]*) merger;;
					*) exit;;
				esac
			fi
		fi
	done
}

function merger(){
	find -name "*.ts" > temp.txt
	sed -i -e "s;./;file ';g" temp.txt
	sed -i -e "s;.ts;.ts';g" temp.txt
	sort temp.txt > temp_sort.txt
	ffmpeg -f concat -safe 0 -i temp_sort.txt -c:v copy -c:a copy ${sid}.mp4
	echo $dlpath"/"$sid."mp4 に保存しました"
	read -p "ts等、mp4以外のファイルをクリーンアップしますか? (Y/n): " cleanyn
	case "$cleanyn" in
		[nN]*) exit;;
		*) cleanup
	esac
	exit
}

function cleanup(){
	rm -f *.ts && rm temp.txt && rm temp_sort.txt
	echo "クリーンアップ完了"
}

if [[ ${1} =~ ^[0-9]+$ ]] && [[ ${#1} -eq 10 ]]; then
	url_calculation "${1}"
	read -p "このまま動画のダウンロードを試みますか? (y/N): " yn
	case "$yn" in
	  [yY]*) sid=${1}; downloader_boot;;
	esac
elif [[ ${1} =~ ^[0-9]+$ ]]; then
	echo "桁数が一致しません。sidは10桁です。idと間違えていませんか?"
elif [[ ${1} != "" ]]; then
	echo "引数のsidは数値のみで入力して下さい"
else
	help
fi
