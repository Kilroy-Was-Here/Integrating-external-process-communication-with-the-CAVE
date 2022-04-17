import viz
from pyCPNv27 import PyCPN

import vizconnect
CONFIG_FILE = "E:\\VizardProjects\\_CaveConfigFiles\\vizconnect_config_CaveFloor+ART_headnode.py"


#from pyEncodeDecodev27 import stringEncode, stringDecode

# Tested with Python v 2.7.10 and CPN Tools v 4.0.1
# For use with HelloNameCPNComm.cpn example net

port = 10101
host = ''

viz.setMultiSample(4)

#viz.go()


viz.startLayer(viz.TRIANGLE_FAN)
viz.vertex(0,1,5) #All the triangles have the first vertex as a point.
viz.vertex(-1.5,1.35,10) #The other points are taken in pairs.
viz.vertex(-.25,1.5,10)
viz.vertex(0,.8,10)
viz.vertex(.25,1.5,10)
viz.vertex(1.5,1.35,10)
myTrianglefan = viz.endLayer()

conn = PyCPN()
conn.connect(host, port)
ex = 0
ey = 0
ez = 0
es = 1
def str2int(i):
	if i[0] == "(":
		return -int(i[2:(len(i)-1)])
	else:
		return int(i)
vizconnect.go(CONFIG_FILE)
def doit():
	#resp = raw_input("Type your name or type quit: ") # v2.7 raw_input vs input
	#conn.send(stringEncode(resp))
	#conn.send(resp)
	#msg = stringDecode(conn.receive())
	msg = conn.receive()
	print(msg)
	global ex
	global ey
	global ez
	location = (tuple(map(str2int, msg.split(':'))))	
	ex = location[0]
	ey = location[1]
	ez = location[2]
	es = location[3]
	conn.disconnect()

if __name__ == "__main__":
   doit()
def Flying():
	flyToPoint = vizact.moveTo([ex, ey, ez],speed=es)
	myTrianglefan.addAction(flyToPoint)
vizact.onkeydown('f',Flying)