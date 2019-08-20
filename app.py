
from flask import Flask, render_template, session, url_for, request, redirect
import pymysql

app = Flask(__name__)
app.secret_key = 'sample_secret'

@app.route('/')
# 세션유지를 통한 로그인 유무 확인
def index():
    if 'username' in session:
        username = session['username']

        return render_template('index.html', logininfo = username)
    else:
        return render_template('index.html', logininfo = "로그인 안됨" )

@app.route('/post')
# board테이블의 게시판 제목리스트 역순으로 출력
def post():
    if 'username' in session:
        username = session['username']
    else:
        username = None
    conn = pymysql.connect(host='localhost', user = 'root', passwd = '2510', db = 'userlist', charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT id, name, title, wdate, view FROM board ORDER BY id DESC" # ORDER BY 컬럼명 DESC : 역순출력, ASC : 순차출력
    cursor.execute(query)
    #title_list = [post[0] for post in cursor.fetchall()]
    post_list = cursor.fetchall()
    #for row in user_list:
    #     user_list = row[]
    
    cursor.close()
    conn.close()

    return render_template('post.html', postlist = post_list, logininfo=username)

@app.route('/post/content/<title>')
# 조회수 증가, post페이지의 게시글 클릭시 title과 content 비교 후 게시글 내용 출력
def content(title):
    if 'username' in session:
        username = session['username']
        conn = pymysql.connect(host='localhost', user = 'root', passwd = '2510', db = 'userlist', charset='utf8')
        cursor = conn.cursor()
        query = "UPDATE board SET view = view + 1 WHERE title = %s"
        value = title
        cursor.execute(query, value)
        conn.commit()
        cursor.close()
        conn.close()

        conn = pymysql.connect(host='localhost', user = 'root', passwd = '2510', db = 'userlist', charset='utf8')
        cursor = conn.cursor()
        query = "SELECT content FROM board WHERE title = %s"
        value = title
        cursor.execute(query, value)
        content = [post[0] for post in cursor.fetchall()]
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('content.html', content = content, title = title, username = username)
    else:
        return render_template ('Error.html')

@app.route('/post/edit/<title>', methods=['GET', 'POST'])
# GET -> 유지되고있는 username 세션과 현재 접속되어진 title과 일치시 edit페이지 연결
# POST -> 접속되어진 title과 일치하는 title, content를 찾아 UPDATE
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
                return render_template('edit.html', title=title, logininfo=username)
            else:
                return render_template('editError.html')
        else:
            return render_template ('Error.html')

@app.route('/post/delete/<title>')
# 유지되고 있는 username 세션과 title 일치시 삭제확인 팝업 연결
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
    else:
        return render_template ('Error.html')

@app.route('/post/delete/success/<title>')
# 삭제 확인시 title 과 일치하는 컬럼 삭제, 취소시 /post 페이지 연결
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
# GET -> write 페이지 연결
# POST -> username, password를 세션으로 불러온 후, form에 작성되어진 title, content를 테이블에 입력
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
            return render_template ('write.html', logininfo = username)
        else:
            return render_template ('Error.html')

@app.route('/logout')
# username 세션 해제
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET','POST'])
# GET -> 로그인 페이지 연결
# 로그인 시 id, pw 세션유지 후 form에 입력된 id, pw를 table에 저장된 id, pw에 비교후 일치하면 로그인
def login():
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
        cursor.execute(query, value)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        
        for row in data:
            data = row[0]
        
        if data:
            return render_template('main.html', logininfo = logininfo)
        else:
            return render_template('loginError.html')
    else:
        return render_template ('login.html')

@app.route('/regist', methods=['GET', 'POST'])
# GET -> 회원가입 페이지 연결
# 회원가입 버튼 클릭 시, 입력된 id가 tbl_user의 컬럼에 있을 시 에러팝업, 없을 시 회원가입 성공
def regist():
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
            conn.rollback() # 이건 안 써도 될 듯
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