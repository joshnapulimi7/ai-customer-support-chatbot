import uuid
from flask import Flask, render_template, request, jsonify, session
from database import init_db, log_chat, get_session_history
from classifier import classify_query, generate_ai_response

app = Flask(__name__)
app.secret_key = "careerpilot-support-secret-key"

init_db()

@app.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())[:8]
    return render_template("index.html", session_id=session["session_id"])

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = (data.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    session_id = session.get("session_id", str(uuid.uuid4())[:8])
    category = classify_query(user_message)
    bot_response, escalated = generate_ai_response(user_message, category)

    log_chat(session_id, user_message, category, bot_response, int(escalated))

    return jsonify({
        "session_id": session_id,
        "category": category,
        "response": bot_response,
        "escalated": escalated
    })

@app.route("/api/history", methods=["GET"])
def history():
    session_id = session.get("session_id", "")
    logs = get_session_history(session_id)
    return jsonify({"session_id": session_id, "history": logs})

if __name__ == "__main__":
    app.run(debug=True)
