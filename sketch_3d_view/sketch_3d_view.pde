float rotX, rotY, rotZ, camX, camY, camZ;
import toxi.geom.*;
import toxi.geom.mesh.*;

import toxi.processing.*;
import de.fhpotsdam.unfolding.*;
import de.fhpotsdam.unfolding.geo.*;
import de.fhpotsdam.unfolding.utils.*;  
import de.fhpotsdam.unfolding.geo.Location;
import de.fhpotsdam.unfolding.marker.SimplePointMarker;
UnfoldingMap map;
Location andenesLocation = new Location(69.296889, 16.028693);
Location cansatLocation = new Location(69.26, 10.3);
SimplePointMarker andenesMarker = new SimplePointMarker(andenesLocation);
SimplePointMarker cansatMarker = new SimplePointMarker(cansatLocation);

import processing.video.*;
Movie   movie;

import processing.serial.*;
Serial myPort;  // Create object from Serial class
int val;      // Data received from the serial port

ToxiclibsSupport gfx;
TriangleMesh mesh;
float seed = 0;
PFont font;
float altitudes[] = new float[100];
float accelrations[] = new float[100];
int graphdelay = 20; // How many plot points to skip before drawing next point
int counter = 0;
int locpoint = 0;
ArrayList<Button> buttons;
boolean logging = false;
String filename = "";
boolean movieLoaded = false;
int connectiondelay = 100;
int connectioncounter = 0;
int lastReadTime = 0;
int lastSavedFrame;
String portName;

public void setup(){
    size(1920, 1080, P3D);
    //fullScreen(P3D);
    font = createFont("fonts/CascadiaCode-Bold.otf", 128);
    textFont(font, 32);
    mesh = (TriangleMesh) new STLReader().loadBinary(sketchPath("Arrow.stl"), STLReader.TRIANGLEMESH);
    gfx = new ToxiclibsSupport(this);
    map  = new UnfoldingMap(this, "overview", width-655, height-400, 655, 400);
    map.zoomAndPanTo(10, new Location(69.29f, 16.0f));
    map.addMarkers(andenesMarker, cansatMarker);
    cansatMarker.setColor(#FF7700);
    andenesMarker.setDiameter(10);
    MapUtils.createDefaultEventDispatcher(this, map);
    lat = 16.028693;
    lon = 69.296889;
    sats = 0;
    alt = 1200;
    vel = 0;
    pres = 102.4012412;
    temp = 15;
    acc = -0.01;
    vcc = 3;
    buttons = new ArrayList<Button>();
    //// Fill graph points with zeroes
    //for(int i = 0; i < 100; i++){
    //  altitudes[i] = 0.0;
    //}
    //Movie.supportedProtocols[0] = "rtsp";
    //movie = new Movie(this, "rtsp://raspberrypi:8080/");
    //try {
    //  movie.play();
    //  movieLoaded = true;
    //} 
    //catch (Exception e) {
    //  //println(e);
    //  movieLoaded = false;
    //}
    portName = Serial.list()[0];
    println(portName);
    myPort = new Serial(this, portName, 9600);
}
//void movieEvent(Movie m) {
//  try {
//    m.read();
//    lastReadTime = millis();
//    if(movieLoaded == false){
//      movieLoaded = true;
//      println("-CONNECTED");
//    }
//  } catch (Exception e) {
//    if(movieLoaded == true){
//      movie.stop();
//      movieLoaded = false;
//      println("-[WARN] DISCONNECTED");
//    }
//  }
//}

float lat, lon, alt, vel, acc, temp, pres, vcc;
int sats;
int writtenLines;
boolean connectedRX = false;
boolean setupButtons = false;
boolean autoCenterMap = true;
boolean enableRPi = false;
String dataString[] = {};
String callsign = "UNIDENTIFIED";
public void draw(){
  if(!setupButtons){
    buttons.add(new Button(width/2, height-75, 400, 100, "square", "Disabled", 16, #FFFFFF, #FF3636, #CE2E2E, 2)); // Turn on RPi
    buttons.add(new Button(width/2, height-200, 400, 100, "square", "Not logging", 16, #FFFFFF, #FF3636, #CE2E2E, 3)); // Turn on csv logging
    //buttons.add(new Button(width-50, height-(400), 100, 32, "square", "Reset", 12, #FFFFFF, #333333, #777777, 10)); // Submit
    buttons.add(new Button(width-75, height-(400), 100, 32, "square", "AUTO", 12, #FFFFFF, #2ECE5A, #25AF4B, 11)); // Auto track cansat
    setupButtons = true;
  }
  getdata();
  //println("                      ",lastReadTime, millis(), connectioncounter, connectiondelay);
  //// Timeout of five seconds
  //if(lastReadTime <= millis() - 5000){
  //  movieLoaded = false;
  //}
  //// Try to connect to stream
  //if(connectioncounter >= connectiondelay){
  //  if (movieLoaded == false){
  //    try {
  //      println("Trying to connect to video");
  //      movie = new Movie(this, "rtsp://raspberrypi:8080/");
  //      movie.play();
  //      if (movie.available()) {
  //        movieLoaded = true;
  //        println("CONNECTED");
  //      } else {
  //        movieLoaded = false;
  //        //movie.stop();
  //        println("NOT CONNECTED");
  //      }
  //    } catch (Exception e) {
  //      if(movieLoaded == true){
  //        movie.stop();
  //        movieLoaded = false;
  //        println("[WARN] DISCONNECTED");
  //      }
  //    }
  //  }
  //  connectioncounter = 0;
  //}
  //connectioncounter ++;
  
  background(0);
  Location cansat = new Location(lon,lat);
  if(autoCenterMap){
    map.panTo(cansat);
  }
  map.draw();
  push();
  for(int i = 0; i < buttons.size(); i++){
    Button button = buttons.get(i);
    button.display();
  }
  graph(altitudes, "ALTITUDE",0,height-400,700,400,#00C601);
  //graph(accelrations, "ACCELERATION",0,300,700,400,#E635FA);
  try {
    if(movieLoaded){
      image(movie, 0, 300, 1920/3, 1080/3);
    } else {
      graph(accelrations, "ACCELERATION",0,300,700,400,#E635FA); 
    }
  } catch (Exception e) {
    graph(accelrations, "ACCELERATION",0,300,700,400,#E635FA); 
  }
  pop();
  fill(255);
  cansatMarker.setLocation(cansat);
  textSize(48);
  text("CANSAT MAI 2022",0,80);
  textSize(24);
  text("CanSat " + callsign + " " + portName ,4,130);
  fill(#F6FF03);
  text((year() + "." + pad(month(),2) + "." + pad(day(),2) + " " + pad(hour(),2) + ":" + pad(minute(),2) + ":" + pad(second(),2) + " (" + counter + ")"),4,172);
  writtenLines = 0;
  write("LAT", lat, 5, "");
  write("LON", lon, 5, "");
  write("ALT", alt, 2, "m", #00C601);
  write("VEL", vel, 3, "mps");
  write("ACC", acc, 2, "mpss");
  write("SAT", sats, 0, "");
  write();
  write("T  ", temp, 1, "°C", #6464FF);
  write("P  ", pres, 4, "kPa");
  write("VCC", vcc, 3, "V");
  directionalLight(126, 126, 126, 0, -1, 0);
  ambientLight(200, 200, 200);
  translate(width/2, height/2, 300);
  rotateX(radians(180));
  //rotateY(mouseX*0.01f);
  rotateX(radians(rotX));
  rotateY(radians(rotY));
  rotateZ(radians(rotZ));
  translate(0,-115/2,0);
  gfx.origin(new Vec3D(), 100);
  noStroke();
  fill(#FF7700);
  gfx.mesh(mesh, false, 0);
}

String pad(int a, int padding){
  String out = "";
  for(int p = padding-1; p > 0; p--){
    int checkVal = int(pow(10,p));
    if(a < checkVal){
      out += '0';
    }
  }
  out += str(a);
  return out;
}
void getdata(){
  //float amplitude = 5;
  //float noise = noise(seed)-0.5;
  //rotX += noise *amplitude;
  //rotY += noise *amplitude;
  //rotZ += noise *amplitude;
  //lat += noise * 0.002;
  //lon += noise * 0.002;
  
  //sats = int(sats + noise *2);
  //acc += noise *0.1;
  //vel += noise;
  //alt += noise;
  //pres += noise * 0.002;
  //temp += noise * 0.02;
  
  
  String vals = "";
  while ( myPort.available() > 0) {  // If data is available,
    vals += char(myPort.read());         // read it and store it in val
  }
  if(vals != ""){
    // Process
    String valueArray[];
    valueArray = split(vals, ',');
    if(valueArray.length == 20){
      //printArray(valueArray);
      callsign = valueArray[0];
      counter = int(valueArray[1]);
      acc = float(valueArray[8]);
      temp = float(valueArray[4]);
      float ax = float(valueArray[5]);
      float ay = float(valueArray[6]);
      float az = float(valueArray[7]);
      pres = float(valueArray[19]);
      rotX = float(valueArray[16]);
      rotY = float(valueArray[17]);
      rotZ = float(valueArray[18]);
      //rotX = degrees(atan((ax) / sqrt(ay * ay + az * az))) + 0;
      //rotY = degrees(atan((ay) / sqrt(ax * ax + az * az))) + 0;
      //rotZ = degrees(atan((sqrt(ax * ax + ay * ay)) / (az))) + 0;
      //println(ax, ay, az, rotX, rotY, rotZ);
      int startTemp = 15;
      float startPres = 102.08;
      alt = 0+(startTemp+273.15)/-0.0065*(pow((pres/startPres),((-8.31432*-0.0065)/(9.80665*0.0289644)))-1);
      vcc = float(valueArray[3]);
    }
  }
  if (counter % graphdelay == 1){
    altitudes[locpoint] = alt;
    accelrations[locpoint] = acc;
    locpoint ++;
    locpoint %= 100;
  }
  if(logging){
    if(lastSavedFrame != counter){
      dataString = append(dataString, day() + ";" + hour() + ";" + minute() + ";" + second() + ";" + 
                                      counter + ";" + callsign + ";" + rotX + ";" + rotY + ";" + rotZ + ";" + 
                                      lon + ";" + lat + ";" + alt + ";" + sats + ";" + 
                                      acc + ";" + vel + ";" + temp + ";" + pres);
      lastSavedFrame = counter;
    }
  }
    
  //seed += 0.005;
  //counter = (counter + 1);
}
int gap = 55;
int padX = 730;
void graph(float points[], String name, int startX, int startY, int grWidth, int grHeight, color c){
  PGraphics gr = createGraphics(grWidth, grHeight, P2D);
  int startGrX, stopGrX, startGrY, stopGrY;
  startGrX = 2*grWidth/10;
  stopGrX = 9*grWidth/10;
  startGrY = 9*grHeight/10;
  stopGrY = grHeight/10;
  gr.beginDraw();
  gr.clear();
  gr.stroke(255);
  gr.strokeWeight(4);
  // Axes
  gr.line(startGrX, stopGrY, startGrX, startGrY);
  gr.line(stopGrX, startGrY, startGrX, startGrY);
  gr.textFont(font);
  gr.textSize(16);
  float maxVal = ceil(max(points));
  float minVal = floor(min(points));
  if(maxVal == minVal){
    maxVal += 1;
    minVal -= 1;
  }
  // Lines on y axis
  for(int i = 0; i < 11; i++){
    gr.line(startGrX - 3, map(i,0,10,startGrY,stopGrY), startGrX + 3, map(i,0,10,startGrY,stopGrY));
    String text = str(map(i,0,10,minVal,maxVal))+"00";
    if (text.length() > 5){
      text = text.substring(0, 6);
    }
    gr.text(text, 5, map(i,0,10,startGrY,stopGrY)+8);
  }
  gr.textAlign(CENTER);
  gr.text(name,grWidth/2,32);
  gr.stroke(c);
  int startno = (locpoint + 100) % 100;
  int stopno = (locpoint+99);
  for(int i = startno+1; i != stopno; i = (i + 1) ){
    int lasti;
    if(i == 0){
      lasti = 99;
    } else {
      lasti = i-1;
    }
    //println(i, (locpoint + 100) % 100, (locpoint+99) % 100);
    if(altitudes[i%100] != -22222222 && altitudes[lasti%100] != -22222222){
      gr.line(map(i, startno, stopno, startGrX, stopGrX),
              map(points[i % 100],minVal,maxVal,startGrY,stopGrY),
              map(lasti, startno, stopno, startGrX, stopGrX),
              map(points[lasti%100],minVal,maxVal,startGrY,stopGrY));
    }
    //println(i, " ", startno, stopno, map(i, startno, stopno, startGrX, stopGrX),
    //        map(points[i % 100],minVal,maxVal,startGrY,stopGrY),
    //        map(lasti, startno, stopno, startGrX, stopGrX),
    //        map(points[lasti%100],minVal,maxVal,startGrY,stopGrY));
  }
  //println(locpoint, (locpoint + 100) % 100, (locpoint-1 + 100) % 100);
  gr.endDraw();
  image(gr, startX,startY);
}

// If no values are given, skip line
void write(){
  writtenLines ++;
}
// If no color is given, give it white
void write(String name, float value, int decimals, String unit){
  write(name, value, decimals, unit, #FFFFFF);
}
void write(String name, float value, int decimals, String unit, color c){
  textSize(32);
  int padding1 = 5-str(floor(abs(value))).length();                 // 4 characters gap, make space for each digit left of comma
  if(value < 0){
    padding1 --;
  }
  int padding2 = 9- (decimals + unit.length());   // 9 characters gap, make space for each decimal and unit chars
  String text = ""; // The text that will eventually be displayed
  text = text + name; // Add name to start of text
  text = text + ':'; // Then append a colon
  for(int i = 0; i < padding1; i++){ // Calculate the needed gap to allign points, then add spaces in the gaps
    text = text + ' ';
  }
  if (value < 0){
    text = text + ceil(value); // Add the integer part of the number
  } else {
    text = text + floor(value); // Add the integer part of the number
  }
  if (decimals > 0){
    text = text + '.'; // Add a decimal point if decimals are printed
  } else {
    padding2 ++;
  }
  float dec = (abs(value) % 1);//floor(value % 1 * pow(10, decimals)); // Value between 0 and 1, mult by 10^digits and round down to get desired number of decimals
  for (int i = decimals; i >= 1; i --){ // Loop through all decimals and add them to the text. Needs to be done this way because of zeroes
    dec = dec % 1;
    dec = dec * 10;
    if(i == 1){
      text = text + floor(dec);
    } else {
      text = text + floor(dec);
    }
  }
  for(int i = 0; i < padding2; i++){ // Calculate the needed gap to allign units, then add spaces in the gaps
    text = text + ' ';
  }
  text = text + unit; // Lastly add the units
  fill(c);
  text(text, width-padX, 50+gap*writtenLines);
  writtenLines ++;
}

String connectedDevice = "";
void mousePressed() {
  int action = 0;
  String value = "";
  int pressedButton = -1;
  // Check if any button was clicked
  for(int i = 0; i < buttons.size(); i++){
    Button button = buttons.get(i);
    if(button.isOver()){
      // Get the action and text of button
      String values[] = button.getId();
      action = int(values[0]);
      value = values[1];
      pressedButton = i;
      //println("Clicked action: " + action + ", value " + value);
    }
  }
  if(action != 0){ // If sonething was clicked
    if(action == 1){ // Set COM port
      if(value != "Discover"){
        //try{ // Try to connect to port
        //  bt.connectToDeviceByName(value);
        //  //myPort = new Serial(this, value, 9600);
        //  bluetoothConnected = true;
        //  connectedDevice = value;
        //  //println("Connection succeded, removing buttons");
        //  // Remove buttons that set COM port
        //  addedButtons = false;
        //  int buttonAmount = buttons.size();
        //  for(int i = buttonAmount-1; i >= 0; i--){
        //    Button button = buttons.get(i);
        //    int id = int(button.getId()[0]);
        //    //println(button.getId()[1]);
        //    //println(buttons.size());
        //    //println(i);
        //    if(id == 1){
        //      buttons.remove(i);
        //    }
        //  }
        //  delay(200);
        //} catch (Exception e){ // If couldnt connect, return to last state
        //  bluetoothConnected = false;
        //  //println("Connection failed");
        //}
      } else { // Discover devices
        //println("TODO, Search for devices");
      }
    } else {
      //println("Pressed ", action);
      switch (action){
        case 2:
          //println("Toggle rpi enable");
          if(enableRPi){
            // Toggle and change color and text of button
            enableRPi = false;
            Button button = buttons.get(pressedButton);
            button.setColors(#FFFFFF, #FF3636, #CE2E2E);
            button.setText("Disabled");
          } else {
            enableRPi = true;
            Button button = buttons.get(pressedButton);
            button.setColors(#FFFFFF, #2ECE5A, #25AF4B);
            button.setText("Enabled");
          }
          break;
        case 3:
          //println("Toggle rpi enable");
          if(logging){
            // Toggle and change color and text of button
            logging = false;
            Button button = buttons.get(pressedButton);
            button.setColors(#FFFFFF, #FF3636, #CE2E2E);
            button.setText("Not logging");
            saveStrings(filename, dataString);
          } else {
            logging = true;
            Button button = buttons.get(pressedButton);
            button.setColors(#FFFFFF, #2ECE5A, #25AF4B);
            button.setText("Logging");
            // Create a file name based on the time, and empty previous data
            filename = str(day())+str(hour())+str(minute())+str(second()) + ".csv";
            String emptyArr[] = {" "};
            dataString = emptyArr;
          }
          break;
        case 11:
          //println("Toggle auto centring");
          if(autoCenterMap){
            autoCenterMap = false;
            Button button = buttons.get(pressedButton);
            button.setColors(#FFFFFF, #FF3636, #CE2E2E);
          } else {
            autoCenterMap = true;
            Button button = buttons.get(pressedButton);
            button.setColors(#FFFFFF, #2ECE5A, #25AF4B);
          }
          break;
      }
    }
  }
}
