from pyCPNv27 import PyCPN
from pyEncodeDecode import stringEncode, stringDecode

# Tested with Python v 2.7.10 and CPN Tools v 4.0.1
# Server for use with pyCPNClient.py if not using the CPN model example

port = 9999
conn = PyCPN()
conn.accept(port)


def doit():
	while True:
		#msg = stringDecode(conn.receive())
		msg = conn.receive()
		if msg == 'quit':
			conn.disconnect()
			break
		else:
			print(msg)
			#conn.send(stringEncode('Hello, ' + msg))
			conn.send('Hello, ' + msg)

if __name__ == "__main__":
   doit()