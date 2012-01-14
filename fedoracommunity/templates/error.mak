<% import tg %>
<html>
<title>Oops!</title>
<body id="error-page">
<head>
<script type="text/javascript" src="${tg.url('/_res/tw2.jquery/static/jquery/1.6.2/jquery.js')}" ></script>
<script type="text/javascript" src="${tg.url('/javascripts/jquery.jparallax.js')}" ></script>
<style type="text/css">
  
#geiger {
  position: relative;
  width: 128px;
  margin-left: auto;
  margin-right: auto;
  z-index: 1000;
}

#geiger #error-code {
  font-size: 28px;
  border: 1px solid blue;
  text-align: center;
  margin-top: -52px;
  font-family: Comfortaa, sans-serif;
  color: #cfe736;
  letter-spacing: 10px;
  margin-left: 10px;
  margin-bottom: 0px;
}

body, h1, h2, h3 {
  font-family: Comfortaa, sans-serif;
  text-transform: uppercase;
  text-align: center;
}  

#parallax {
	margin: auto;
	background: black;
	border: solid thin black;
	position:relative; 
	overflow:hidden; 
	width:1000px; 
	height:500px;
}



#panda {
  position: relative;
  z-index: 0;
  top: -50px;
  left: 20px;
}

#hotdog {
  position: relative;
  z-index: 3;
  left: 80px;
  top: -100px;
}

h2 { 
 color: white;
 text-shadow: 1px 1px 0px #db3279;
 font-size: 30px;
 margin-bottom: 0px;
}  

h3 {
 color: #db3279;
 margin-top: 2px;
}

a {
 text-decoration: none;
}

body {
  background: black;
}
</style>
</head>
<h2>Oops, something went wrong!</h2>
<a href="/"><h3>Click the panda to go back.</h3></a>

<div id="geiger">
<img src="${tg.url('/images/geiger.png')}"/>
<h3 id="error-code">${code}</h3>
</div>
<div id="parallax">
  <img id='rad-back'  src="${tg.url('/images/parallax-radiation1.png')}" />
  <img id='panda'  		src="${tg.url('/images/parallax-panda-only.png')}" />
  <img id='rad-front' src="${tg.url('/images/parallax-radiation-top.png')}" />
  <img id='blast'  		src="${tg.url('/images/blast.png')}" />
  <img id='hotdog'  	src="${tg.url('/images/laser.png')}" />
</div>

<br/>
<script>
jQuery(document).ready(function(){
  var opts = {
  };

  var rad_back ={
    xtravel: '45%',
    xorigin: '.55',
    ytravel: '50%',
    yorigin: '-0.6'
  };

  var panda = {
    xtravel: '40%',
    xorigin: '.8',
    ytravel: '40%',
    yorigin: '0.12'
  };

  var rad_front ={
    xtravel: '35%',
    xorigin: '.50',
    ytravel: '30%',
    yorigin: '-0.25'
  };

  var blast = {
    xtravel: '20%',
    xorigin: '.18',
    ytravel: '20%',
    yorigin: '.34'
  };

  var laser = {
    xtravel: '10%',
    xorigin: '0',
    ytravel: '10%',
  };

  $('#parallax').jparallax( opts, rad_back,panda,rad_front,blast,laser);

  var _fade = function(element,duration,loops){
    for (var i=0; i < loops; i++) {
      element
        .fadeIn(duration)
        .fadeOut(duration);
    }
    element.fadeIn(duration);
  }

  var delay = 4500;
  var loops = 20;
  var ratio = .6;

  _fade($('#rad-back'),delay,loops);
  _fade($('#rad-front'),delay * ratio,loops/ratio);
});

</script>
</body>
</html>
