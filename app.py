from flask import Flask, jsonify, request, render_template, send_from_directory
import os

app = Flask(__name__, template_folder=".", static_folder=".")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/linkedin")
def linkedin_index():
    return render_template("linkedin.html")


@app.route("/api/scrape_linkedin", methods=["POST"])
def api_scrape_linkedin():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"success": False, "error": "Missing url"})

    try:
        from linkedin_scraper import api_scrape_linkedin_post

        result = api_scrape_linkedin_post(url)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/api/tags", methods=["GET"])
def api_tags():
    try:
        from scraper import get_tags

        tags = get_tags()
        return jsonify({"success": True, "tags": tags})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/api/headlines", methods=["POST"])
def api_headlines():
    data = request.json
    tag_url = data.get("tag_url")
    if not tag_url:
        return jsonify({"success": False, "error": "Missing tag_url"})

    try:
        from scraper import get_headlines_from_tag

        headlines = get_headlines_from_tag(tag_url)
        return jsonify({"success": True, "headlines": headlines})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/api/scrape", methods=["POST"])
def api_scrape():
    data = request.json
    story_url = data.get("story_url")
    headline = data.get("headline", "Unknown Story")
    if not story_url:
        return jsonify({"success": False, "error": "Missing story_url"})

    try:
        from scraper import scrape_story

        filepath = scrape_story(story_url, headline)
        return jsonify({"success": True, "filepath": filepath})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/download/<folder>/<filename>")
def download_file(folder, filename):
    allowed_folders = ["linkedin text", "linkedin image", "linkedin video", "texts"]
    if folder not in allowed_folders:
        return "Invalid folder", 403

    base_dir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(base_dir, folder)
    return send_from_directory(directory, filename, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
