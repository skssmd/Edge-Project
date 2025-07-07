from flask import Flask, render_template, request, send_from_directory, jsonify, redirect, url_for
import whisperx
import os
import uuid
import json

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
SESSION_FOLDER = "sessions"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SESSION_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        audio = request.files["audio"]
        model_size = request.form["model_size"]
        device = request.form["device"]
        compute_type = request.form["compute_type"]

        if audio:
            session_id = str(uuid.uuid4())
            filename = audio.filename
            audio_path = os.path.join(UPLOAD_FOLDER, filename)
            audio.save(audio_path)

            model = whisperx.load_model(model_size, device=device, compute_type=compute_type)
            audio_data = whisperx.load_audio(audio_path)
            result = model.transcribe(audio_data)

            data = {
                "session_id": session_id,
                "name": filename,
                "audio_url": f"/uploads/{filename}",
                "segments": result["segments"]
            }

            with open(os.path.join(SESSION_FOLDER, f"{session_id}.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            return redirect(url_for("session_view", session_id=session_id))

    return render_template("index.html")

@app.route("/session/<session_id>")
def session_view(session_id):
    try:
        with open(os.path.join(SESSION_FOLDER, f"{session_id}.json"), "r", encoding="utf-8") as f:
            data = json.load(f)
        return render_template("session.html", data=data)
    except FileNotFoundError:
        return "Session not found", 404

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ✅ API to List All Sessions
@app.route("/api/sessions", methods=["GET"])
def list_sessions():
    sessions = []
    for filename in os.listdir(SESSION_FOLDER):
        if filename.endswith(".json"):
            session_id = filename.replace(".json", "")
            with open(os.path.join(SESSION_FOLDER, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
                sessions.append({
                    "session_id": session_id,
                    "name": data.get("name", "Untitled")
                })
    return jsonify(sessions)

if __name__ == "__main__":
    app.run(debug=True)
