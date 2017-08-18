#-*- coding: utf-8 -*-
import subprocess
import MySQLdb
import _mysql_exceptions
from contextlib import contextmanager
import sys
import json

sys.path.append("/app/api-infra")
from info.L4info import L4info

@contextmanager
def db_connect():
    db_ip = L4info.get_db_ip()
    db_id = L4info.get_db_id()
    db_pw = L4info.get_db_pw()
    conn = MySQLdb.connect(host=db_ip, user=db_id, passwd=db_pw, db='TEST')
    cur = conn.cursor()

    try:
        yield (conn, cur)
    finally:
        cur.close()
        conn.close()

with db_connect() as (conn, cur):
    s = """ SELECT * FROM API """
    cur.execute(s)
    data = cur.fetchall()

print json.dumps(data)


cmd = "echo %s | mail -v -r 'dlatmdals99@gmail.com' -s 'test mail' -S smtp='localhost' dlatmdals99@gmail.com" % (json.dumps(data))
o = subprocess.Popen(cmd, stderr=subprocess.STDOUT, shell=True)
