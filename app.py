# board | app.py
# Copyright 2022・5・13 | @gamma410

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy  # SQLで必要なライブラリ
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///postdata.db'  # "postdata.db" という データベースを作成
db = SQLAlchemy(app)  # SQLAlchemy() クラス に app を格納して 変数 db に入れておく - これで使えるようになる

# 項目はクラスオブジェクトで定義
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id：整数値で設定。
    user = db.Column(db.String(20), nullable=False)  # user：20文字以内の文字列で設定。空欄にできない。
    title = db.Column(db.String(30), nullable=False)  # title：30文字以内の文字列で設定。空欄にできない。
    detail = db.Column(db.Text, nullable=False)  # detail：テキスト形式の文字列で設定。空欄にできない。
    post_date = db.Column(db.DateTime, nullable=False)  # post_date：日付型で設定。空欄にできない。

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('index.html', posts=posts)
    else:
        user = request.form.get('user')
        title = request.form.get('title')
        detail = request.form.get('detail')
        post_date = request.form.get('post_date')

        post_date = datetime.strptime(post_date, '%Y-%m-%d')
        new_post = Post(user=user, title=title, detail=detail, post_date=post_date)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/detail/<int:id>')
def detail(id):
    post = Post.query.get(id)
    return render_template('detail.html', post=post)

@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)