import flet as ft
import datetime
import os
import sys
import urllib.request
import time
import subprocess
import shutil

cooltime = 3
################################fletによるGUIの定義###############################
def main(page: ft.Page):
    page.title = "sidtool(GUI)"
    page.window_width = 720
    page.windows_height = 580
    page.theme = ft.Theme(color_scheme_seed="blue")

    dl_stop_flag = 0
    ################################sidtool(CLI)からの移植###############################
    def calculate_date_from_sid(arg1):
        sid = sidbox.value
        unix_time_str = sid[2:] #後ろ8桁を日付計算に利用
        unix_time = int(unix_time_str)*100
        date = datetime.datetime.fromtimestamp(unix_time)
        url1.value = "https://rescdn.dokidokilive.com/doki/record_m3u8/"+str(date.year)+"/"+str(date.month)+"/"+str(date.day)+"/"+str(sid)+"/"+str(sid)+".m3u8"
        url2.value = "https://rescdn.dokidokilive.com/doki/record_m3u8/"+str(date.year)+"/"+str(date.month)+"/"+str(date.day+1)+"/"+str(sid)+"/"+str(sid)+".m3u8"
        page.update()

    def ts_download(arg2):
        i=0
        nonlocal dl_stop_flag
        dl_stop_flag = 0
        folder_name = "sidtool_temp"
        try:
            os.mkdir("sidtool_temp")
        except FileExistsError:
            dl_progress.value = "フォルダ「sidtool_temp」が存在します。クリーンアップを実行してください"
            page.update()
            return
        sid = sidbox.value
        unix_time_str = sid[2:] #後ろ8桁を日付計算に利用
        unix_time = int(unix_time_str)*100
        date = datetime.datetime.fromtimestamp(unix_time)
        url = "https://rescdn.dokidokilive.com/doki/record_m3u8/"+str(date.year)+"/"+str(date.month)+"/"+str(date.day)+"/"+str(sid)+"/"+str(sid)+"-"
        while dl_stop_flag == 0:
            try:
                url_all = url + str(i).zfill(5) + ".ts"
                urllib.request.urlretrieve(url_all, "sidtool/"+str(sid) + "-" + str(i).zfill(5) + ".ts")
                dl_progress.value = "ダウンロード中: "+ str(i+1)+" 個目 (クールタイム："+str(cooltime)+"秒)"
                page.update()
                time.sleep(cooltime)
                i += 1
            except urllib.error.URLError as e:
                dl_progress.value = "ダウンロードが完了しました。"
                page.update()
                break
    def dl_stop(arg21):
        nonlocal dl_stop_flag
        dl_stop_flag = 1
        dl_progress.value = "ダウンロードが開始されると、ここに進捗が表示されます"
        page.update()

    def makefilelist(arg3):
        tsfiles = sorted(os.listdir("sidtool_temp"))
        for tsi in range(len(tsfiles)):
            tsfiles[tsi] = "file " + tsfiles[tsi]
            with open("sidtool_temp/temp.txt","w") as tsf:
                tsf.write('\n'.join(tsfiles))

    def merger(arg4):
        try:
            sid = sidbox.value
            subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "sidtool_temp/temp.txt", "-c:v", "copy", "-c:a", "copy", sid + ".mp4"], check=True)
        except subprocess.CalledProcessError as e:
            print (e)

    def cleanup(arg5):
        shutil.rmtree("sidtool_temp")
        dl_progress.value = "クリーンアップ完了"
        page.update()
    ####################################################################################

    page.add(
        ft.Text("sidtoolへようこそ！"),
        sidbox := ft.TextField(label="sid", hint_text="sidを入力してください", input_filter=ft.NumbersOnlyInputFilter(), max_length=10),
        url1 := ft.TextField(label="URL1", hint_text="ボタンを押すと、ここにURLが表示されます", read_only=True),
        url2 := ft.TextField(label="URL2", hint_text="ボタンを押すと、ここに予備用のURLが表示されます", read_only=True),
        dl_progress := ft.Text("ダウンロードが開始されると、ここに進捗が表示されます"),
    )
    page.add(
            ft.ElevatedButton("URLの表示", on_click=calculate_date_from_sid),
            ft.ElevatedButton("ダウンロード", on_click=ts_download), 
            ft.ElevatedButton("ダウンロード中止", on_click=dl_stop), 
            ft.ElevatedButton("結合準備", on_click=makefilelist),
            ft.ElevatedButton("結合処理", on_click=merger), 
            ft.ElevatedButton("クリーンアップ", on_click=cleanup),  
    )

ft.app(target=main)