from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import sqlite3
import jwt
from datetime import datetime, timedelta
 
conn = sqlite3.connect('bank_clients.db')
cursor = conn.cursor()
key='secret'
 
cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
id INT PRIMARY KEY,
full_name TEXT,
password TEXT,
account_number TEXT,
token TEXT)
  """)

conn.commit()
 
users = cursor.execute("SELECT * FROM Users")
 
if (len(users.fetchall()) == 0):
    user = [('1', 'Tataru Bogdan', 'xcv1', '1234', ''), ('2', 'Lupu Minodora', 'xcv2', '12345', ''), ('3', 'Vasile Mioara', 'xcv3', '123456', '')]
    cursor.executemany("INSERT INTO Users VALUES (?, ?, ?, ?, ?)", user)
    conn.commit()  
 



 
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        
        self.log_message("Incoming GET request...")
        
        token = parse_qs(self.path[2:])['token'][0]
        if(self.checkToken(token) == False):
            self.send_response_to_client(200, "Token not valid")
            return
        while True:
            pass
        
    def do_POST(self):
        self.log_message('Incoming POST request...')
        data_passed = parse_qs(self.path[2:])
 
        try:
            data = cursor.execute("SELECT %s FROM Users WHERE %s=? and %s=?" %
                                   ("account_number", "account_number", 'password'), (data_passed['account_number'][0], data_passed['password'][0]))
           
            if(len(data.fetchall()) == 0):
                        self.send_response_to_client(400, 'Invalid login')
            else:
                encoded = jwt.encode({'account_number': data_passed['account_number'][0], 'exp': datetime.utcnow() + timedelta(seconds=45)}, key, algorithm='HS256')
                self.send_response_to_client(200, 'Token (valid for 45 sec): {}'.format(encoded.decode("utf-8")))      
                cursor.execute("UPDATE Users SET %s=? WHERE %s=?" % ("token", "account_number"), (encoded, data_passed['account_number'][0]))
                conn.commit()
        except KeyError:
            self.send_response_to_client(404, 'Incorrect parameters provided')
            self.log_message("Incorrect parameters provided")
 
    def send_response_to_client(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(str(data).encode())
        
 
    def checkToken(self, token):
        try:
            payload = jwt.decode(token, key)
        except:
            return False
 
server_address = ('127.0.0.1', 8000)
http_server = HTTPServer(server_address, RequestHandler)
http_server.serve_forever()
