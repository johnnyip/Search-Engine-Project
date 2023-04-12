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
    result = query.query_vector("")
    return jsonify({'status': 'ok', 'data': result})


@app.route('/query_pagerank', methods=['GET'])
def retrieval_pagerank():
    result = query.query_page_rank("")
    return jsonify({'status': 'ok', 'data': result})


@app.route('/query_semantics', methods=['GET'])
def retrieval_semantics():
    result = semantics.query_semantics("")
    return jsonify({'status': 'ok', 'data': result})


if __name__ == '__main__':

    app.run(debug=True)
