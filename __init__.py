from flask import Flask, render_template, request
# from flask_sqlalchemy import SQLAlchemy
import requests
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        title = request.form['Title'] # search.html에서 form에 title을 받음
        con = sqlite3.connect('/Users/jeongdaun/Desktop/AIB/Section3/section3_project/database.db')
        cur = con.cursor()
        cur.execute(f"SELECT * FROM info WHERE name='{title}'")
        rows = cur.fetchall()
        print(rows)
        return render_template("search.html", rows=rows)
    else:
        return render_template("search.html")


# @app.route('/list')
# def list():
#    con = sqlite3.connect("database.db") #database.db파일에 접근.
#    con.row_factory = sqlite3.Row 
   
#    cur = con.cursor() #입력커서 놓기.
#    cur.execute("select * from info") #데이터 검색 
   
#    rows = cur.fetchall(); #레코드 단위로 데이터를 전달받음.
#    return render_template("list.html",rows = rows) #rows객체를 리스트 타입으로 list.html에 전달.


if __name__ ==  '__main__':
    app.run()