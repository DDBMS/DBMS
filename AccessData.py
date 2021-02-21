import pymysql
from Crypto.Hash import SHA1

from config import SplitLength, DBGroups


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
        print(tag)
        cursor.execute(sql, {
            'tag': tag,
            'data': data_ok[X[1][0]:X[1][0] + X[1][1]]
        })
        hosts[X[0]].commit()
        hosts[X[0]].close()
    print({
        'tag': tag,
        'data': data_ok[X[1][0]:X[1][0] + X[1][1]]
    })


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
            data += got['data']

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
