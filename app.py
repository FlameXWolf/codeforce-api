from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def get_codechef_user_details(username):
    url = f"https://www.codechef.com/users/{username}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rating_element = soup.select_one('.rating-number')
        rating = re.search(r'\d+', rating_element.text).group() if rating_element else 'N/A'
        
        division = soup.select_one('.rating-header div:nth-of-type(2)')
        division = division.text.strip() if division else 'N/A'
        
        highest_rating = soup.select_one('.rating-header small')
        highest_rating = highest_rating.text.strip() if highest_rating else 'N/A'
        
        global_rank = soup.select_one('.rating-ranks ul li:nth-of-type(1) strong')
        global_rank = global_rank.text.strip() if global_rank else 'N/A'
        
        country_rank = soup.select_one('.rating-ranks ul li:nth-of-type(2) strong')
        country_rank = country_rank.text.strip() if country_rank else 'N/A'
        
        return {
            'rating': rating,
            'division': division,
            'highest_rating': highest_rating,
            'global_rank': global_rank,
            'country_rank': country_rank
        }
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

@app.route('/user/<username>')
def user_details(username):
    details = get_codechef_user_details(username)
    if details:
        return jsonify(details)
    else:
        return jsonify({"error": "User not found or unable to fetch details"}), 404

if __name__ == '__main__':
    app.run(debug=True)
