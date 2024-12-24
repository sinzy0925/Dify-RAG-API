from fastapi import FastAPI, HTTPException, Query, Request # Import Request
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript
import re
import json
from langdetect import detect
from datetime import datetime
import pytz
import uvicorn

# FastAPIアプリ設定
app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

languages = {"ja": "Japanese","jv": "Javanese","en": "English",    "ab": "Abkhazian",    "aa": "Afar",    "af": "Afrikaans",    "ak": "Akan",    "sq": "Albanian",    "am": "Amharic",    "ar": "Arabic",    "hy": "Armenian",    "as": "Assamese",    "ay": "Aymara",    "az": "Azerbaijani",    "bn": "Bangla",    "ba": "Bashkir",    "eu": "Basque",    "be": "Belarusian",    "bho": "Bhojpuri",    "bs": "Bosnian",    "br": "Breton",    "bg": "Bulgarian",    "my": "Burmese",    "ca": "Catalan",    "ceb": "Cebuano",    "zh-Hans": "Chinese (Simplified)",    "zh-Hant": "Chinese (Traditional)",    "co": "Corsican",    "hr": "Croatian",    "cs": "Czech",    "da": "Danish",    "dv": "Divehi",    "nl": "Dutch",    "dz": "Dzongkha",    "eo": "Esperanto",    "et": "Estonian",    "ee": "Ewe",    "fo": "Faroese",    "fj": "Fijian",    "fil": "Filipino",    "fi": "Finnish",    "fr": "French",    "gaa": "Ga",    "gl": "Galician",    "lg": "Ganda",    "ka": "Georgian",    "de": "German",    "el": "Greek",    "gn": "Guarani",    "gu": "Gujarati",    "ht": "Haitian Creole",    "ha": "Hausa",    "haw": "Hawaiian",    "iw": "Hebrew",    "hi": "Hindi",    "hmn": "Hmong",    "hu": "Hungarian",    "is": "Icelandic",    "ig": "Igbo",    "id": "Indonesian",    "iu": "Inuktitut",    "ga": "Irish",    "it": "Italian",    "kl": "Kalaallisut",    "kn": "Kannada",    "kk": "Kazakh",    "kha": "Khasi",    "km": "Khmer",    "rw": "Kinyarwanda",    "ko": "Korean",    "kri": "Krio",    "ku": "Kurdish",    "ky": "Kyrgyz",    "lo": "Lao",    "la": "Latin",    "lv": "Latvian",    "ln": "Lingala",    "lt": "Lithuanian",    "lua": "Luba-Lulua",    "luo": "Luo",    "lb": "Luxembourgish",    "mk": "Macedonian",    "mg": "Malagasy",    "ms": "Malay",    "ml": "Malayalam",    "mt": "Maltese",    "gv": "Manx",    "mi": "Māori",    "mr": "Marathi",    "mn": "Mongolian",    "mfe": "Morisyen",    "ne": "Nepali",    "new": "Newari",    "nso": "Northern Sotho",    "no": "Norwegian",    "ny": "Nyanja",    "oc": "Occitan",    "or": "Odia",    "om": "Oromo",    "os": "Ossetic",    "pam": "Pampanga",    "ps": "Pashto",    "fa": "Persian",    "pl": "Polish",    "pt": "Portuguese",    "pt-PT": "Portuguese (Portugal)",    "pa": "Punjabi",    "qu": "Quechua",    "ro": "Romanian",    "rn": "Rundi",    "ru": "Russian",    "sm": "Samoan",    "sg": "Sango",    "sa": "Sanskrit",    "gd": "Scottish Gaelic",    "sr": "Serbian",    "crs": "Seselwa Creole French",    "sn": "Shona",    "sd": "Sindhi",    "si": "Sinhala",    "sk": "Slovak",    "sl": "Slovenian",    "so": "Somali",    "st": "Southern Sotho",    "es": "Spanish",    "su": "Sundanese",    "sw": "Swahili",    "ss": "Swati",    "sv": "Swedish",    "tg": "Tajik",    "ta": "Tamil",    "tt": "Tatar",    "te": "Telugu",    "th": "Thai",    "bo": "Tibetan",    "ti": "Tigrinya",    "to": "Tongan",    "ts": "Tsonga",    "tn": "Tswana",    "tum": "Tumbuka",    "tr": "Turkish",    "tk": "Turkmen",    "uk": "Ukrainian",    "ur": "Urdu",    "ug": "Uyghur",    "uz": "Uzbek",    "ve": "Venda",    "vi": "Vietnamese",    "war": "Waray",    "cy": "Welsh",    "fy": "Western Frisian",    "wo": "Wolof",    "xh": "Xhosa",    "yi": "Yiddish",    "yo": "Yoruba",    "zu": "Zulu"}

def get_current_datetime_jst():
    """現在日時を日本時間で取得します。"""
    # 日本のタイムゾーンを設定
    jst = pytz.timezone('Asia/Tokyo')

    # 現在日時をUTCで取得
    utc_now = datetime.utcnow()

    # UTCのdatetimeオブジェクトを日本時間に変換
    jst_now = utc_now.replace(tzinfo=pytz.utc).astimezone(jst)

    return jst_now
@app.get("/")
async def root():
    print({"status": "ok", "message": "API is running"})
    return {"status": "ok", "message": "API is running"}

def extract_youtube_video_id(url):
    """YouTube動画URLからVideo IDを抽出"""
    match = re.search(r"(?:v=|youtu\.be\/)([0-9A-Za-z_-]+)", url)
    return match.group(1) if match else None

# ヘルパー関数
@app.get("/transcript")
def get_video_transcript(videoId: str = Query(..., pattern=r"^[0-9A-Za-z_-]{11}$")): # バリデーションを追加    ic('Start def get_video_transcript(videoId: str = Query(...)):')
    print(f'get_video_transcript videoId: {videoId} で呼び出されました') # 
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            videoId,
            languages=[
                "ja", "en", "ab", "aa", "af", "ak", "sq", "am", "ar", "hy",
                "as", "ay", "az", "bn", "ba", "eu", "be", "bho", "bs", "br",
                "bg", "my", "ca", "ceb", "zh-Hans", "zh-Hant", "co", "hr",
                "cs", "da", "dv", "nl", "dz", "eo", "et", "ee", "fo", "fj",
                "fil", "fi", "fr", "gaa", "gl", "lg", "ka", "de", "el", "gn",
                "gu", "ht", "ha", "haw", "iw", "hi", "hmn", "hu", "is", "ig",
                "id", "iu", "ga", "it", "jv", "kl", "kn", "kk", "kha", "km",
                "rw", "ko", "kri", "ku", "ky", "lo", "la", "lv", "ln", "lt",
                "lua", "luo", "lb", "mk", "mg", "ms", "ml", "mt", "gv", "mi",
                "mr", "mn", "mfe", "ne", "new", "nso", "no", "ny", "oc", "or",
                "om", "os", "pam", "ps", "fa", "pl", "pt", "pt-PT", "pa", "qu",
                "ro", "rn", "ru", "sm", "sg", "sa", "gd", "sr", "crs", "sn",
                "sd", "si", "sk", "sl", "so", "st", "es", "su", "sw", "ss",
                "sv", "tg", "ta", "tt", "te", "th", "bo", "ti", "to", "ts",
                "tn", "tum", "tr", "tk", "uk", "ur", "ug", "uz", "ve", "vi",
                "war", "cy", "fy", "wo", "xh", "yi", "yo", "zu"
            ])
        
        #print(transcript)

        transcript_time = [{'text': item['text'], 'start': item['start']} for item in transcript]

        #print(result)

        formatter = TextFormatter()
        transcript = formatter.format_transcript(transcript)
        detected_lang = detect(transcript)
        detected_lang = languages[detected_lang]
        now_jst = get_current_datetime_jst()
        

        print('transcript[:50]: ',transcript[:50])
        print('now_jst: ',now_jst.strftime("%Y-%m-%d %H:%M:%S"))

        res = {"lang":detected_lang,"text":transcript,"text_time":transcript_time,"now_jst":now_jst.strftime("%Y-%m-%d %H:%M:%S")}
        res = json.dumps(res,ensure_ascii=False)

        return res

    except TranscriptsDisabled as e:  # youtube_transcript_api. は不要
        print(f"status_code=404 An unexpected error occurred: {e}")  # or logging.error(...)
        raise HTTPException(status_code=404, detail="Internal Server Error")
    except NoTranscriptFound as e:  # youtube_transcript_api. は不要
        print(f"status_code=404 An unexpected error occurred: {e}")  # or logging.error(...)
        raise HTTPException(status_code=404, detail="Internal Server Error")
    except CouldNotRetrieveTranscript as e:  # youtube_transcript_api. は不要
        print(f"status_code=500 An unexpected error occurred: {e}")  # or logging.error(...)
        raise HTTPException(status_code=500, detail="Internal Server Error")    
    except Exception as e:
        print(f"status_code=500 An unexpected error occurred: {e}")  # or logging.error(...)
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)