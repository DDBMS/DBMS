from flask import Flask, request, jsonify
import pymysql
import base64

from Crypto.Hash import SHA1
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from config import DBGroups, SplitLength
import EatData
import AccessData

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB


"""
DBHosts = []
try:
    for host in DBGroups:
        print('  > MySQL Host: ' + host['host'])
        DBHosts.append(pymysql.connect(**host))
except Exception as ex:
    print(ex)
"""

@app.route('/')
def index():
    return 'Hello, World!222222'


@app.route('/test')
def test():
    DBHosts = []
    try:
        for host in DBGroups:
            print('  > MySQL Host: ' + host['host'])
            DBHosts.append(pymysql.connect(**host))
    except Exception as ex:
        print(ex)


    for conn in DBHosts:
        cursor_object = conn.cursor()
        sql_query = """
        CREATE TABLE IF NOT EXISTS `Test` (
          tag varchar(32),
          data longtext,
          PRIMARY KEY (tag)
        )
        """
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
    # Database Integration
    db_hosts = AccessData.connect()

    # HTTP Request Params
    tag = request.form.get('tag')
    key = request.form.get('key')
    data = request.files['data'].read()

    # 處理並加密資料
    eaten = EatData.encrypt(
        key=key,
        data=data,
        db_num=len(db_hosts)
    )  # map_key, data_b64, iv_b64, cipher_b64

    # 儲存資料
    AccessData.save(
        tag=tag,
        hosts=db_hosts,
        key=eaten[0],
        cipher=eaten[3]
    )

    return jsonify({
        'status': True,
        'tag': tag,
        'len': len(eaten[3].decode('utf8')),
        'iv': eaten[2].decode('utf8')
    })


@app.route('/file/content', methods=['POST'])
def content():
    """
    data
    tag
    key
    len
    """
    # Database Integration
    DBHosts = []
    try:
        for host in DBGroups:
            print('  > MySQL Host: ' + host['host'])
            DBHosts.append(pymysql.connect(**host))
    except Exception as ex:
        print(ex)

    # HTTP Params
    tag = request.form.get('tag')
    key = request.form.get('key')
    data_length = int(request.form.get('len'))

    h = SHA1.new()
    h.update(key.encode('utf-8'))
    key = h.hexdigest()[0:len(DBHosts)]

    data = ""
    last = 0
    out = False
    queue = []
    for i in range(0, len(key)):
        length = int(data_length * SplitLength[key[i]])

        if i == len(key) - 1:
            length = data_length - last

        if last + length > data_length:
            length = data_length - last
            out = True

        queue.append((i,(last,length)))

        last = last + length
        if out: break

    for X in queue:
        cursor = DBHosts[X[0]].cursor(pymysql.cursors.DictCursor)
        sql = """
        SELECT * from Test 
        where 
          tag = %(tag)s
        """
        cursor.execute(sql, {
            'tag': tag
        })
        got = cursor.fetchone()
        print(tag)
        print(got)
        DBHosts[X[0]].commit()
        DBHosts[X[0]].close()

        if got :
            data += got['data']

        print('  > MySQL' + str(X[0]) + ' Perform SQL: ' + sql)

    return jsonify({
        'status': True,
        'tag': tag,
        'data': data
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=10022)
