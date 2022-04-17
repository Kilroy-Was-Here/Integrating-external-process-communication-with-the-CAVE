uniform sampler2D dayTexture;
uniform sampler2D nightTexture;
uniform sampler2D specularTexture;
uniform vec3 sunLocation;
uniform float earthRotation;
uniform vec3 camLocation;
varying vec3 vNormal;
varying vec3 vLight;
varying vec3 vCamera;
varying vec2 vUv;

void main() {
        // Textures for day and night:
                vec2 vUv2 = vec2(vUv.x + earthRotation,vUv.y); //tried putting this in vertex shader, got artifacts at edge wraparound.
                                                               //also, needed to specify WRAP attribute in Python for all the pertinent textures.
        vec3 dayColor       = texture2D( dayTexture, vUv2 ).rgb;
        vec3 nightColor     = texture2D( nightTexture, vUv2 ).rgb;

        // // compute cosine sun to normal so -1 is away from sun and +1 is toward sun.
        float cosineAngleSunToNormal = dot(normalize(vLight),vNormal);
                float cosineAngleCamToNormal = dot(normalize(vCamera),vNormal);
                float sineAngleCamToNormal = 1.0 - pow(cosineAngleCamToNormal,2.0);

        // sharpen the edge beween the transition.
        cosineAngleSunToNormal = clamp( cosineAngleSunToNormal * 10.0, -1.0, 1.0);

        // convert to 0 to 1 for mixing.
        float mixAmount = (cosineAngleSunToNormal * 0.5) + 0.5;
        float mixAmount2 = (sineAngleCamToNormal * 0.5) + 0.5;
                
        //         //atmosphere effect.
        vec3 atmosphereColor = vec3(0.0,0.7,0.8);
        float intensity = 1.09 - mixAmount2;
        vec3 AtmosphereDay = atmosphereColor * pow(intensity,2.0);
        vec3 AtmosphereNight = atmosphereColor * pow(mixAmount,0.5);

        // Specular:s
        vec3 specularAmount = texture2D( specularTexture, vUv2 ).xyz;
        vec3 specularColor  = vec3(1.0,1.0,1.0);
        vec3 specular = specularColor * 0.5 * pow(dot(normalize(vLight),vNormal), 30.0) * specularAmount.z;

        if (isnan(specular.x) || isnan(specular.y) || isnan(specular.z)) {
                specular = vec3(0,0,0);
        }

        // Select day or night texture based on mixAmount.
        vec3 color = dayColor + specular + AtmosphereDay;

        nightColor = nightColor + AtmosphereNight;
        color = mix( nightColor, color, mixAmount );

        // Set the color
        gl_FragColor = vec4(color, 1.0);
        // gl_FragColor = vec4(1,0,0,1);
}