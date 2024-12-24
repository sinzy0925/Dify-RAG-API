# Dify-RAG-API

## アプリの起動方法１）
### Difyで「v02_YouTubeで学習を加速する要約アプリ」を起動したら以下も起動しないと字幕取得できない
- １）Youtube字幕取得API起動
- ```python youtube_api01.py```
- ２）ngrok起動
- ```ngrok http 8001```

## アプリの起動方法２）
### difyで「チャットフロー外部ナレッジAPI(RAG-API)」を起動したら以下も起動しないとRAGが使えない
- １）DIFY-RAG-API起動
- ```python main.py```
- ２）cloudflare起動(Ngrokでは公開できなかったため導入した)
- ```.\cloudflared-windows-amd64 tunnel run rag-api```

     
