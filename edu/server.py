from flask import Flask, render_template, request, send_from_directory
from inference import answer

app = Flask(__name__, static_folder="frontend", template_folder="frontend", static_url_path="")

@app.route("/")
def home_page():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/query/<query>", methods=["GET"])
def query(query):
    answer_text = answer(query)
    return {"answer": answer_text}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 7860)