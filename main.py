from flask import Flask, render_template, request
import requests
import my_creds 

app = Flask(__name__)

YOUTUBE_API_KEY = my_creds.YOUTUBE_API_KEY
YOUTUBE_SEARCH_URL = my_creds.YOUTUBE_SEARCH_URL

def search_youtube(query, order="relevance", page_token=None):
    """Searches YouTube for videos based on a query and sorting order."""
    params = {
        "part": "snippet",
        "order": order,  # Use the selected order
        "q": query,
        "key": YOUTUBE_API_KEY,
        "type": "video",
        "maxResults": 20,
        "pageToken": page_token
    }

    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    data = response.json()
    return data

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        order = request.form.get("order", "relevance")  # Get from form
    else:
        query = request.args.get("query", "").strip()
        order = request.args.get("order", "relevance")  # Get from URL (pagination)

    page_token = request.args.get("page_token")  # Get pagination token from URL

    videos = []
    next_page_token = None
    prev_page_token = None

    if query:
        results = search_youtube(query, order, page_token)

        if isinstance(results, dict):
            videos = results.get("items", [])
            next_page_token = results.get("nextPageToken")
            prev_page_token = results.get("prevPageToken")
        else:
            print("Unexpected API response.")

    return render_template(
        "index.html",
        query=query,
        videos=videos,
        order=order,  # Pass order to template for pagination
        next_page_token=next_page_token,
        prev_page_token=prev_page_token
    )

if __name__ == "__main__":
    app.run(debug=True)
