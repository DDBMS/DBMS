DBGroups = [
    {
        "port": 3306,
        "host": '172.50.0.3',
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
    SplitLength[f.readline().split(' ')[0]] = float(f.readline().split(' ')[1])
