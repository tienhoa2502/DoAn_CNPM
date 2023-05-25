from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/crawldata', methods=['POST'])
def crawl_data():
    url = request.form.get('url')
    keyword = request.form.get('keyword')
    crawl_times = int(request.form.get('crawl_times'))

    # Code xử lý dữ liệu JSON ở đây

    return jsonify(json_data)

if __name__ == '__main__':
    app.run()
