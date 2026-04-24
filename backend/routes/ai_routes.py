from flask import Blueprint, request, jsonify
from services.rag_query import answer_question

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/ask-ai", methods=["POST"])
def ask_ai():

    data = request.json

    question = data["question"]
    repo = data["repo"]

    answer = answer_question(question, repo)

    return jsonify({
        "answer": answer
    })