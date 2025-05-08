//author surya
// Linked repository with demo 
// https://github.com/thesunRider/APMWS/tree/master/assign/ubq2

let showTime = true;
let swipeIndicator = "";
let accelSimData = 0;

// Display function
function updateDisplay() {
  g.clear();
  g.setFont("6x8", 2);
  g.setFontAlign(0, 0); // center
  g.drawString(showTime ? getTimeString() : getDateString(), g.getWidth() / 2, g.getHeight() / 2);
  g.setFont("6x8", 1);
  g.drawString("Swipe: " + swipeIndicator, g.getWidth() / 2, g.getHeight() - 10);
  g.flip();
}

// Format time
function getTimeString() {
  let d = new Date();
  return ("0" + d.getHours()).slice(-2) + ":" +
         ("0" + d.getMinutes()).slice(-2) + ":" +
         ("0" + d.getSeconds()).slice(-2);
}

// Format date
function getDateString() {
  let d = new Date();
  return d.getFullYear() + "-" +
         ("0" + (d.getMonth() + 1)).slice(-2) + "-" +
         ("0" + d.getDate()).slice(-2);
}

//this wont get called because espruino ide doesnt simulate these
function accelHandler(a) {
  console.log( "x:"+a.x+" y:"+a.y+" z:"+a.z );  // a.mag and a.diff not used
}
function accelConfig(hz,gs) {
   switch (hz) { case 12.5:  KI_HZ = 0x00; break; // 12.5 Hz
                 case 25:    KI_HZ = 0x01; break; // 25 Hz
                 case 50:    KI_HZ = 0x02; break; // 50 Hz
                 case 100:   KI_HZ = 0x03; break; // 100 Hz
  }
  switch (gs) { case 2:  KI_GS = 0x00; break; // sensitivity = +/-2g
                case 4:  KI_GS = 0x08; break; // sensitivity = +/-4g
                case 8:  KI_GS = 0x10; break; // sensitivity = +/-8g
  }
}
accelConfig(12.5,8);
Bangle.setPollInterval(10);  
Bangle.on('accel',accelHandler);

setInterval(() => {
  accelSimData = Math.random() * 10;
  console.log("Accelerometer reading (simulated):", accelSimData.toFixed(2));
}, 4000);


Bangle.on("swipe",function(direction){
   console.log("Swiped :"+ direction);
  switch (direction){
    case 0 : swipeIndicator = "Down"; break;
    case 1 : swipeIndicator = "Right";break;
    case -1 :swipeIndicator = "Left"; break;
  }
});



// Button 1 toggles time/date
setWatch(() => {
  showTime = !showTime;
  updateDisplay();
}, BTN1, { repeat: true, edge: "rising", debounce: 50 });

// Update display every second
setInterval(updateDisplay, 1000);

// Initial display
g.clear();
updateDisplay();
