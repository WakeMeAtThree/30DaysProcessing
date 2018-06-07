class Meshes {
  ArrayList<Mesh> initials;
  ArrayList<Mesh> blends;
  ArrayList<Mesh> targets;
  Meshes(int n) {
    this.initials = new ArrayList<Mesh>();
    this.blends = new ArrayList<Mesh>();
    this.targets = new ArrayList<Mesh>();
    
    for (int i = 1; i <= n; i++) {
      this.initials.add(new Mesh(loadShape("initial"+i+".obj")));
      this.blends.add(new Mesh(loadShape("initial"+i+".obj")));
      this.targets.add(new Mesh(loadShape("target"+i+".obj")));
    }
  }
  
  void morph(float a){
    for(int i = 0; i < this.blends.size(); i++){
      float param = 50.0*i/this.blends.size();
      this.blends.get(i).morph(this.initials.get(i), this.targets.get(i), a+param);
    }
  }
  
  void display(float a){
    int count = 1;
    float alpha;
    for(Mesh m: this.blends){
      alpha = 0;
      if(count==1 || count==0) alpha = PI; 
      m.display(a,alpha);
      count++;
    }
  }
}
