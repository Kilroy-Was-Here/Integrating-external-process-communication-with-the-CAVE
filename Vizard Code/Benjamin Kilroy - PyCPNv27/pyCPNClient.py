from pyCPNv27 import PyCPN

# Tested with Python v 2.7.10 and CPN Tools v 4.0.1
# For use with HelloNameCPNComm.cpn example net

port = 10101
host = 'localhost'
conn = PyCPN()
conn.connect(host, port)

def str2int(i):
	if i[0] == "(":
		return -int(i[2:(len(i)-1)])
	else:
		return int(i)

def doit():
	while True:
		resp = raw_input("Type your name or type quit: ") # v2.7 raw_input vs input
		#conn.send(stringEncode(resp))
		conn.send(resp)
		if resp == 'quit':
			conn.disconnect()
			break
		else:
			#msg = stringDecode(conn.receive())
			msg = conn.receive()
			print(tuple(map(str2int, msg.split(':'))))	

if __name__ == "__main__":
   doit()