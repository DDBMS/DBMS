from flask import Flask, request, jsonify
import pymysql
import base64
from Crypto.Hash import SHA1, MD5
from Crypto.Cipher import AES
from config import DBGroups, SplitLength

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
    DBHosts = []
    try:
        for host in DBGroups:
            print('  > MySQL Host: ' + host['host'])
            DBHosts.append(pymysql.connect(**host))
    except Exception as ex:
        print(ex)

    # HTTP Request Params
    tag = request.form.get('tag')
    key = request.form.get('key')
    data = request.files['data']
    encoded = base64.b64encode(data.read()).decode('utf8')

    h = MD5.new()
    h.update(key.encode('utf-8'))
    encrypt_key = h.digest()

    h = SHA1.new()
    h.update(key.encode('utf-8'))
    key = h.hexdigest()[0:len(DBHosts)]

    cipher = AES.new(encrypt_key, AES.MODE_EAX)
    encrypted = cipher.encrypt_and_digest(encoded.encode('utf8'))
    print(base64.b64encode(encrypted).decode('utf8'))

    plaintext = cipher.decrypt_and_verify(base64.b64decode(
        b"P8HDNl54bLIUwi4syTgvM3TaCEqthZ2h+aie5H+omk/wjKnmagkYuKK9ArG4k+/Qhj5D+3i146Sil1cBBVktq3aJwtxkpv5XRX/YOWyeOc4=s"
    ))
    print(plaintext)
    #print(SplitLength)
    #print(key)

    last = 0
    out = False
    queue = []
    for i in range(0, len(key)):
        length = int(len(encoded) * SplitLength[key[i]])

        if i == len(key) - 1:
            length = len(encoded) - last

        if last + length > len(encoded):
            length = len(encoded) - last
            out = True

        queue.append((i,(last,length)))

        #print('Data %s' % encoded[last:last + length])
        last = last + length
        if out: break

    for X in queue:
        cursor = DBHosts[X[0]].cursor()
        sql = """
        INSERT INTO Test 
          (tag,data)
        VALUES 
          (%(tag)s, %(data)s)
        ON DUPLICATE KEY UPDATE
          tag  = values(tag),
          data = values(data) 
        """
        cursor.execute(sql, {
            'tag': tag,
            'data': encoded[X[1][0]:X[1][0]+X[1][1]]
        })
        DBHosts[X[0]].commit()
        DBHosts[X[0]].close()
        print({
            'tag': tag,
            'data': encoded[X[1][0]:X[1][0]+X[1][1]]
        })
        #print('  > MySQL' + str(X[0]) + ' Perform SQL: ' + sql)

    #print(encoded)
    # print(request.headers)
    # print(request.data)
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
