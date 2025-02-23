# numtool/sidtool
## このツールを使用したことによる一切の責任を負いません。
### numtool.py
10桁の数字を入力すると、後ろから8桁を利用してUNIX時間に基づく日付を返すだけのPythonスクリプト<br>
### sidtool.py
numtoolを応用し、某ライブ配信サイトのsidから日付を計算してm3u8のURLを表示した後、連番の.tsのダウンロードとffmpegによるmp4への結合を一括でできるようにしたpythonスクリプト。sidtool.shは、当初同等の機能をbashで実現しようとしたときに書いたもので、参考用に残してありますが、通常はpython版を使ってください。<br>
何らかの要因により途中でtsの番号が飛び、ダウンロード完了を誤検知する場合があります。どうしてもうまく行かないときは手動でtsの抜けた分をダウンロードした上で、sidtoolをimportして必要部分の関数のみを利用するpythonスクリプトを組むなどしてもらえると良いと思います。アクセス過多で一時BANされている可能性もあるため、bashのsleep(37行目)やpythonのtime.sleep(25行目)は念の為大きめに設定すると良いかもしれません。
