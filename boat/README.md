# boat_data

## 導入方法
まずpythonが入っている前提で進めていきます。

1. 以下のコマンドを入力して、モジュールをインストールしてください
 - `pip3 install beautifulsoup4`
 - `pip3 install lxml`
 - `pip3 install openpyxl`
 - `pip3 install requests`

2. input_boat_info.jsonに追加したいデータを指定します。

ex) １日分を追加したい時
```json
{
  "1":{
    "excelFile": "2020年6月7日",
    "txtFile": "K200607",
    "urlList": [
      //　この中には指定した日の大会ごとのurlを九州地区から順番に貼り付けます。
      "https://www.boatrace.jp/owpc/pc/race/raceindex?jcd=24&hd=20200607",
      "https://www.boatrace.jp/owpc/pc/race/raceindex?jcd=22&hd=20200607",
      "https://www.boatrace.jp/owpc/pc/race/raceindex?jcd=21&hd=20200607"
      ...
    ],
    "raceRankList": [
      //　この中には先ほど追加したurlの大会の大会ランク(G1,G2等)を家から順番に指定していきます。
      "G1",
      "一般",
      "一般",
      "一般"
      ...
    ]
  },
  "2":{
    "excelFile": "2020年6月7日",
    "txtFile": "K200607"
    ...
  }
}
```

※ 注意点
urlListやraceRankListの最後の要素には`,`を付けないようにしましょう。


3. 書き込みをしたいexcelファイルをexcel_dataのフォルダに入れます。

4.最後に確認ができたら、`python3 main.py`というコマンドを実行して待つだけで完成です。

```
