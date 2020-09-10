//Usage

// API Post Function. Here we send data back to Streamlabs Chatbot through spinwheel's API
// This api let's us write some data to disk for the chatbot to pick up
function APIPost(e){
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "http://localhost:5000/nuggets", true);

  //Send the proper header information along with the request
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

  xhr.onreadystatechange = function(){ // Call a function when the state changes.
    if (this.readyState === XMLHttpRequest.DONE && this.status === 200){
      // Request finished. Do processing here.
    }
  }
  payload = e;
  xhr.send("count=" + payload );
};

//load your JSON (you could jQuery if you prefer)
function loadJSON(callback) {

  var xobj = new XMLHttpRequest();
  xobj.overrideMimeType("application/json");
  xobj.open('GET', './static/wheel_data.json', true); 
  xobj.onreadystatechange = function() {
    if (xobj.readyState == 4 && xobj.status == "200") {
      //Call the anonymous function (callback) passing in the response
      callback(xobj.responseText);
    }
  };
  xobj.send(null);
}

//your own function to capture the spin results
function myResult(e) {
  //e is the result object
    console.log(e);
    console.log('Spin Count: ' + e.spinCount + ' - ' + 'Win: ' + e.win + ' - ' + 'Message: ' +  e.msg);

    // if you have defined a userData object...
    if(e.userData){
      
      console.log('User defined score: ' + e.userData.score);
      APIPost(e.userData.score);

    }

    setTimeout(function(){
      hideWheel();
      setTimeout(function() {
        e.target.restart();
        changeImage();
      }, 500)
    }, 9000);

  //if(e.spinCount == 3){
    //show the game progress when the spinCount is 3
    //console.log(e.target.getGameProgress());
    //restart it if you like
    //e.target.restart();
  //}  

}

//your own function to capture any errors
function myError(e) {
  //e is error object
  console.log('Spin Count: ' + e.spinCount + ' - ' + 'Message: ' +  e.msg);

}

function myGameEnd(e) {
  //e is gameResultsArray
  console.log(e);
  TweenMax.delayedCall(5, function(){
    //location.reload();
  })


}

function init() {
  loadJSON(function(response) {
    // Parse JSON string to an object
    var jsonData = JSON.parse(response);
    //if you want to spin it using your own button, then create a reference and pass it in as spinTrigger
    var mySpinBtn = document.querySelector('.spinBtn');
    //create a new instance of Spin2Win Wheel and pass in the vars object
    var myWheel = new Spin2WinWheel();
    
    //WITH your own button
    myWheel.init({data:jsonData, onResult:myResult, onGameEnd:myGameEnd, onError:myError, spinTrigger:mySpinBtn});
    
    //WITHOUT your own button
    //myWheel.init({data:jsonData, onResult:myResult, onGameEnd:myGameEnd, onError:myError);
  });
}



//And finally call it
init();
hideWheel();

//Automatically click the spin button after 2 seconds
function startSpin(){
    showWheel();
    setTimeout(function(){
      document.getElementById("spin").click();
    },1500);
}

function showWheel(){
  var d = document.getElementById("wheel");
  d.classList.remove("bounceOutDown");
  d.classList.add("bounceIn");
}

//hide the body of the document
function hideWheel(){
    var d = document.getElementById("wheel");
    d.className += " bounceOutDown";
}

//timed events for spinning and hiding wheel
//setTimeout(startSpin, 4000);
//setTimeout(hideWheel, 20000);

var imageURLs = [
  "static/media/twillsie.gif"
];

function changeImage() {
  var randomIndex = Math.floor(Math.random() * imageURLs.length);
  var img = '<image id=\"personality\" href=\"';
  img += imageURLs[randomIndex];
  img += '\" alt=\"Some alt text\" width=\"330\" height=\"330\" x=\"348\" y=\"219\"></image>';
  console.log(img)
  document.getElementById('personality').outerHTML = img;
}
