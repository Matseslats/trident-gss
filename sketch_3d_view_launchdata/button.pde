class Button {
  int xCoord, yCoord, w, h;
  String text, shape;
  color t, b, bo;
  int id;
  int textSize;
  Button(int x, int y, int _width, int _height, String _shape, String _text, int tz, color cT, color cB, color cBo, int identifier){
    text = _text;
    xCoord = x;
    yCoord = y;
    w = _width;
    h = _height;
    t = cT;
    b = cB;
    bo = cBo;
    id = identifier;
    shape = _shape;
    textSize = tz;
  }
  void display(){
    if(isOver()){
      fill(bo);
    } else {
      fill(b);
    }
    if(shape == "square"){
      rectMode(CENTER);
      rect(xCoord, yCoord, w, h, 10);
    } else if (shape == "triangle"){
      if(h<0){
        triangle(xCoord-w/2, yCoord+abs(h)/2, xCoord+w/2, yCoord+abs(h)/2, xCoord, yCoord-abs(h)/2);
      } else {
        triangle(xCoord-w/2, yCoord-h/2, xCoord+w/2, yCoord-h/2, xCoord, yCoord+h/2);
      }
    }
    fill(t);
    textAlign(CENTER, CENTER);
    textSize(textSize);
    text(text, xCoord, yCoord+(g.textSize*0.3));//+(g.textSize*0.3));
  }
  
  String[] getId(){
    String ret[] = {str(id), text};
    return ret;
  }
  
  boolean isOver(){
    return (mouseX > xCoord-(w/2) && mouseX < xCoord+(w/2) && mouseY > yCoord-(abs(h)/2) && mouseY < yCoord+(abs(h)/2));
  }
  void setColors(color _t, color _b, color _bo){
    t = _t;
    b = _b;
    bo = _bo;
  }
  void setText(String newText){
    text = newText;
  }
}
