
from flask import Flask, render_template, session, url_for, request, redirect
import pymysql

app = Flask(__name__)
app.secret_key = 'sample_secret'

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', logininfo = username)
    # session['logged'] = False
    else:
        return render_template('index.html', logininfo = "로그인 안됨" )

@app.route('/post')
def post():
    conn = pymysql.connect(host='localhost', user = 'root', passwd = '2510', db = 'userlist', charset='utf8')
    cursor = conn.cursor()
    query = "SELECT user_name FROM tbl_user "
    cursor.execute(query)
    user_list = [item[0] for item in cursor.fetchall()]

    # for row in user_list:
    #     user_list = row[]
    
    cursor.close()
    conn.close()
    return render_template('post.html', userlist = user_list)

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            
            usertitle = request.form['title']
            usercontent = request.form['content']

            conn = pymysql.connect(host='localhost', user = 'root', passwd = '2510', db = 'userlist', charset='utf8')
            cursor = conn.cursor()
             
            query = "INSERT INTO board (name, title, content) values (%s, %s, %s)"
            value = (username, usertitle, usercontent)

            cursor.execute(query, value)
            data = (cursor.fetchall())
            conn.commit()
            
            cursor.close()
            conn.close()

            return render_template('post.html')
        else:
            pass
            #return render_template('errorpage.html')
    else:
        if 'username' in session:
            username = session['username']
            return render_template ('write.html', logininfo=username)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET','POST'])
def login():
    #error = None
    if request.method == 'POST':

        session['username'] = request.form['id']

        userid = request.form['id']
        userpw = request.form['pw']

        logininfo = request.form['id']
        
        conn = pymysql.connect(host='localhost', user = 'root', passwd = '2510', db = 'userlist', charset='utf8')
        cursor = conn.cursor()
         
        query = "SELECT * FROM tbl_user WHERE user_name = %s AND user_password = %s"
        value = (userid, userpw)
        #cursor.execute("set names utf8")
        cursor.execute(query, value)
        data = (cursor.fetchall()) # SQL 실행 결과를 가져옴
        
        cursor.close()
        conn.close()
        
        for row in data:
            data = row[0]
        
        if data:
            # print ('login success')
            return render_template('main.html', logininfo = logininfo)
        else:
            return render_template('loginError.html')
            #return render_template('python_login.html', error=error)
    else:
        return render_template ('login.html')
#app.secret_key = 'sample_secret'

@app.route('/regist', methods=['GET', 'POST'])
def regist():
    #error = None
    if request.method == 'POST':

        userid = request.form['id']
        userpw = request.form['pw']

        conn = pymysql.connect(host='localhost', user = 'root', passwd = '2510', db = 'userlist', charset='utf8')
        cursor = conn.cursor()

        query = "SELECT * FROM tbl_user WHERE user_name = %s"
        value = userid
        
        cursor.execute(query, value)
        data = (cursor.fetchall())

        #import pdb; pdb.set_trace()
        if data:
            conn.rollback()
            return render_template('registError.html') 
        else:
            query = "INSERT INTO tbl_user (user_name, user_password) values (%s, %s)"
            value = (userid, userpw)
            cursor.execute(query, value)
            data = cursor.fetchall()
            conn.commit()
            return render_template('registSuccess.html')

        cursor.close()
        conn.close()
    else:
        return render_template('regist.html')        

@app.route('/main', methods=['GET','POST'])
def main():
    if 'username' in session:
        username = session['username']
        return render_template('main.html', logininfo = username)
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)