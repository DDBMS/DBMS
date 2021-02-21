import pymysql
from config import SplitLength


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
        cursor.execute(sql, {
            'tag': tag,
            'data': data_ok[X[1][0]:X[1][0]+X[1][1]]
        })
        hosts[X[0]].commit()
        hosts[X[0]].close()
        print({
            'tag': tag,
            'data': data_ok[X[1][0]:X[1][0]+X[1][1]]
        })

