uniform sampler2D dayTexture;
uniform sampler2D nightTexture;
uniform sampler2D specularTexture;
uniform vec3 sunLocation; //already in World/Projection coordinates
uniform float earthRotation;
uniform vec3 camLocation;
varying vec3 vNormal;
varying vec3 vLight;
varying vec3 vCamera;
varying vec2 vUv;
attribute vec3 Tangent;

void main(void)
{
    //vec3 n = normalize(gl_NormalMatrix * gl_Normal);
    //vec3 t = normalize(gl_NormalMatrix * Tangent);
    //vec3 b = cross(n, t);
    
    vec4 tmpVertex = gl_ModelViewProjectionMatrix * vec4(gl_Vertex.x, gl_Vertex.y, gl_Vertex.z, 1.0);
    vec3 vVertex = vec3(tmpVertex.x, tmpVertex.y, tmpVertex.z);
    vec4 tmpSun = - vec4(sunLocation.x, sunLocation.y, sunLocation.z, 1.0);
    vec4 tmpCam = - gl_ModelViewProjectionMatrix * vec4(camLocation.x, camLocation.y, camLocation.z, 1.0);

    vLight = normalize(vVertex - vec3(tmpSun.x, tmpSun.y, tmpSun.z));
    vCamera = normalize(vVertex - vec3(tmpCam.x, tmpCam.y, tmpCam.z)); 
    
    vUv = gl_MultiTexCoord0.xy;

    vNormal = gl_Normal;
    
    gl_Position = ftransform(); //tmpVertex; //ftransform();
}