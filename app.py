import requests
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.ustockplus.com/ipo', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
trs = soup.select('#__next > section > div > div.lBox > article:nth-child(2) > div.tableB > table > tbody > tr')

for tr in trs:
    a_tag = tr.select_one('td.txt')
    b_tag = tr.select_one('td.num')
    if a_tag is not None:
        day = b_tag.text
        name = a_tag.text
        doc = {
            'day': day,
            'name': name
        }
        db.stock.insert_one(doc)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['GET'])
def listing():
    stock = list(db.stock.find({}, {'_id': False}))
    return jsonify({'all_stock': stock})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
