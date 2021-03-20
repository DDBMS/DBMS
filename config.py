#  Copyright (c) 2021. DBMS

DBGroups = [
    {
        "port": 3307,
        "host": '192.168.4.200',
        "user": "root",
        "password": "root_toor",
        "db": "my_db",
        "charset": "utf8"
    },
    {
        "port": 3308,
        "host": '192.168.4.200',
        "user": "root",
        "password": "root_toor",
        "db": "my_db",
        "charset": "utf8"
    },
    {
        "port": 3309,
        "host": '192.168.4.200',
        "user": "root",
        "password": "root_toor",
        "db": "my_db",
        "charset": "utf8"
    }
]
SplitLength = {}
with open('slen.conf', 'r') as f:
    lines = f.readlines()
    for line in lines:
        SplitLength[line.split(' ')[0]] = float(line.split(' ')[1])

FixedLength = 1.5