from flask import Flask,render_template,request,redirect
import pymysql

conn = pymysql.connect(
    user='root', 
    passwd='java1004', 
    host='127.0.0.1', 
    db='pyapp',
    port=3306,
    charset='utf8'
    )

print(conn)

# 목록보기
app = Flask(__name__)

# 리스트 불러오기
@app.route('/', methods=['GET'])
def msgList():
    cursor = conn.cursor()
    cursor.execute('select msg_id, msg_text from msg')
    list = cursor.fetchall()
    print(list)
    return render_template('msgList.html', list=list)

# 메세지 입력
@app.route('/addMSG', methods=['GET','POST'])
def addMSG():
    if request.method == 'GET':
        return render_template('addMSG.html')
    elif request.method == 'POST':
        msgText = request.form['msgText']
        cursor = conn.cursor()
        cursor.execute('insert into msg(msg_text) values(%s)', [msgText])
        conn.commit()
        return redirect('/')

# 메세지 수정
@app.route('/modMSG', methods=['GET','POST'])
def modMSG():
    if request.method == 'GET':
        msgId = request.args.get('msgId')
        cursor = conn.cursor()
        cursor.execute('select msg_id ,msg_text from msg where msg_id = %s', [msgId])
        msgList = cursor.fetchone()
        print(msgList)
        return render_template('modMSG.html', msgList=msgList)
    elif request.method == 'POST':
        msgText = request.form['msgText']
        msgId = request.form['msgId']
        cursor = conn.cursor()
        cursor.execute('update msg set msg_text = %s where msg_id = %s', [msgText,msgId])
        conn.commit()
        return redirect('/')

# 메시지 삭제
@app.route('/delMSG', methods=['GET'])
def delMSG():
    msgId = request.args.get('msgId')
    cursor = conn.cursor()
    cursor.execute('delete from msg where msg_id = %s', [msgId])
    conn.commit()
    return redirect('/')

app.run(host='127.0.0.1',port=80)