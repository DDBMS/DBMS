from flask import Flask, request, jsonify
import pymysql
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB


@app.route('/')
def index():
    return 'Hello, World!222222'


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

    db_settings = {
        "host": "172.50.0.3",
        "port": 3306,
        "user": "root",
        "password": "root_toor",
        "db": "my_db",
        "charset": "utf8"
    }

    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        cursorObject = conn.cursor()
        sqlQuery = "CREATE TABLE Employee(id int, LastName varchar(32), FirstName varchar(32), DepartmentCode int)"
        # cursorObject.execute(sqlQuery)

    except Exception as ex:
        print(ex)

    print(encoded)
    print('read data')
    return jsonify({
        'status': True,
        'tag': tag,
        'data': encoded
    })

@app.route('/file/content', methods=['POST'])
def content():
    """
    data
    tag
    key
    """

    tag = request.form.get('tag')
    key = request.form.get('key')

    db_settings = {
        "host": "172.50.0.3",
        "port": 3306,
        "user": "root",
        "password": "root_toor",
        "db": "my_db",
        "charset": "utf8"
    }

    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)

        cursorObject = conn.cursor()
        sqlQuery = "CREATE TABLE Employee(id int, LastName varchar(32), FirstName varchar(32), DepartmentCode int)"
        # cursorObject.execute(sqlQuery)

    except Exception as ex:
        print(ex)

    print('read data')
    print(request.data)
    return jsonify({
        'status': True,
        'tag': tag,
        'data': ""
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=10022)
