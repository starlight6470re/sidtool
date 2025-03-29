# dokisidpy
#### このツールを利用するには、FFmpegをインストールし、必要に応じてパスを通す必要があります。
### sidtool.py
DokiDokiLiveのsidから日付を計算してm3u8のURLを表示した後、連番の.tsのダウンロードとffmpegによるmp4への結合を一括でできるようにしたpythonスクリプト。  
何らかの要因により途中でtsの番号が飛び、ダウンロード完了を誤検知する場合があります。どうしてもうまく行かないときは手動でtsの抜けた分をダウンロードした上で、sidtoolをimportして必要部分の関数のみを利用するpythonスクリプトを組むなどしてもらえると良いと思います。time.sleep(25行目)は念の為大きめに設定すると良いかもしれません。
### GUI_test.py
Fletで作ったsidtoolの版です。上記の「必要部分の関数のみ」を各ボタンを押すことで実行可能にしてあります。pipでfletを入れて、 flet run GUI_test.py で動くと思います。ReleaseにWindows向けのビルドがあります
