import pymysql
from config import DBGroups


def migrate():
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
          tag varchar(36),
          data longtext,
          PRIMARY KEY (tag)
        )
        """
        cursor_object.execute(sql_query)
        print('  > MySQL Perform SQL: ' + sql_query)

    return 'wow!!'