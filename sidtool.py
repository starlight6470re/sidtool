import datetime
import os
import sys
import urllib.request
import time
import subprocess
import shutil

def calculate_date_from_sid(sid):
    unix_time_str = sid[2:] #後ろ8桁を日付計算に利用
    unix_time = int(unix_time_str)*100
    date = datetime.datetime.fromtimestamp(unix_time)
    return date.year, date.month, date.day
def ts_download():
    i=0
    folder_name = os.getcwd()+"/"+str(time.time()*1000)
    os.mkdir(folder_name)
    os.chdir(folder_name)
    url = "https://rescdn.dokidokilive.com/doki/record_m3u8/"+str(year)+"/"+str(month)+"/"+str(day)+"/"+str(sid)+"/"+str(sid)+"-"
    while True:
        try:
            url_all = url + str(i).zfill(5) + ".ts"
            urllib.request.urlretrieve(url_all, str(sid) + "-" + str(i).zfill(5) + ".ts")
            print ("ダウンロード中: "+ str(i))
            time.sleep(3)
            i += 1
        except urllib.error.URLError as e:
            print("ダウンロードが完了しました。")
            return folder_name
            break
def makefilelist(folder_name):
    tsfiles = sorted(os.listdir(folder_name))
    for tsi in range(len(tsfiles)):
        tsfiles[tsi] = "file " + tsfiles[tsi]
        with open("test.txt","w") as tsf:
            tsf.write('\n'.join(tsfiles))
    merger()
def merger():
    try:
        subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "test.txt", "-c:v", "copy", "-c:a", "copy", sid + ".mp4"], check=True)
        shutil.move(sid + ".mp4", "../"+sid+".mp4")
    except subprocess.CalledProcessError as e:
        print (e)
def cleanup(folder_name):
    shutil.rmtree(folder_name)

if __name__ == "__main__":
    while True:
        while True:
            try:
                sid = str(input("SIDを入力してください: "))
                tmp = int(sid)
                break
            except ValueError:
                print("数値以外が入力されています。")
        if len(sid)<10:
            print("10桁未満です。IDとSIDを間違えていませんか？") 
        else:
            break
    year, month, day = calculate_date_from_sid(sid)
    print ("URL: https://rescdn.dokidokilive.com/doki/record_m3u8/"+str(year)+"/"+str(month)+"/"+str(day)+"/"+str(sid)+"/"+str(sid)+".m3u8")
    print ("予備用: https://rescdn.dokidokilive.com/doki/record_m3u8/"+str(year)+"/"+str(month)+"/"+str(day+1)+"/"+str(sid)+"/"+str(sid)+".m3u8")

    ts_if=input("このままダウンロードを試みるにはyを入力してください。それ以外の場合は、Enterで終了します。")
    if ts_if == "y":
        print ("tsファイルを一時フォルダにダウンロードします。")
        folder_name = ts_download()
    merge_if=input("tsファイルをmp4に変換しますか？しない場合は、Enterで終了します。")
    if merge_if == "y":
        print ("ffmpeg")
        makefilelist(folder_name)
    print ("クリーンアップを実行します。")
    cleanup(folder_name)
    print ("完了：スクリプトのあるフォルダに{sid}.mp4の形式で保存されました。")
