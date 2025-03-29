from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_occupancy():
    url = 'https://sport.wp.st-andrews.ac.uk/'
    print(f"Fetching data from: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    response = requests.get(url, headers=headers)
    print(f"Status code: {response.status_code}")

    if response.status_code == 200:
        # Save HTML to a file for inspection
        with open("gym_response.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        
        # Print just a portion to avoid flooding terminal
        print("Response received, first 500 characters:")
        print(response.text[:500])
        soup = BeautifulSoup(response.text, "html.parser")

        all_text = soup.findAll(text=lambda text: text and "Occupancy:" in text)
        if all_text:
            print(f"Found {len(all_text)} text nodes containing 'Occupancy:'")
            for text in all_text:
                print(f"Text node: '{text}'")
                occupancy_value = text.strip().replace("Occupancy:", "").strip()
                return {"status": "success", "occupancy": occupancy_value}

        return {"status": "error", "message": "Occupancy data not found"}

    return {"status": "error", "message": "Failed to retrieve data"}

@app.route("/api/gym-occupancy", methods=["GET"])
def gym_occupancy():
    data = get_occupancy()
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

