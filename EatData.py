from Crypto.Hash import SHA1
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from app import salt
import base64


def encrypt(key, data, db_num):
    # 將資料用base64編碼
    data_b64 = base64.b64encode(data)

    # 產生 Mapping Key
    h = SHA1.new()
    h.update(key.encode('utf-8'))
    map_key = h.hexdigest()[0:len(db_num)]

    # 產生 加密 Key
    encrypt_key = PBKDF2(key, salt, dkLen=32)

    # 加密
    cipher = AES.new(encrypt_key, AES.MODE_CFB)
    cipher_b64 = base64.b64encode(cipher.encrypt(data_b64))

    iv_b64 = base64.b64encode(cipher.iv)

    return map_key, data_b64, iv_b64, cipher_b64


def decrypt(key, data, db_num, iv):
    cipher = AES.new(encrypt_key, AES.MODE_CBC, iv=cipher.iv)
    plaintext = unpad(cipher.decrypt(base64.b64decode(base64.b64encode(cipher_data))), AES.block_size)
    print(plaintext)
