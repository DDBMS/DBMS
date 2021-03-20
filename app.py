import argparse
import sys
from random import uniform

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
import Migration

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./"
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 16MB

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


# 實驗對照組
@app.route('/file/upload2', methods=['POST'])
def upload2():
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
    AccessData.another_save(
        tag=tag,
        hosts=db_hosts,
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
    iv
    tag
    key
    len
    """

    # Database Integration
    db_hosts = AccessData.connect()

    # HTTP Request Params
    tag = request.form.get('tag')
    key = request.form.get('key')
    iv = request.form.get('iv').encode('utf8')
    data_length = int(request.form.get('len'))

    # 讀取資料
    cipher = AccessData.read(
        tag=tag,
        hosts=db_hosts,
        key=key,
        data_length=data_length
    )  # 取得加密資料

    # 處理並加密資料
    eaten = EatData.decrypt(
        key=key,
        db_num=len(db_hosts),
        iv=iv,
        cipher_data=cipher.encode('utf8')
    )

    return jsonify({
        'status': True,
        'tag': tag,
        'data': eaten.decode('utf8')
    })


def gen_slen():
    with open('slen.conf','w+') as f:
        arr = ['a', 'b', 'c', 'd', 'e', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for c in arr:
            f.write('{} {:.2f}\n'.format(c, uniform(0.1, 0.7)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("mode",
                        help="Generate the SplitLength config",
                        choices=['gen','serve','migrate'])
    parser.add_argument("--host", help="Server host", nargs = '*',default='0.0.0.0',type=str)
    args = parser.parse_args()
    if args.mode:
        if args.mode == 'gen':
            gen_slen()
            print("generate!")
        elif args.mode == 'serve':
            app.run(host=args.host, debug=True, port=10022)
        elif args.mode == 'migrate':
            Migration.migrate()
            print("Migrated!")

