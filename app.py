
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
    return render_template('index.html', logininfo = "로그인 안됨" )

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

        login_info = request.form['id']
        
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
            return render_template('main.html', login_info_html = login_info)
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
        value = (userid)
        
        cursor.execute(query, value)
        data = (cursor.fetchall()) 

        if data:
            return render_template('registError.html') 
        else:
            query = "INSERT INTO tbl_user (user_name, user_password) values (%s, %s)"
            value = (userid, userpw)
            cursor.execute(query, value)
            data = cursor.fetchall()
            
            if not data:
                conn.commit()
                #print (data)
                return render_template('registSuccess.html') 
            else:
                conn.rollback()
                #print (data)
                #return "Register Failed"
                return render_template('registError.html') # 적용이 안됨

        cursor.close()
        conn.close()
    else:
        return render_template('regist.html')        

@app.route('/main',methods=['GET','POST'])
def main():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)