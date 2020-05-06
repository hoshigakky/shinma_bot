# シノアリス 神魔 Discordボット
神魔画像を投稿することでテキストチャンネルにその日の神魔武器種を投稿します。  
通知時間を設定するとリマインドします。  
時々解析に失敗します。  

## Bot URL
以下のURLからBotを追加してください。  
https://discordapp.com/api/oauth2/authorize?client_id=608260208086745101&permissions=2048&scope=bot

## コマンド
* /inch [チャンネル名]: 画像投稿チャンネルを設定
* /outch [チャンネル名]: 神魔情報投稿チャンネルを設定
* /time [通知時間(08:00,18:05等)]: リマインドする時間を設定
* /info: 設定内容表示

## 設定イメージ
1コマンドずつテキストチャンネルに投稿してください。  
画像投稿チャンネルは投稿専用のチャンネルを作成してください。  
関係ない画像が貼られるとゴミが神魔情報投稿チャンネルに投稿されます。  
```
/inch 一般
/outch 神魔ちゃんねる
/time 12:30
```

## 投稿サンプル画像
投稿する画像の解像度はなるべく大きいものにしてください。  
小さいと失敗します。  
<img src="https://github.com/hoshigakky/shinma_bot/blob/master/data/%E6%97%8B%E9%A2%A8%E3%81%AE%E5%8E%84%E7%81%BD_%E6%97%A5%E8%BC%AA%E3%81%AE%E5%8E%84%E7%81%BD.png" width="30%" />

## 結果イメージ
数秒から数分後に以下のような結果がBotから投稿されます。  
![](https://github.com/hoshigakky/shinma_bot/blob/master/data/result_sample.png)
