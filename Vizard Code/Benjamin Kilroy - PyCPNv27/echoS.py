from pyCPNv27 import PyCPN

port = 9999
conn = PyCPN()
conn.accept(port)


def doit():
	msg = conn.receive()
	conn.send(msg)
	conn.disconnect()

if __name__ == "__main__":
   doit()