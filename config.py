DBGroups = [
    {
        "port": 3307,
        "host": '0.0.0.0',
        "user": "root",
        "password": "root_toor",
        "db": "my_db",
        "charset": "utf8"
    },
    {
        "port": 3306,
        "host": '172.49.0.3',
        "user": "root",
        "password": "root_toor",
        "db": "my_db",
        "charset": "utf8"
    },
    {
        "port": 3306,
        "host": '172.48.0.3',
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
