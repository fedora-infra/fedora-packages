<% import tg %>
<html>
<title>Oops!</title>
<body id="error-page">
<head>
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
<a href="javascript:history.go(-1)"><h3>Click the panda to go back.</h3></a>

<div id="geiger">
<img src="${tg.url('/images/geiger.png')}"/>
<h3 id="error-code">${code}</h3>
</div>

<a href="javascript:history.go(-1)"><img id="hotdog" src="${tg.url('/images/laser.png')}"/></a>
<a href="javascript:history.go(-1)"><img id="panda" src="${tg.url('/images/panda-wee.png')}"/></a>
<br/>
<script>
		$(document).ready(function() {
			for (var i=0; i < 20; i++) {
				$("img#panda").fadeIn(4500);
				$("img#panda").fadeOut(4500);
			}
			$("img#panda").fadeIn(4500);
		}); // end doc ready
</script>
</body>
</html>
