#  Copyright (c) 2021. DBMS

import pymysql
from Crypto.Hash import SHA1

from config import SplitLength, DBGroups, FixedLength
from Utils.Padding import random_rpad


def save(tag, hosts, key, cipher):
    data_ok = cipher.decode('utf8')
    last = 0
    out = False
    queue = []
    for i in range(0, len(key)):
        length = int(len(data_ok) * SplitLength[key[i]])

        if i == len(key) - 1:
            length = len(data_ok) - last

        if last + length > len(data_ok):
            length = len(data_ok) - last
            out = True

        queue.append((i, (last, length)))
        last = last + length
        if out: break

    for X in queue:
        """
        X : (第幾個DB, (起始index, 結束index))
        """
        cursor = hosts[X[0]].cursor()
        sql = """
        INSERT INTO Test 
          (tag,data)
        VALUES 
          (%(tag)s, %(data)s)
        ON DUPLICATE KEY UPDATE
          tag  = values(tag),
          data = values(data) 
        """

        to_save = data_ok[X[1][0]:X[1][0] + X[1][1]]
        print(f"""
        Origin Data: {to_save}
        """)
        to_save = random_rpad(to_save, int(len(to_save) * FixedLength))
        print(f"""
        Tag : {tag}
        Saved Data : {to_save}
        """)
        cursor.execute(sql, {
            'tag': tag,
            'data': to_save
        })
        hosts[X[0]].commit()

        sql = """
            INSERT INTO Test 
                (tag,data)
            VALUES 
                (%(tag)s, %(data)s)
            ON DUPLICATE KEY UPDATE
                tag  = values(tag),
                data = values(data) 
        """
        cursor = hosts[(X[0] + 1 + len(DBGroups)) % len(DBGroups)].cursor()
        cursor.execute(sql, {
            'tag': tag + '_bak_n',
            'data': to_save[int(len(to_save) * 0.5):len(to_save)]
        })
        hosts[(X[0] + 1 + len(DBGroups)) % len(DBGroups)].commit()

        sql = """
                    INSERT INTO Test 
                        (tag,data)
                    VALUES 
                        (%(tag)s, %(data)s)
                    ON DUPLICATE KEY UPDATE
                        tag  = values(tag),
                        data = values(data) 
                """
        cursor = hosts[(X[0] - 1 + len(DBGroups)) % len(DBGroups)].cursor()
        cursor.execute(sql, {
            'tag': tag + '_bak_p',
            'data': to_save[0:int(len(to_save) * 0.5)]
        })
        hosts[(X[0] - 1 + len(DBGroups)) % len(DBGroups)].commit()


def read(tag, hosts, key, data_length):
    # 產生 Mapping Key
    h = SHA1.new()
    h.update(key.encode('utf-8'))
    key = h.hexdigest()[0:len(hosts)]

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

        queue.append((i, (last, length)))

        last = last + length
        if out: break

    for X in queue:
        cursor = hosts[X[0]].cursor(pymysql.cursors.DictCursor)
        sql = """
        SELECT * from Test 
        where 
          tag = %(tag)s
        """
        cursor.execute(sql, {
            'tag': tag
        })
        got = cursor.fetchone()

        hosts[X[0]].commit()
        hosts[X[0]].close()

        if got:
            print(f"Origin Got: {got['data']}")
            print(f"Final  Got: {got['data'][0:X[1][1]]}")
            data += got['data'][0:X[1][1]]

    return data


def connect():
    db_hosts = []
    try:
        for host in DBGroups:
            print('  > MySQL Host: ' + host['host'])
            db_hosts.append(pymysql.connect(**host))
    except Exception as ex:
        print(ex)

    return db_hosts


def another_save(tag, hosts, cipher):
    data_ok = cipher.decode('utf8')
    cursor = hosts[0].cursor()
    sql = """
                INSERT INTO Test 
                  (tag,data)
                VALUES 
                  (%(tag)s, %(data)s)
                ON DUPLICATE KEY UPDATE
                  tag  = values(tag),
                  data = values(data) 
                """
    print(tag)
    cursor.execute(sql, {
        'tag': tag,
        'data': data_ok
    })
    hosts[0].commit()
    hosts[0].close()
    print({
        'tag': tag,
        'data': data_ok
    })
