#!/bin/bash

# 英語クエリのテスト
echo "Testing English Query..."
curl -X POST http://localhost:8000/retrieval \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Authorization: Bearer Dify_API_KEY" \
  -d '{
    "knowledge_id": "test-knowledge",
    "query": "RAG",
    "retrieval_setting": {
        "top_k": 3,
        "score_threshold": 0.1
    }
}'

echo -e "\n\n--- Testing Japanese Query ---\n"

# 日本語クエリのテスト（UTF-8でエンコード）
curl -X POST http://localhost:8000/retrieval \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer Dify_API_KEY" \
  -d '{
    "knowledge_id": "test-knowledge",
    "query": "チャットボット",
    "retrieval_setting": {
        "top_k": 10,
        "score_threshold": 0.1
    }
}'