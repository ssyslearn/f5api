#-*- coding: utf-8 -*-
import MySQLdb
import _mysql_exceptions
from contextlib import contextmanager
import sys
import json
import smtplib
from email.mime.text import MIMEText

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

def sendmail(msg, subject, sender, to, smtp):
   msg = MIMEText(msg, 'html', 'utf-8')
   msg['Subject'] = subject
   msg['From'] = sender
   msg['To'] = ','.join(to)
   s = smtplib.SMTP(smtp)
   s.sendmail(sender, to, msg.as_string())
   s.quit()


if __name__ == '__main__':

   with db_connect() as (conn, cur):
       s = """ SELECT * FROM API """
       cur.execute(s)
       data = cur.fetchall()
   
   
   smtp_server = 'localhost'
   mailTo = ['dlatmdals99@gmail.com']
   mailFrom = 'dlatmdals99@gmail.com'
   
   email_str = '''
   <!DOCTYPE html>
   <html>
   <head>
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
      <style>
         table { border-collapse: collapse; }
         table, th, td { border: 1px solid black; }
         td { text-align: left; padding: 2px; }
      </style>
   </head>
   <body>
      <table>
         <thead>
         <tr>
            <th>Called API</th>
         </tr>
         </thead>
         <tbody>
   '''

   for i in data:
      email_str += '<tr>'
      email_str += '<td>' + str(i) + '</td>'
      email_str += '</tr>'
      
   email_str += '''
         </tbody>
      </table>
   </body>
   </html>
   '''
   
   #print email_str
   subject = 'test mail test'
   sendmail(email_str, subject, mailFrom, mailTo, smtp_server)
