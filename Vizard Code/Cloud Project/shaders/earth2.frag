uniform sampler2D surfaceTexture;
uniform vec3 sunLocation;
uniform float earthRotation;
varying vec3 vLight;
varying vec3 vNormal;
varying vec2 vUv;

void main() {
        // Textures for day and night:
        vec2 vUv2 = vec2(vUv.x + earthRotation,vUv.y); //tried putting this in vertex shader, got artifacts at edge wraparound.
        vec4 dayColor = texture2D( surfaceTexture, vUv2 ).rgba;

        // compute cosine sun to normal so -1 is away from sun and +1 is toward sun.
        float cosineAngleSunToNormal = dot(normalize(vNormal), vLight);


        // sharpen the edge beween the transition.
        cosineAngleSunToNormal = clamp( cosineAngleSunToNormal * 6.0, -1.0, 1.0);

        // convert to 0 to 1 for mixing.
        float darkFactor = clamp(cosineAngleSunToNormal * 0.5 + 0.48, 0.0, 1.0);

        // Select day or night texture based on mixAmount.
        vec3 color = vec3(dayColor.r, dayColor.g, dayColor.b) * darkFactor;
        
        //Filter clouds from background
        float background_threshold = 60f/255f;
        float alpha = dayColor.a;
        if (dayColor.r <= background_threshold) {
            alpha = 0f;
        }
        
        // Set the color
        gl_FragColor = vec4(color, alpha);
}