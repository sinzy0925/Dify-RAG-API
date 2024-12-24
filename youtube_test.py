import json,time
def main(cnt,cnt_from,arg1,arg2,arg3,arg4):
    arg1 = arg1 + arg2 + arg3
    urls = []
    videoIds=[]
    titles=[]
    views=[]
    publishs=[]
    lengths=[]
    # viewsキーがない場合は0として処理する
    sorted_items = sorted(arg1, key=lambda x: x.get('views', 0), reverse=True)

# 重複削除
    unique_items = []
    seen = set()
    for item in sorted_items:
        item_json = json.dumps(item, sort_keys=True) # JSON文字列に変換
        if item_json not in seen:
            seen.add(item_json)
            unique_items.append(item)
                        

    filtered_items = []
    for item in unique_items:
        if arg4.upper() in item.get('title', '').upper():
            filtered_items.append(item)
            print(arg4)
            print(item.get('title', ''))


    # 上位arg3件取得
    top_items = filtered_items[cnt_from:cnt_from+cnt]

    for item in top_items:
        length = item.get('length', '') # lengthキーがない場合は空文字として処理する
        lengths.append(length)
        published = item.get('published_date','')
        publishs.append(published)
        url = item['link']
        videoIds.append(url.split('v=')[1])
        urls.append(url)
        title = item.get('title','')
        titles.append(title)
        # viewsキーがない場合は0として処理する
        view = item.get('views', 0)
        views.append(view)

    time.sleep(1)
        
    res = {"urls": urls,"views":views,"titles":titles,"videoIds":videoIds,"lengths":lengths,"publishs":publishs}

    return res

cnt = 5
cnt_from = 0
arg1=[
    {
      "position_on_page": 2,
      "title": "OpenAIのGPTsより凄い！無料で使えるDifyを徹底解説してみた",
      "link": "https://www.youtube.com/watch?v=O_bmmDWIjTc",
      "serpapi_link": "https://serpapi.com/search.json?engine=youtube_video&gl=jp&hl=ja&v=O_bmmDWIjTc",
      "channel": {
        "name": "にゃんたのAIチャンネル",
        "link": "https://www.youtube.com/@aivtuber2866",
        "thumbnail": "https://yt3.ggpht.com/FIXyucHLT-DvUlmgTVlcZ4Od3ffaqOSUZqHbA1mJOP2DTtCmsUPNEdfZ7MDpSUM2nszziMsu3Q=s68-c-k-c0x00ffffff-no-rj"
      },
      "published_date": "7 か月前",
      "views": 82193,
      "length": "38:08",
      "description": "こんにちは、にゃんたです。 今回は話題になっているDifyの基本的な使い方を解説してみました   めちゃくちゃ便利なので是非 ...",
      "thumbnail": {
        "static": "https://i.ytimg.com/vi/O_bmmDWIjTc/hq720.jpg?sqp=-oaymwEcCOgCEMoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLAKrHN7TL8EFN7tfBjhlNlLjAoIvw",
        "rich": "https://i.ytimg.com/an_webp/O_bmmDWIjTc/mqdefault_6s.webp?du=3000&sqp=CIrco7sG&rs=AOn4CLBpICih0pms7-v7TJDXLuSxxLcSuA"
      }
    },
    {
      "position_on_page": 3,
      "title": "Is Dify the easiest way to build AI Applications?",
      "link": "https://www.youtube.com/watch?v=yXAJwDtAbLo",
      "serpapi_link": "https://serpapi.com/search.json?engine=youtube_video&gl=jp&hl=ja&v=yXAJwDtAbLo",
      "channel": {
        "name": "Matt Williams",
        "link": "https://www.youtube.com/@technovangelist",
        "thumbnail": "https://yt3.ggpht.com/ytc/AIdro_mXVAnytfFhGKFrCuySGeQMMXlclfEdex9Yxx3PVKV9rMI=s68-c-k-c0x00ffffff-no-rj"
      },
      "published_date": "4 か月前",
      "views": 24360,
      "length": "13:50",
      "description": "Dify is a pretty cool tool for making AI apps that you can host. It's not perfect, but there is a lot to like. My Links Subscribe ...",
      "extensions": [
        "4K"
      ],
      "thumbnail": {
        "static": "https://i.ytimg.com/vi/yXAJwDtAbLo/hq720.jpg?sqp=-oaymwEcCOgCEMoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLD1P0qJOQLtRS7Zu05k8Zuh9K_JgQ",
        "rich": "https://i.ytimg.com/an_webp/yXAJwDtAbLo/mqdefault_6s.webp?du=3000&sqp=CNL2o7sG&rs=AOn4CLC-0K5q2zDKrpgxkw6FNwA6gPw4Lw"
      }
    }
  ]
arg2=[{
      "position_on_page": 1,
      "title": "無料で自分用AIチャットボット作れる #dify",
      "link": "https://www.youtube.com/watch?v=GW8ikzHXitc",
      "serpapi_link": "https://serpapi.com/search.json?engine=youtube_video&gl=jp&hl=ja&v=GW8ikzHXitc",
      "channel": {
        "name": "KEITO【AI&WEB ch】",
        "link": "https://www.youtube.com/@keitoaiweb",
        "thumbnail": "https://yt3.ggpht.com/0Gc_bfKZC8MJLbJdjA6axrVRGr3bxjVRz_ZNHFJ2wEYxXqw2f-JU-d-1IuU455YXrBXvJ-05naY=s68-c-k-c0x00ffffff-no-rj"
      },
      "published_date": "7 か月前",
      "views": 57322,
      "length": "0:48",
      "thumbnail": {
        "static": "https://i.ytimg.com/vi/GW8ikzHXitc/hq720.jpg?sqp=-oaymwE2COgCEMoBSFXyq4qpAygIARUAAIhCGABwAcABBvABAfgBtgiAAoAPigIMCAAQARhXIFwoZTAP&rs=AOn4CLBnbeGEtk-hi7fskMl0WdUQyUDxUw",
        "rich": "https://i.ytimg.com/an_webp/GW8ikzHXitc/mqdefault_6s.webp?du=3000&sqp=CN6WpLsG&rs=AOn4CLB3MJv0Xqw1Jj_R8xM2NCTPp4KQkQ"
      }
    },
    {
      "position_on_page": 2,
      "title": "Difyで作る！RAGの精度を向上させるSelf-Routeについて解説してみた",
      "link": "https://www.youtube.com/watch?v=b5zlZkRLh5Y",
      "serpapi_link": "https://serpapi.com/search.json?engine=youtube_video&gl=jp&hl=ja&v=b5zlZkRLh5Y",
      "channel": {
        "name": "にゃんたのAIチャンネル",
        "link": "https://www.youtube.com/@aivtuber2866",
        "thumbnail": "https://yt3.ggpht.com/FIXyucHLT-DvUlmgTVlcZ4Od3ffaqOSUZqHbA1mJOP2DTtCmsUPNEdfZ7MDpSUM2nszziMsu3Q=s68-c-k-c0x00ffffff-no-rj"
      },
      "published_date": "3 か月前",
      "views": 13907,
      "length": "14:33",
      "description": "こんにちは、にゃんたです。 今回は少し前にSNSを騒がせたSelf-Routeという技術について紹介しました！ RAGの精度が中々 ...",
      "thumbnail": {
        "static": "https://i.ytimg.com/vi/b5zlZkRLh5Y/hq720.jpg?sqp=-oaymwEcCOgCEMoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLAFXi4MeCAFBV41MsXgewLLAvzexw",
        "rich": "https://i.ytimg.com/an_webp/b5zlZkRLh5Y/mqdefault_6s.webp?du=3000&sqp=CNCDpLsG&rs=AOn4CLBO_i6W-rZPSMwOFj9t5F-iFeFCvA"
      }
    }]
arg3=[]
arg4='dify'

res = main(cnt,cnt_from,arg1,arg2,arg3,arg4)

print(res)