"""
@Infrastructure
  ↳   SSH-Keys    - SSH keys must be set from the         - Required  : (RSA-Key)
                  | - host --> client.
                  | - For testing purposes, add SSH
                  | - keys to and from localhost.
@Parameters
  ↳   Server      - The IP address or verified hostname   - Required  : (Command-Line)
                  | - of the target server hosting the
                  | - VPS. Defaults to localhost.
@Documentation
  [Note]    - When packaging the program, {script} may not work correct. The path relative
            - to its execution potentially could be the problem.
  [To-Do]   - Update @Parameters
"""
import textwrap
import mysql.connector

class Connection(object):
  def __init__(self, username:str, password:str, host:str , database:str):
    self.connection = mysql.connector.connect(
      user = username,
      passwd = password,
      host = host,
      database = database
    )
    self.network = "192.168.0."

  def disconnect(self):
    self.connection.close()

  def queryAll(self):
    cursor = self.connection.cursor()
    cursor.execute("SELECT * FROM DEVELOPMENT")
    query = cursor.fetchall()
    return query

  def incrementIP(self):
    data = self.queryAll()
    for row in data:
      last_row = row

    IP = last_row[4]
    # print("IP Address: " + IP)
    subnet = int(IP[10:])

    # print(subnet)
    return subnet + 1

  def addVPS(self, user:str, password:str, injection:str, ip:str, ram:int, cpu:int, domain:str, ssl:int, email:str):
    cursor = self.connection.cursor()
    command = ("INSERT INTO DEVELOPMENT "
              "(USERNAME, PASSWORD, INJECTION, IP, RAM, CPU, FQDN, CERTIFICATE, EMAIL) "
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

    data = (user, password, injection, ip, ram, cpu, domain, ssl, email)

    cursor.execute(command, data)
    self.connection.commit()