from flask import Flask, render_template, request
import requests
import my_creds 


app = Flask(__name__)

YOUTUBE_API_KEY = my_creds.YOUTUBE_API_KEY
YOUTUBE_SEARCH_URL = my_creds.YOUTUBE_SEARCH_URL

def search_youtube(query, page_token=None):
    """Searches YouTube for videos based on a query."""
    params = {
        "part": "snippet",
        "q": query,
        "key": YOUTUBE_API_KEY,
        "type": "video",
        "maxResults": 50,
        "pageToken": page_token
    }

    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    data = response.json()
    return data



@app.route("/", methods=["GET", "POST"])
def index():
    query = request.form.get("query", "").strip()
    page_token = request.args.get("page_token")  # Get pagination token from URL

    videos = []
    next_page_token = None
    prev_page_token = None

    if query:
        results = search_youtube(query, page_token)
      

        if isinstance(results, dict):
            videos = results["items"] if "items" in results else []
            next_page_token = results.get("nextPageToken")
            prev_page_token = results.get("prevPageToken")
        else:
            print("Unexpected API ")

    return render_template(
        "index.html",
        query=query,
        videos=videos,
        next_page_token=next_page_token,
        prev_page_token=prev_page_token
    )

if __name__ == "__main__":
    app.run(debug=True)