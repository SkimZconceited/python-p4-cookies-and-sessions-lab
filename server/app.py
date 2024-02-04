#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session, request, json
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
CORS(app)

migrate = Migrate(app, db)

db.init_app(app)

# @app.route('/clear')
# def clear_session():
#     session['page_views'] = 0
#     return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    article = Article.query.filter_by(id=id).first()
    session['page_views'] = session.get('page_views', 0) + 1
    
    if article:
        article_client = {
            'title': article.title,
            'author': article.author,
            'date': article.date,
            'content': article.content,
            'minutes_to_read': article.minutes_to_read
        }

        
        response_data = {
            'session': {
                'session_key': 'page_views',
                'session_value': session['page_views'],
                'session_accessed': session.accessed,
            },
            'cookies': [{cookie: request.cookies[cookie]} for cookie in request.cookies],
            'article': article_client,
        }

        response = make_response(jsonify(response_data), 200)
        session.get('page_views')

        # Set the 'article' cookie with the article data
        response.set_cookie('article', value=json.dumps(article_client))  # Adjust max_age as needed

        return response
    return response


if __name__ == '__main__':
    app.run(port=5555)
