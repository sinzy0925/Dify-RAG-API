from flask import Flask, request, jsonify
import json
import logging
from auth import require_api_key
from rag import RAGEngine
from config import CSV_PATH, HOST, PORT, DEFAULT_TOP_K, DEFAULT_SCORE_THRESHOLD
import traceback

# ログ設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# JSONエンコーダーの設定
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return super().default(obj)
    
    def encode(self, obj):
        # 日本語文字列のエンコードを確実に行う
        return json.dumps(obj, ensure_ascii=False, indent=2)

app.json_encoder = CustomJSONEncoder
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# RAGエンジンの初期化
try:
    rag_engine = RAGEngine(CSV_PATH)
    logging.info("RAG engine initialized successfully")
except Exception as e:
    logging.error(f"Failed to initialize RAG engine: {str(e)}\n{traceback.format_exc()}")
    raise

@app.route('/',methods=['GET'])
def aaa():
    return {"echo":"Hello World"}

@app.route('/retrieval', methods=['POST'])
@require_api_key
def retrieval():
    try:
        # リクエストボータを明示的にUTF-8でデコード
        raw_data = request.get_data()
        if not raw_data:
            return jsonify({
                'error_code': 400,
                'error_msg': 'Missing request body'
            }), 400
            
        try:
            data = json.loads(raw_data.decode('utf-8'))
        except UnicodeDecodeError:
            # UTF-8でデコードできない場合は他のエンコーディングを試す
            data = json.loads(raw_data.decode('shift-jis'))
        
        # 必須パラメータの検証
        required_params = ['knowledge_id', 'query', 'retrieval_setting']
        if not all(param in data for param in required_params):
            return jsonify({
                'error_code': 400,
                'error_msg': f'Missing required parameters. Required: {required_params}'
            }), 400
            
        # クエリのログ出力（デバッグ用）
        logging.debug(f"Received query: {data['query']}")
            
        # 検索設定の取得
        retrieval_setting = data.get('retrieval_setting', {})
        top_k = retrieval_setting.get('top_k', DEFAULT_TOP_K)
        score_threshold = retrieval_setting.get('score_threshold', DEFAULT_SCORE_THRESHOLD)
        
        # RAG検索の実行
        records = rag_engine.search(
            query=data['query'],
            top_k=top_k,
            score_threshold=score_threshold
        )
        
        # レスポンスの生成（日本語対応）
        response = app.response_class(
            response=json.dumps({"records": records}, ensure_ascii=False, indent=2),
            status=200,
            mimetype='application/json'
        )
        
        # エンコーディングとCORSヘッダーの設定
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
        return response
        
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'error_code': 500,
            'error_msg': f'Internal server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
