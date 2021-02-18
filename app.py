from flask import Flask
import pymysql

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

@app.route('/')
def index():
    return 'Hello, World!222222'

@app.route('/file/upload')
def upload():
    db_settings = {
        "host": "172.50.0.3",
        "port": 3306,
        "user": "root",
        "password": "",
        "db": "my_DB",
        "charset": "utf8"
    }
    try:
        # 建立Connection物件
        conn = pymysql.connect(**db_settings)
    except Exception as ex:
        print(ex)
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)