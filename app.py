from flask import Flask, request, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)
DOWNLOAD_DIR = "static"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/download", methods=["GET"])
def download():
    video_id = request.args.get("id")
    if not video_id:
        return jsonify({"error": "Missing video ID"}), 400

    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        subprocess.run(
            ["yt-dlp", "-f", "bestvideo+bestaudio", "-o", filepath, url],
            check=True
        )
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Download failed", "details": str(e)}), 500

    domain = request.host_url.rstrip("/")
    return jsonify({
        "status": "success",
        "downloadUrl": f"{domain}/static/{filename}"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
