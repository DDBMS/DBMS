
#  Copyright (c) 2021. DBMS

from Crypto.Hash import SHA1
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Utils.Padding import random_rpad
import base64
salt = b'\xd0\x18\xa7QM\xd6\x9b\xebxu\xe4\xed\xa8\x83\xf6\xa3/\x01\x9c\x9e\x86n\xda;\x10EdD\xf7\x932\xcc'


def encrypt(key, data, db_num):
    # 將資料用base64編碼
    data_b64 = base64.b64encode(data)

    # 產生 Mapping Key
    h = SHA1.new()
    h.update(key.encode('utf-8'))
    map_key = h.hexdigest()[0:db_num]

    # 產生 加密 Key
    encrypt_key = PBKDF2(key, salt, dkLen=32)

    # 加密
    cipher = AES.new(encrypt_key, AES.MODE_CFB)
    cipher_b64 = base64.b64encode(cipher.encrypt(data_b64))

    iv_b64 = base64.b64encode(cipher.iv)

    return map_key, data_b64, iv_b64, cipher_b64


def decrypt(key, cipher_data, iv, db_num):
    # 產生 加密 Key
    encrypt_key = PBKDF2(key, salt, dkLen=32)

    cipher = AES.new(encrypt_key, AES.MODE_CFB, iv=base64.b64decode(iv))

    decrypted = cipher.decrypt(base64.b64decode(cipher_data))
    print(decrypted)
    return decrypted
