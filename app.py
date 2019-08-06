
from flask import Flask, render_template, request, session, url_for
import pymysql

app = Flask(__name__)

@app.route('/')
def index():
    session['logged'] = False
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login(): 
    return render_template('login.html')

@app.route('/regist'])
    return render_template('regist.html')        

@app.route('/main', methods=['POST'])
def main():
    if request.method == 'POST':
        if(request.form['name'] == '현채' and request.form['pw'] == '123'):
            # session['logged'] = True
            # session['user'] = request.form['id']
            login_info = request.form['name']
            return render_template('main.html', login_info_html=login_info)
        else:
            return """<script>alert("wrong!");location.href='/login';</script>"""
    else:
        return """<script>alert("not allowd!");location.href='/login';</script>"""
app.secret_key = 'sample_secret'

if __name__ == '__main__':
    app.run()