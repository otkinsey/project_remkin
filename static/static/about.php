<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
"http://www.w3.org/TR/html4/strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
	<head>
		<meta name= "viewport" content= "width=device-width, initial-scale=1.0">
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<title>welcome to handstack</title>
		<meta name="author" content="remkin" />
		<!-- Date: 2014-02-25 -->
		<link href= "css/main.css" rel= "stylesheet" type= "text/css">
		<link href= "css/normalize.css" rel= "stylesheet" type= "text/css">
		<link href= "css/normalize.min.css" rel= "stylesheet" type= "text/css">
		<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
  		<script src="js/vendor/1.10.1.min.js"></script>
  		<script src="js/main.js"></script>
  	<script>
  		$(document).ready(function(){
  			$(".team_member").click(function(){
  				var name = $(this)
	  			$.get("about.html", function(data){
 	 				$(".main-container").html(data);
  				}); 				
  			});
  		});

  		$(document).ready(function(){
  			$("#team").click(function(){
	  			$.get("team.html", function(data){
 	 				$(".main-container").html(data);
  				}); 				
  			});
  		});

  		$(document).ready(function(){
  			$("#about").click(function(){
	  			$.get("about.html", function(data){
 	 				$(".main-container").html(data);
  				}); 				
  			});
  		});
  		
  		
  	</script>	
	</head>
	<body>

		<div class= "site_container">
        <div class="header-container"> 
        	
             	<div class= "header_element">
             		<a href= "index.php" class= "h_e-1_lrg">
             		<img src= "img/logo.png" class= "logo" >
            		<img src= "img/handstack_b.png" class= "handstack">           		           		
            		</a>             		
             	</div>
				<div class= "header_element">
						<ul class= "nav_horizontal h_e-2_lrg">
							<a href="index.php" id= "home"><li class= "inline_item">Home</li></a>
							<a href="about.php" id= "about"><li class= "inline_item">About Us</li></a>
							<a href="team.php" id= "team"><li class= "inline_item">Team</li></a>
						</ul>
            	</div>	
            	     	
        	          
       
        </div><!---header-container----->
        <div class= "main-container">
		<div class= "title" id= "about_title"></div>
		<div class= "article">
			<div class= "section">
				We're just a fun bunch of guys and gals who are passionate about the web and producing fun web apps that improve people's lives. HandStack is our first contribution to the internet community. Hopefully you'll find it handy and fun to use. Feel free to give us your feed back about the app, be sure to drop by periodically to find what's new in the HandStack community.		</div>	
			</div>
		</div><!----end of "main-container"------> 
        <div class="footer-container">
            <footer class="wrapper">
                <h3>HandStack</h3>
            </footer>
        </div>	        	
	</body>
</html>
