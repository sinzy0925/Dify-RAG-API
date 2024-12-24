import os
from dotenv import load_dotenv

load_dotenv()

# APIキー設定
API_KEY = os.getenv("API_KEY", "Dify_API_KEY")

# RAG設定
DEFAULT_TOP_K = 5
DEFAULT_SCORE_THRESHOLD = 0.1
CSV_PATH = "RAG.csv"

# サーバー設定
HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", 8000))
