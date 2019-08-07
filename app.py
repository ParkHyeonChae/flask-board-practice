
from flask import Flask, render_template, session, url_for, request
import pymysql

app = Flask(__name__)

@app.route('/')
def index():
    session['logged'] = False
    return render_template('index.html')

@app.route('/login')
def login(): 
    return render_template('login.html')

@app.route('/regist', methods=['GET', 'POST'])
def regist():
    error= None
    if request.method == 'POST':

        userid = request.form['id']
        userpw = request.form['pw']

        print(userid, userpw)

        conn = pymysql.connect(host='localhost', user = 'root', passwd = '2510', db = 'userlist', charset='utf8')
        cursor = conn.cursor()

        query = "INSERT INTO tbl_user (user_name, user_password) values (%s, %s)"
        value = (userid, userpw)
        cursor.execute(query, value)
        data = cursor.fetchall()
        print (data)
        if not data:
            conn.commit()
            print (data)
            return "Register Success"
        else:
            conn.rollback()
            print (data)
            return "Register Failed"
        cursor.close()
        conn.close()
        return render_template('index.html')

    else:
        return render_template('regist.html')        

@app.route('/main', methods=['POST'])
def main():
    if request.method == 'POST':
        if(request.form['id'] == '현채' and request.form['pw'] == '123'):
            # session['logged'] = True
            # session['user'] = request.form['id']
            login_info = request.form['id']
            return render_template('main.html', login_info_html=login_info)
        else:
            return """<script>alert("wrong!");location.href='/login';</script>"""
    else:
        return """<script>alert("not allowd!");location.href='/login';</script>"""
app.secret_key = 'sample_secret'

if __name__ == '__main__':
    app.run()