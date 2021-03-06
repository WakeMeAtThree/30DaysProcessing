#ifdef GL_ES
precision mediump float;
#endif

#define PROCESSING_COLOR_SHADER

uniform vec2 u_resolution;
uniform vec3 u_mouse;
uniform float u_time;

float Circle(vec2 uv, vec2 p, float r, float blur){
    /*Function that creates a circle given 
    (u, v) coordinates, (x,y) position, radius,
    and blur 
    */
    float d = length(uv-p);
    float c = smoothstep(r,r-0.01,d);
    return c;
}

float Smiley(vec2 uv, vec2 p, float size){
    uv -= p;
    uv /= size;
    float mask = Circle(uv, vec2(0.), .4, .05);

    mask -= Circle(uv, vec2(-.13,.1), .07, .01);
    mask -= Circle(uv, vec2(.13,.1), .07, .01);
    
    float mouth = Circle(uv, vec2(0.0,0.0), .3, .02);
    mouth -= Circle(uv, vec2(0.0,0.1), .3, .02);
    
    mask -= max(0.0,mouth);
    return mask;
}

float Band(float t, float start, float end, float blur){
    float step1 = smoothstep(start-blur,start+blur,t);
    float step2 = smoothstep(end+blur,end-blur,t);
    return step1*step2;
}

float Rect(vec2 uv,float left, float right, float bottom, float top,float blur){
    float band1 = Band(uv.x,left,right,blur);
    float band2 = Band(uv.y,bottom,top,blur);
    
    return band1*band2;
}
float norm(float t, float a, float b){
    return (t-a)/(b-a);
}
float remap(float t, float a, float b, float c, float d){
    return norm(t, a, b) * (d-c) + c;
}

void main() {
    vec2 uv = gl_FragCoord.st/u_resolution;
    
    //Move origin to center of canvas
    uv -= .5;

    //Un-stretchify canvas
    uv.x *= u_resolution.x/u_resolution.y;
    
    vec3 col = vec3(0.);
    float mask = 0.0;
    //Smiley(uv, vec2(0.,0.1), 0.45);

    //mask = smoothstep(-.2,.2,uv.x);
    //mask *= smoothstep(.2,-.2,uv.x);
    //mask = Band(uv.x, -.2,.2,.01);
    
    float x = uv.x;
    
    //Bending around a parabola
    //float m = -(x-.5)*(x+.5);
    //m = m*m*4.;
    float t = u_time;
    float m = 0.2*sin(t+x*8.);
    float y = uv.y-m;
    
    //x += y*-2;
    float blur = remap(x,-.5,.5,.01,.25);;
    //blur *= blur;
    blur = pow(blur*4.,3.);
    
    mask = Rect(vec2(x,y), -0.5, 0.5, -.1,.1,blur);
    //mask = Rect(vec2(x,y), -.2+y*.2, .2-y*.3, -.3,.3,.01);
    

    col = vec3(1.,1.,1.) * mask;

    gl_FragColor = vec4(col,1.0);
}