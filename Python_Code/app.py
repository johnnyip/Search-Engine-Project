from flask import Flask, request, jsonify
from flask_cors import CORS

from api_webpage_crawling import api_webpage_crawling
from api_query_retrieval import api_query_retrieval
from api_semantics_search import api_semantics_search

app = Flask(__name__)
CORS(app, origins="*")

crawl = api_webpage_crawling()
query = api_query_retrieval()
semantics = api_semantics_search()


@app.route('/', methods=['GET'])
def status():
    return "ok"


@app.route('/crawl', methods=['GET'])
def start_crawl():
    crawl.start()
    return jsonify({'status': 'ok'})


@app.route('/query_vector', methods=['GET'])
def retrieval_vector():
    keyword = request.args.get("keyword")
    print(keyword)
    result = query.query_vector(keyword)
    return jsonify({'status': 'ok', 'data': result})


@app.route('/query_pagerank', methods=['GET'])
def retrieval_pagerank():
    keyword = request.args.get("keyword")
    result = query.query_page_rank(keyword)
    return jsonify({'status': 'ok', 'data': result})


@app.route('/query_semantics', methods=['GET'])
def retrieval_semantics():
    keyword = request.args.get("keyword")
    result = semantics.query_semantics(keyword)
    return jsonify({'status': 'ok', 'data': result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)
