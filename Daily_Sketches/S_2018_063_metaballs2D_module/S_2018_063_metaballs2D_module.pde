/*
Implementation of metaballs and marching squares algorithm using
the wonderful article written by Jamie Wong as a reference:
http://jamie-wong.com/2014/08/19/metaballs-and-marching-squares/

- finish color interpolation

*/

ArrayList<Ball> balls;
Grid someGrid;
float a = 0;

void setup() {
  size(400, 400,P2D);
  smooth(8);
  clear();
  //blendMode(DIFFERENCE);
  balls = new ArrayList<Ball>();
  someGrid = new Grid(75,75, balls);
  balls.add(new Ball(new PVector(259.314,302.736,0), new PVector(width/2,height/2,0)));
  balls.add(new Ball(new PVector(318.629,200,0), new PVector(width/2,height/2,0)));
  balls.add(new Ball(new PVector(259.314,97.2645,0), new PVector(width/2,height/2,0)));
  balls.add(new Ball(new PVector(140.686,97.2645,0), new PVector(width/2,height/2,0)));
  balls.add(new Ball(new PVector(140.686,302.736,0), new PVector(width/2,height/2,0)));
  balls.add(new Ball(new PVector(81.3713,200,0), new PVector(width/2,height/2,0)));
}

void draw() {
  clear();
  background(255);
  someGrid.display();
  //someGrid.displayCorners();
  for (int i = 0; i < balls.size(); i++) {
    float param = 0.0 * i/balls.size();
    balls.get(i).run(i+1);
  }
  //saveFrame("output/animation###.png");
  a+=0.02;
  if(a >= TWO_PI) exit();
  
}

// Set of ease functions below borrowed from Dave Whyte's sketches
// who's awesome enough to share it.

float ease(float p) {
  return 3*p*p - 2*p*p*p;
}

float ease(float p, float g) {
  if (p < 0.5) 
    return 0.5 * pow(2*p, g);
  else
    return 1 - 0.5 * pow(2*(1 - p), g);
}

float cs(float q) {
  return lerp(-1, 1, ease(map(cos(q), -1, 1, 0, 1), 5));
}
