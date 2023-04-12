from flask import Flask, request, jsonify
from flask_cors import CORS

from webpage_crawling import webpage_crawling
from retrieval_function import query_retrieval
from semantics_search import semantics_search

app = Flask(__name__)
CORS(app)

crawl = webpage_crawling()
query = query_retrieval()
semantics = semantics_search()


@app.route('/crawl', methods=['GET'])
def start_crawl():
    crawl.start()
    return jsonify({'status': 'ok'})


@app.route('/query_vector', methods=['GET'])
def retrieval_vector():
    keyword = request.args.get("keyword")
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

    app.run(debug=True)
