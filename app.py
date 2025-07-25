from flask import Flask, render_template, request
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import csv
from datetime import datetime
import os

app = Flask(__name__)

# Cấu hình Affiliate mặc định
AFFILIATE_ID = "haudau-aff"  # 👈 Thay bằng mã của bạn
CSV_FILE = 'history.csv'

def add_affiliate(link):
    parsed = urlparse(link)
    query = parse_qs(parsed.query)
    query['af_lid'] = AFFILIATE_ID
    query['af_siteid'] = AFFILIATE_ID
    new_query = urlencode(query, doseq=True)
    new_url = urlunparse(parsed._replace(query=new_query))
    return new_url

def save_to_csv(original_link, final_link):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Thời gian', 'Link gốc', 'Link đã tạo'])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), original_link, final_link])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_link = request.form.get('shopee_link')
        if not original_link:
            return render_template('index.html', error="Vui lòng nhập link Shopee.")

        final_link = add_affiliate(original_link)
        save_to_csv(original_link, final_link)
        return render_template('preview.html', original=original_link, result=final_link)

    return render_template('index.html')
