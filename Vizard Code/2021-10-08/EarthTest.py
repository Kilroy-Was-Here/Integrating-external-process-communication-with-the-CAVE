import viz
import vizact
import vizshape
import vizinfo
import viztracker
import math
import os
from PIL import Image

viz.setMultiSample(6)
viz.fov(60)

viz.clearcolor(viz.BLACK)

os.system("curl -u XP100-YRB7N-GEGFX-F8ULN:C6pzHQtNz5Pc -L -o clouds-8192.jpg https://secure.xericdesign.com/xplanet/clouds/8192/clouds-8192.jpg")

img = Image.open("C:\\Users\\benja\\Documents\\Vizard Code\\2021-10-08\\clouds-8192.jpg")
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    if item[0] <= 60 and item[1] <= 60 and item[2] <= 60:
        newData.append((item[0], item[1], item[2], 0))
    else:
        newData.append(item)

img.putdata(newData)
img.save("just-clouds.png", "PNG")

def IsThisVillanovaCAVE():
	cave_host_names = ["exx-PC","render-PC"]
	import socket
	if socket.gethostname() in cave_host_names:
		return True
	else:
		return False

if IsThisVillanovaCAVE():
    #Cave specific set-up
    import vizconnect
    CONFIG_FILE = "E:\\VizardProjects\\_CaveConfigFiles\\vizconnect_config_CaveFloor+ART_headnode.py"
    vizconnect.go(CONFIG_FILE)
    
    #Selected this view from experimenting in the CAVE.
    viewMatrix = [ 0.562127, 0.000000, -0.827051, 0.000000,
                    0.000000, 1.000000, -0.000000, 0.000000,
                    0.827051, -0.000000, 0.562127, 0.000000,
                    8.234159, -1.438034, -3.980055, 1.000000 ]
                  
    vizconnect.getTransport('wandmagiccarpet').getNode3d().setMatrix(viewMatrix)
    
else:
    #Local PC pecific set-up    
    viz.go()
    
    viz.MainView.setPosition((15,0,0))
    
    viewOfEarthMatrix = [ 0.912075, 0.058685, -0.405802, 0.000000,
                          -0.124867, 0.982449, -0.138574, 0.000000,
                          0.390547, 0.177061, 0.903395, 0.000000,
                          8.967296, -0.270925, -2.598568, 1.000000 ]
    
    #View closer to the change from light to dark                      
    viewOfEarthMatrix2 = [ 0.899875, -0.103062, -0.423795, 0.000000,
  -0.125831, 0.869012, -0.478523, 0.000000,
  0.417600, 0.483938, 0.769035, 0.000000,
  9.325228, -0.866960, -1.573088, 1.000000 ]

    viz.MainView.setMatrix(viewOfEarthMatrix2)


MOVE_SPEED=10

#sky = viz.add(viz.ENVIRONMENT_MAP, 'TychoSkymap.tif') #starry background
#skybox = viz.add('skydome.dlc')
#skybox.texture(sky)

earthVertCode=None
with open ("shaders/earth.vert", "r") as file:
    earthVertCode = file.read()
    

earthFragCode=None
with open ("shaders/earth.frag", "r") as file:
    earthFragCode = file.read()
    
cloudFragCode=None
with open ("shaders/earth2.frag", "r") as file:
    cloudFragCode = file.read()


earthCloudsTexture = viz.addTexture('C:\\Users\\benja\\Documents\\Vizard Code\\2021-10-08\\just-clouds.png')
earthDayTexture = viz.addTexture('images/8k_earth_daymap.jpg')
earthDayTexture.wrap(viz.WRAP_S,viz.REPEAT)
earthNightTexture = viz.addTexture('images/8k_earth_nightmap.jpg')
earthNightTexture.wrap(viz.WRAP_S,viz.REPEAT)
earthSpecularTexture = viz.addTexture('images/8k_earth_specular_map.png')
earthSpecularTexture.wrap(viz.WRAP_S,viz.REPEAT)
earth = vizshape.addSphere(radius=1.0,slices=80,stacks=80, pos=(10,0,0))
earth.setEuler(0,-23.4,0)


earth.texture(earthDayTexture)
earth.texture(earthNightTexture,unit=1)
earth.texture(earthSpecularTexture,unit=2)
earthShader = viz.addShader(vert=earthVertCode, frag=earthFragCode)
earth.apply(earthShader)
earth.apply(viz.addUniformInt('dayTexture',0))
earth.apply(viz.addUniformInt('nightTexture',1))
earth.apply(viz.addUniformInt('specularTexture',2))
earth.apply(viz.addUniformFloat('sunLocation',3))
earth.apply(viz.addUniformFloat('earthRotation',4))
earth.apply(viz.addUniformFloat('camLocation',5))
earth.setUniformFloat('sunLocation',(300.0,0.0,0.0))
earth.setUniformFloat('earthRotation',earth.getEuler()[0]) #yaw (rotation around y-axis) is first element
earth.setUniformFloat('camLocation',viz.MainView.getPosition(viz.REL_GLOBAL))


earth2 = vizshape.addSphere(radius=0.98,slices=80,stacks=80,pos=(10,0,0))
earthClouds2 = vizshape.addSphere(radius=0.96,slices=80,stacks=80,pos=(10,0,0))
earth2.addAction( vizact.spin(0,-1,0,5) )
earthClouds2.addAction( vizact.spin(0,-1,0,5.4) )


earthClouds = vizshape.addSphere(radius=1.005,slices=80,stacks=80,pos=(10,0,0))
earthClouds.setEuler(0,-23.4,0)
earthClouds.texture(earthCloudsTexture)
earthCloudsTexture.wrap(viz.WRAP_S,viz.REPEAT)
cloudShader= viz.addShader(vert=earthVertCode,frag=cloudFragCode)
earthClouds.apply(cloudShader)
earthClouds.apply(viz.addUniformInt('surfaceTexture',0))
earthClouds.apply(viz.addUniformFloat('sunLocation',1))
earthClouds.apply(viz.addUniformFloat('earthRotation',2))
earthClouds.setUniformFloat('sunLocation',(300.0,0.0,0.0))
earthClouds.setUniformFloat('earthRotation',earthClouds2.getEuler()[0])



#earth.addAction( vizact.spin(0,-1,0,5) )
#earthClouds.addAction( vizact.spin(0,-1,0,5.05))


sunTexture= viz.addTexture('images/Sun_2.jpg')
sun= vizshape.addSphere(radius=173, slices=40, stacks=40, pos=(300,0,0))
sun.texture(sunTexture)
sun.addAction( vizact.spin(0,-1,0,0.5) )
sunlight = viz.addLight()
sunlight.position(300,0,-700)
sunlight.spread(180)
sunlight.intensity(0.4)
sunlight.color(viz.WHITE)
sun.disable(viz.LIGHTING)




def updateView():
    earth.setUniformFloat('earthRotation',(earth2.getEuler()[0]+180.0)/360.0)
    earthClouds.setUniformFloat('earthRotation',(earthClouds2.getEuler()[0]+180.0)/360.0)
    earth.setUniformFloat('camLocation',viz.MainView.getPosition(viz.REL_GLOBAL))
    if viz.key.isDown(viz.KEY_UP):
        viz.MainView.move([0,0,MOVE_SPEED*viz.elapsed()],viz.BODY_ORI)
    elif viz.key.isDown(viz.KEY_DOWN):
        viz.MainView.move([0,0,-MOVE_SPEED*viz.elapsed()],viz.BODY_ORI)
    elif viz.key.isDown(viz.KEY_LEFT):
        viz.MainView.move([-MOVE_SPEED*viz.elapsed(),0,0],viz.BODY_ORI)
    elif viz.key.isDown(viz.KEY_RIGHT):
        viz.MainView.move([MOVE_SPEED*viz.elapsed(),0,0],viz.BODY_ORI)	
    elif viz.key.isDown('w'):
        viz.MainView.move([0,MOVE_SPEED*viz.elapsed(),0],viz.BODY_ORI)
    elif viz.key.isDown('s'):
        viz.MainView.move([0,-MOVE_SPEED*viz.elapsed(),0],viz.BODY_ORI)		
        
vizact.ontimer(0,updateView)
