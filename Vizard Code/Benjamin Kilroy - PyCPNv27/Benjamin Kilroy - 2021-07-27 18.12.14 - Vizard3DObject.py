import viz
from pyCPNv27 import PyCPN
#from pyEncodeDecodev27 import stringEncode, stringDecode

# Tested with Python v 2.7.10 and CPN Tools v 4.0.1
# For use with HelloNameCPNComm.cpn example net

import vizconnect
CONFIG_FILE = "E:\\VizardProjects\\_CaveConfigFiles\\vizconnect_config_CaveFloor+ART_headnode.py"
vizconnect.go(CONFIG_FILE)

port = 10101
host = '192.168.1.5'

viz.setMultiSample(4)

# WIDTH = 0
# HEIGHT = 1
#
# CLUSTER_EXISTS = bool(viz.getOption("viz.cluster"))
#
# if CLUSTER_EXISTS:
#     CLUSTER_NUM_CLIENTS = int(viz.getOption("viz.cluster.clients"))
#     print("Number of Cluster Clients: %s" % CLUSTER_NUM_CLIENTS)
#
#     window_size = [300, 300]
#     #MONITOR_WIDTH = int(viz.getOption("viz.monitor.width"))
#     MONITOR_WIDTH = 1920
#     print("Monitor Width: %i" % MONITOR_WIDTH)
#     clients_per_row = MONITOR_WIDTH // window_size[WIDTH]
#     print("clients per row: %i" % clients_per_row)
#
#     clients = [viz.MASTER, viz.CLIENT1, viz.CLIENT2, viz.CLIENT3, viz.CLIENT4]
#
#     client_names = ["MASTER", "CLIENT1", "CLIENT2","CLIENT3", "CLIENT4"]
#     for i in range(CLUSTER_NUM_CLIENTS+1):
#         client = clients[i]
#         client_name = client_names[i]
#         row = int(i // clients_per_row)
#         col = i - (row * clients_per_row)
#         pos = [col * (window_size[WIDTH]+10), row * (window_size[HEIGHT]+30)]
#
#         print(client_name + ": " + str(pos))
#
#         with viz.cluster.MaskedContext(client):
#             w = viz.window
#             w.setName(client_name)
#             w.setSize(window_size)
#             w.setPosition(pos)

# viz.go()

viz.startLayer(viz.TRIANGLE_FAN)
viz.vertex(0,1,5) #All the triangles have the first vertex as a point.
viz.vertex(-1.5,1.35,10) #The other points are taken in pairs.
viz.vertex(-.25,1.5,10)
viz.vertex(0,.8,10)
viz.vertex(.25,1.5,10)
viz.vertex(1.5,1.35,10)
myTrianglefan = viz.endLayer()

thisLight = viz.addLight()
thisLight.enable()
thisLight.position(0,0,0)
thisLight.spread(180)
thisLight.intensity(2)

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
def Joystick():
	rawInput = vizconnect.getConfiguration().getRawDict("input")
	if rawInput['flystick'].isButtonDown(2):
		Flying()

#vizact.onkeydown('f',Flying)
vizact.onupdate(0, Joystick)