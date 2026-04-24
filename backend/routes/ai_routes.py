from flask import Blueprint, request, jsonify
from services.rag_query import answer_question

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/ask-ai", methods=["POST"])
def ask_ai():

    data = request.get_json() or {}

    question = (data.get("question") or "").strip()
    repo = data.get("repo")
    owner = data.get("owner")

    if not question or not repo:
        return jsonify({"error": "question and repo are required"}), 400

    if not owner:
        return jsonify({"error": "owner is required"}), 400

    answer = answer_question(question, repo, owner)

    return jsonify({
        "answer": answer
    })
