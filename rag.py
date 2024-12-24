import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging
import MeCab
import re
import traceback
import os

class RAGEngine:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path, encoding='utf-8')
        
        # MeCabのパスを環境変数から取得するか、デフォルトパスを使用
        mecab_path = os.getenv('MECAB_PATH', '-Owakati')
        self.mecab = MeCab.Tagger(mecab_path)
        # 初期化時のエラーを回避するためのダミー解析
        self.mecab.parse('')
        
        self.vectorizer = TfidfVectorizer(
            analyzer='char_wb',
            ngram_range=(2, 3),
            max_features=10000,
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
            token_pattern=r'(?u)\b\w+\b'  # 単語の境界をより厳密に
        )
        self._prepare_vectors()
        
    def tokenize(self, text):
        """テキストを形態素解析して単語に分割"""
        try:
            text = self.preprocess_text(text)
            result = self.mecab.parse(text)
            if result is None:
                logging.error("MeCab parse returned None")
                return []
            tokens = result.strip().split()
            logging.debug(f"Tokenized text: {tokens}")  # デバッグ用ログ
            return tokens
        except Exception as e:
            logging.error(f"Tokenization error for text '{text}': {str(e)}")
            return []
        
    def preprocess_text(self, text):
        """テキストの前処理"""
        if not isinstance(text, str):
            text = str(text)
        # 改行を空白に置換
        text = re.sub(r'\n', ' ', text)
        # 特殊文字を削除
        text = re.sub(r'[【】「」『』（）\[\]（）\(\)]+', ' ', text)
        # 連続する空白を1つに置換
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
        
    def _prepare_vectors(self):
        """質問のベクトル化を行う"""
        try:
            # 質問テキストを抽出してベクトル化
            questions = self.df['question'].fillna('')
            # 前処理を適用
            processed_questions = [self.preprocess_text(q) for q in questions]
            self.question_vectors = self.vectorizer.fit_transform(processed_questions)
            
            # デバッグ用ログ
            logging.info("Vectors prepared successfully")
            logging.debug(f"Total questions: {len(processed_questions)}")
            for i, (orig, proc) in enumerate(zip(questions, processed_questions)):
                logging.debug(f"Q{i}: Original: {orig}")
                logging.debug(f"Q{i}: Processed: {proc}")
            
        except Exception as e:
            logging.error(f"Error preparing vectors: {str(e)}")
            raise

    def search(self, query, top_k=5, score_threshold=0.5):
        """クエリに類似した質問-回答ペアを検索する"""
        try:
            # ク���リの前処理
            processed_query = self.preprocess_text(query)
            logging.debug(f"Search query: {query} -> {processed_query}")
            
            # クエリをベクトル化
            query_vector = self.vectorizer.transform([processed_query])
            
            # コサイン類似度を計算
            similarities = cosine_similarity(query_vector, self.question_vectors).flatten()
            
            # クエリの意図を分析
            query_keywords = {
                'RAG': ['rag', 'retrieval', 'augmented', 'generation'],
                'Dify': ['dify', 'defy', 'platform', 'プラットフォーム'],
                # 他のトピックも必要に応じて追加
            }
            
            # クエリがどのトピックに関連するか判定
            query_lower = query.lower()
            matched_topic = None
            for topic, keywords in query_keywords.items():
                if any(keyword in query_lower for keyword in keywords):
                    matched_topic = topic
                    break
            
            if matched_topic:
                # トピックに関連する問のスコアを調整
                for i, question in enumerate(self.df['question']):
                    question_lower = question.lower()
                    if any(keyword in question_lower for keyword in query_keywords[matched_topic]):
                        similarities[i] *= 2.0  # 関トピックのスコアを増加
                    else:
                        similarities[i] *= 0.5  # 無係なトピックのスコアを減少
            
            # スコアの正規化（0-1の範囲に）
            max_score = similarities.max()
            if max_score > 0:
                similarities = similarities / max_score
            
            # 上位k件を取得
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                score = float(similarities[idx])
                if score >= score_threshold:  # スコアが閾値以上の結果のみを返す
                    row = self.df.iloc[idx]
                    result = {
                        "content": str(row['question']) + ' [Answer] ' + str(row['Answer']),
                        "score": score,
                        "title": row['Title'],
                        #"question": str(row['question']), # ここで質問を追加
                        "metadata": {}
                    }
                    if 'url' in row:
                        result["metadata"]["url"] = row['url']
                    results.append(result)
                    logging.info(f"Found match: {row['question']} (score: {score:.4f})")
            
            return results
            
        except Exception as e:
            logging.error(f"Search error: {str(e)}\n{traceback.format_exc()}")
            raise
