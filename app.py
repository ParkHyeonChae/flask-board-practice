
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
    query = "SELECT title FROM board "
    cursor.execute(query)
    title_list = [post[0] for post in cursor.fetchall()]

    # for row in user_list:
    #     user_list = row[]
    
    cursor.close()
    conn.close()

    return render_template('post.html', titlelist = title_list)

@app.route('/post/content/<title>')
def content(title):
    conn = pymysql.connect(host='localhost', user = 'root', passwd = '2510', db = 'userlist', charset='utf8')
    cursor = conn.cursor()
    query = "SELECT content FROM board WHERE title = %s"
    value = title
    cursor.execute(query, value)
    content = [post[0] for post in cursor.fetchall()]

    cursor.close()
    conn.close()
    return render_template('content.html', content = content, title = title)

@app.route('/post/edit/<title>', methods=['GET', 'POST'])
def edit(title):
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
 
            edittitle = request.form['title']
            editcontent = request.form['content']

            conn = pymysql.connect(host='localhost', user = 'root', passwd = '2510', db = 'userlist', charset='utf8')
            cursor = conn.cursor()
            query = "UPDATE board SET title = %s, content = %s WHERE title = %s"
            value = (edittitle, editcontent, title)
            cursor.execute(query, value)
            conn.commit()
            cursor.close()
            conn.close()

            return render_template('editSuccess.html')
    else:
        if 'username' in session:
            username = session['username']
            conn = pymysql.connect(host='localhost', user = 'root', passwd = '2510', db = 'userlist', charset='utf8')
            cursor = conn.cursor()
            query = "SELECT title FROM board WHERE name = %s"
            value = username
            cursor.execute(query, value)
            data = [post[0] for post in cursor.fetchall()]
            cursor.close()
            conn.close()

            if title in data:
                return render_template('edit.html',logininfo = username, title = title)
            else:
                return render_template('editError.html')

@app.route('/post/delete/<title>')
def delete(title):
    if 'username' in session:
        username = session['username']
        conn = pymysql.connect(host='localhost', user = 'root', passwd = '2510', db = 'userlist', charset='utf8')
        cursor = conn.cursor()
        query = "SELECT title FROM board WHERE name = %s"
        value = username
        cursor.execute(query, value)
        data = [post[0] for post in cursor.fetchall()]
        cursor.close()
        conn.close()

        if title in data:
            return render_template('delete.html', title = title)
        else:
            return render_template('editError.html')

@app.route('/post/delete/success/<title>')
def deletesuccess(title):
    conn = pymysql.connect(host='localhost', user = 'root', passwd = '2510', db = 'userlist', charset='utf8')
    cursor = conn.cursor()
    query = "DELETE FROM board WHERE title = %s"
    value = title
    cursor.execute(query, value)
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('post'))
    
@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        if 'username' in session:

            username = session['username']
            password = session['password']
            
            usertitle = request.form['title']
            usercontent = request.form['content']

            conn = pymysql.connect(host='localhost', user = 'root', passwd = '2510', db = 'userlist', charset='utf8')
            cursor = conn.cursor()
             
            query = "INSERT INTO board (name, pass, title, content) values (%s, %s, %s, %s)"
            value = (username, password, usertitle, usercontent)

            cursor.execute(query, value)
            #data = cursor.fetchall()
            conn.commit()
            
            cursor.close()
            conn.close()

            return redirect(url_for('post'))
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
        session['password'] = request.form['pw']

        userid = request.form['id']
        userpw = request.form['pw']

        logininfo = request.form['id']
        
        conn = pymysql.connect(host='localhost', user = 'root', passwd = '2510', db = 'userlist', charset='utf8')
        cursor = conn.cursor()
         
        query = "SELECT * FROM tbl_user WHERE user_name = %s AND user_password = %s"
        value = (userid, userpw)
        #cursor.execute("set names utf8")
        cursor.execute(query, value)
        data = cursor.fetchall() # SQL 실행 결과를 가져옴
        
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