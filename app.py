from flask import Flask, request, jsonify
import pymysql
import base64
from Crypto.Hash import SHA1
from config import DBGroups, SplitLength

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

DBHosts = []
try:
    for host in DBGroups:
        print('  > MySQL Host: ' + host['host'])
        DBHosts.append(pymysql.connect(**host))
except Exception as ex:
    print(ex)


@app.route('/')
def index():
    return 'Hello, World!222222'


@app.route('/test')
def test():
    print((DBHosts))
    print(len(DBHosts))
    for conn in DBHosts:
        cursor_object = conn.cursor()
        sql_query = "CREATE TABLE Test(tag varchar(32),Data longtext)"
        cursor_object.execute(sql_query)
        print('  > MySQL Perform SQL: ' + sql_query)

    return 'wow!!'


@app.route('/file/upload', methods=['POST'])
def upload():
    """
    data
    tag
    key
    """

    tag = request.form.get('tag')
    key = request.form.get('key')
    data = request.files['data']
    encoded = base64.b64encode(data.read()).decode('utf-8')

    h = SHA1.new()
    h.update(key.encode('utf-8'))

    key = h.hexdigest()[0:len(DBHosts)]
    last = -1
    print(SplitLength)
    print(key)
    for i in range(0, len(key)):
        length = int(len(encoded) * SplitLength[key[i]])
        cursor = DBHosts[i].cursor()
        sql = "INSERT INTO Test VALUES (%(tag)s, %(data)s)"
        cursor.execute(sql, {
            'tag': tag,
            'data': encoded[last + 1:last + length]
        })
        print('  > MySQL Perform SQL: ' + sql)
        print('Data %s' % encoded[last + 1:last + length])
        last = last + length

    """        cursorObject = conn.cursor()
            sqlQuery = "CREATE TABLE Employee(id int, LastName varchar(32), FirstName varchar(32), DepartmentCode int)"
            # cursorObject.execute(sqlQuery)
    """

    print(encoded)
    #print(request.headers)
    #print(request.data)
    return jsonify({
        'status': True,
        'tag': tag,
        'data': encoded,
        'len': len(encoded)
    })


@app.route('/file/content', methods=['POST'])
def content():
    """
    data
    tag
    key
    len
    """

    tag = request.form.get('tag')
    key = request.form.get('key')
    data_length = request.form.get('len')
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        cursorObject = conn.cursor()
        sqlQuery = "CREATE TABLE Employee(id int, LastName varchar(32), FirstName varchar(32), DepartmentCode int)"
        # cursorObject.execute(sqlQuery)

    except Exception as ex:
        print(ex)

    print('read data')
    print(request.headers)
    print(request.data)
    return jsonify({
        'status': True,
        'tag': tag,
        'data': ""
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=10022)
