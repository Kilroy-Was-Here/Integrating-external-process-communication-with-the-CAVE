from pyCPNv27 import PyCPN
from randstr import randStr

port = 9999
host = 'localhost'
conn = PyCPN()
conn.connect(host, port)

def doit():
	sent = randStr(5000)
	conn.send(sent)
	recd = conn.receive()
	print(sent == recd)
	print(len(sent))
	print(len(recd))		
	conn.disconnect()

if __name__ == "__main__":
   doit()