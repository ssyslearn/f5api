#-*- coding: utf-8 -*-
#!/app/python2.7/bin/python
import subprocess
from MySQLdb as mydb



cmd = "mail -v -r 'dlatmdals99@gmail.com' -s 'test mail' -S smtp='localhost' dlatmdals99@gmail.com < test.mail"
o = subprocess.Popen(cmd, stderr=subprocess.STDOUT, shell=True)

print o.decode("utf-8")
