from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('spotiindex.html')

@app.route('/get_trending_apps')
def get_trending_apps():
    url = 'https://appfigures.com/top-apps/google-play/united-states/top-overall'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data'}), 500

    soup = BeautifulSoup(response.text, 'html.parser')

    def extract_apps(section_title):
        section = soup.find('h3', string=section_title)
        if not section:
            return []
        app_list = []
        for li in section.find_next('ol').find_all('li'):
            rank = li.find('span', class_='rank').get_text(strip=True)
            title = li.find('span', class_='title').get_text(strip=True)
            developer = li.find('span', class_='developer').get_text(strip=True)
            price_tag = li.find('span', class_='price')
            price = price_tag.get_text(strip=True) if price_tag else 'Free'
            app_list.append({
                'rank': rank,
                'title': title,
                'developer': developer,
                'price': price
            })
        return app_list

    free_apps = extract_apps('Free')
    paid_apps = extract_apps('Paid')
    grossing_apps = extract_apps('Grossing')

    return jsonify({
        'free': free_apps,
        'paid': paid_apps,
        'grossing': grossing_apps
    })

if __name__ == '__main__':
    app.run(debug=True)
