import network
import usocket
import gc



gc.collect()

s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr  =s.accept()
    request = conn.recv(1024)
    request = str(request)

