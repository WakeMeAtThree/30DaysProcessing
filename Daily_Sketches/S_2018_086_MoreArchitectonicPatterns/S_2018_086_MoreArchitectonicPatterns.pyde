#make bias an input
#Issue 3: Decide on a universal animated noise standard 
#Issue 4: Flat rendering shadows
#Issue 5: Silhouette outlines
#Issue 6: Static Icons below with percentages
#Issue 7: distribution of modules based on probability
#or based on max_counts (or both)
import os

a = 0
scl = 5
X = 5
Y = 5
radius = 1

def setup():
    global M,data,B,toon,matrices
    
    #Display settings
    size(400,400,P3D)
    smooth(8)
    #blendMode(EXCLUSION)
    ellipseMode(CORNER)
    shapeMode(CORNER)
    ortho()
    toon = loadShader("ToonFrag.glsl", "ToonVert.glsl")
    
    #Dataloading obj files
    data = [setPShape(loadShape(i)) for i in os.listdir("data") if i.endswith(".obj")]
    data[0].setFill(color(255,0,0))
    stroke(255,50)
    #noStroke()
    #biases = [int(map(sin(i/len(data)),-1,1,0,5)) for i in range(len(data))[::-1]]
    biases = [1 for i in range(len(data))[::-1]]
    #M = Matrix(X,Y,0.0,biases)
    #B = Matrix(3,Y,0.95,biases)
    matrices = [Matrix(X,Y,random(0.96),biases) for i in range(16)]
    #M.biases = [1,1,1,1]
    

def draw():
    global a,M,Ushape
    background(0)
    count = 0

    #dirY = (239 / float(self.height) - 0.5) * 2
    #dirX = (67 / float(self.width) - 0.5) * 2
    
    option = PVector(137, 92)
    #option = PVector(mouseX, mouseY)
    dirY = (option.y / float(height) - 0.5) * 2
    dirX = (option.x / float(width) - 0.5) * 2
    
    directionalLight(204, 204, 204, -dirX, -dirY, -1)
    shader(toon)
    #directionalLight(255, 255, 255, -1, 0, 0);
    #Coordinate transformations
    if(mousePressed): print(mouseX,mouseY)
    translate(45+9+8,height+37-240)
    
    scale(0.5)
    rotateZ(-PI/2)
    
    #Applying custom shear Matrix
    with pushMatrix():
        applyMatrix(  
        1.0, 0.0, 1.0,  0.0,
        0.0, 1.0, 0.0,  0.0,
        0.0, 0.0, 1.0,  0.0,
        0.0, 0.0, 0.0,  1.0);
        
        rotateZ(PI/4)
        #M.displayH()
        #M.displayV()
        #M.displayU()
        #translate(0,0,50)
        #B.displayU()
        #B.displayU()
        #M.display()
        count = 0
        for i in matrices:
            with pushMatrix():
                translate(0,0,-count)
                fill(255,0,0)
                i.displayU(a+1.0*count/50)
                #i.displayH()
                count += 30
    
    #Animate
    a += 0.006
    #if(a >= 1.0): exit()
    #saveFrame("output7/animation###.png")

class Matrix(object):
    def __init__(self, X, Y, chance, biases):
        #coloroptions = [color(225,0,0),color(225,128,0),color(0,50,230),color(255,255,255)]
        self.X = X
        self.Y = Y
        
        self.width = 400
        self.height = 400
        
        self.modules = data
        
        self.biases = biases
        self.modules = bias(self.modules,self.biases)
        self.modules = shuffle(self.modules)
        self.choices = [[floor(random(len(self.modules))) for j in range(X)] for i in range(Y)]
        
        #Cancel a module given some chance threshold
        self.canceled = [[1 if random(1)>=chance else 0 for j in range(X)] for i in range(Y)]
        
    def module(self,someShape,X,Y,W,H):
        #DEFUNCT, USE DATA LOADER ABOVE
        """This function is where you'll keep your module. Keep in mind that this is
        considering the display in CORNER mode.
        """
        global Ushape
        
        if(W != 0):
            shape(someShape,X,Y,W,H)
            #shape(anotherShape,X,Y,W,H)
            #shape(sides,X,Y,W,H)
    def getMatrix(self):
        """This is where Matrix is dynamically updated"""
        #Choice of using sin and cos vs sin and cos
        #return [[0 if not self.canceled[i][j] else noise(scl*i+radius*cos(TWO_PI*a),scl*j+radius*sin(TWO_PI*a)) for j in range(self.X)] for i in range(self.Y)]
        return [[0 if not self.canceled[i][j] else sin(a+0.25)+sin(1.26*a+1.26) for j in range(self.X)] for i in range(self.Y)]
    def displayH(self):
        """Equal spaced Y, dynamic X"""
        Matrix = self.getMatrix()
        Matrix = [normalizeList(i,self.width) for i in Matrix]
        shiftY = 0
        spaceY = 1.0*self.height/Y
        param = [0,0]
        for row in Matrix:
            shiftX = 0
            param[0] = 0
            for i in row:
                with pushMatrix():
                    scale(1,1,255*noise(scl*param[1]+cos(TWO_PI*a),scl*param[0]+sin(TWO_PI*a)))
                    #self.module(shiftX,shiftY,i,spaceY)
                    #scale(1,1,255*noise(radius*cos(TWO_PI*a)+sum(param)))
                    if(i > 0): self.module(self.modules[self.choices[param[1]][param[0]]],shiftX,shiftY,i,spaceY)
                shiftX += i
                param[0]+=1
            shiftY += spaceY
            param[1]+=1
    def displayV(self):
        """Equal spaced X, dynamic Y"""
        Matrix = self.getMatrix()
        Matrix = [normalizeList(i,self.height) for i in Matrix]
        shiftX = 0
        spaceX = 1.0*self.width/X
        param = [0,0]
        for row in Matrix:
            shiftY = 0
            param[0] = 0
            for i in row:
                with pushMatrix():
                    #scale(1,1,555*noise(scl*param[0]+cos(TWO_PI*a),scl*param[1]+sin(TWO_PI*a)))
                    scale(1,1,255*noise(radius*cos(TWO_PI*a)+sum(param)))

                    if(i > 0): self.module(self.modules[self.choices[param[1]][param[0]]],shiftX,shiftY,spaceX,i)
                shiftY += i
                param[0]+=1
            shiftX += spaceX
            param[1]+=1
    def displayU(self, a):
        """Unequal spaced Y, dynamic X"""
        Matrix = self.getMatrix()
        Matrix = [normalizeList(i,self.width) for i in Matrix]
        shiftY = 0
        spaceY = [noise(scl*i+radius*sin(TWO_PI*a)+25334) for i in range(Y)]
        spaceY = normalizeList(spaceY,self.height)
        param = [0,0]
        stretch = False
        for row in Matrix:
            shiftX = 0
            val = spaceY.pop(0)
            param[0] = 0
            for i in row:
                with pushMatrix():
                    #scale(1,1,100*noise(radius*cos(TWO_PI*a)+sum(param)))
                    #scale(1,1,100*noise(cos(TWO_PI*a)+sum(param)))
                    scale(1,1,100*noise(scl*param[0]+cos(TWO_PI*a),scl*param[1]+sin(TWO_PI*a)))
                    if(not stretch): self.module(self.modules[self.choices[param[1]][param[0]]],shiftX,shiftY,i,val)
                shiftX += i
                param[0]+=1
            shiftY += val
            param[1]+=1
    def display(self):
        """Dynamic Y, dynamic X"""
        Matrix = self.getMatrix()
        Matrix = [normalizeList(i,self.width) for i in Matrix]
        shiftY = 0
        spaceY = [[noise(scl*i+cos(TWO_PI*a)+25334,scl*j+radius*sin(TWO_PI*a)+25334) for j in range(X)] for i in range(Y)]
        spaceY = [normalizeList(row,self.height) for row in spaceY]
        shiftY = [0 for i in range(X)]
        param = [0,0]
        for row in Matrix:
            shiftX = 0
            someValues = spaceY.pop(0)
            
            count = 0
            param[0] = 0
            for j,i in zip(shiftY,row):
                val = someValues.pop(0)
                with pushMatrix():
                    scale(1,1,255*noise(radius*cos(TWO_PI*a)+sum(param)))
                    self.module(self.modules[self.choices[param[1]][param[0]]],shiftX,j,i,i)                
                shiftX += val
                shiftY[count] += i
                count+=1
                param[0]+=1
            param[1]+=1

def noiseFunc():
    pass
    
############

def normalizeList(alist,multiply): return [1.0*multiply*i/(sum(alist)+0.0001) for i in alist]

def bias(modules, multiples):
    output = []
    for i,j in zip(modules,multiples):
        output+=[i]*j
    return output

def shuffle(alist):
    jumble = alist
    for i,letter in enumerate(jumble):
        r = int(random(i))
        jumble[i],jumble[r] = jumble[r],jumble[i]
    return jumble

def keyPressed():
    frameCount = -1;
##########

def setPShape(someShape):
    someShape.disableStyle()
    someShape.setStrokeWeight(5)
    someShape.setFill(color(230))
    return someShape

def ease(p): return 3*p*p - 2*p*p*p;

def ease(p, g):
    if (p < 0.5): 
        return 0.5 * pow(2*p, g);
    else:
        return 1 - 0.5 * pow(2*(1 - p), g);

def sn(q): return lerp(-1, 1, ease(map(sin(q), -1, 1, 0, 1), 5))
def cs(q): return lerp(-1, 1, ease(map(cos(q), -1, 1, 0, 1), 5))
