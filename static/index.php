<?php

include "includes/head.html";

/*********************home page output***********************************/
?>


            <div class="main wrapper clearfix">
				<div>
                <div class= "slider_cont"><!------media queries for different screen sizes------------------>
<div class= "slider" >
	<img id="1" src= "img/sliderImg_01.png">
	<!--div class= "slider-wrap">
	<div class= "slider-nav" style= "position:relative;left:.3em;" ><img src= "img/slider-nav-r.png" class= "" onclick="prev(); return false;"></div>
	<div class= "slider-frame ">
		<div class= "inner-frame">		
		<div class= "imgDisplay_L" id= "FC_imgGallery">
						
		</div>
		</div>				
	</div>
	<div class= "slider-nav" style= "position:relative;left:-.3em;" ><img src= "img/slider-nav-l.png" onclick="next(); return false;"></div>
	<div class= "paginate-wrap">
		<ul>
			<li id= "t1" class="pagination"></li>
			<li id= "t2" class="pagination"></li>
			<li id= "t3" class="pagination"></li>
			<li id= "t4" class="pagination"></li>
		</ul>
	</div>	
	</div-->
	<!--div class= "FC_imgControl_cont">
	<div class="FC_imgControl " id= "FC_prev"><a  href= "#" onclick="prev(); return false;"><img id= "ssImg_1" class= "ssImg" src= "images/video/controls/prev_off.png" ></a></div>
	<div class="FC_imgControl " id= "FC_pause"><a  href= "#" onclick="pause(); return false;"><img id= "ssImg_2" class= "ssImg" src= "images/video/controls/pause_off.png"></a></div>
	<div class="FC_imgControl " id= "FC_next"><a href= "#" onclick="next(); return false;"><img id= "ssImg_3" class= "ssImg" src= "images/video/controls/next_off.png"></a></div>
	</div-->	
	<!--script>
		sliderInt = 1;
		sliderNext = 2;
		t_Int = 1;
		t_Next = 2;
		
		$(document).ready(function(){
			$("#FC_imgGallery>img#1").fadeIn(1500);
			//$("#t1").removeClass("pagination");
			$("#t1").addClass("pagination-dark");
			startLoop();
		});
		
		function startLoop(){
			count = $("#FC_imgGallery>img").size();
			
			t_count = 4
			
			loop = setInterval(function(){
				
				if(sliderNext > count){
					sliderNext = 1;
					sliderInt = 1;
				}
				
				if(t_Next > t_count){
					t_Next = 1;
					t_Int =1;
				}
								
				$("#FC_imgGallery>img").hide();
				$("#FC_imgGallery>img#" + sliderNext).fadeIn(2000);
				$(".pagination").removeClass("pagination-dark");
				$("#t" + t_Next).addClass("pagination-dark");
				sliderInt = sliderNext;
				sliderNext = sliderNext + 1;
				t_Int = t_Next;
				t_Next = t_Next + 1;
			},5000)
		}
		
		function prev(){
			newSlide = sliderInt - 1;
			newSlide= t_Int - 1;
			showSlide(newSlide);
		}

		function pause(){
		stopLoop();
		}


		function next(){
			newSlide = sliderInt + 1;
			newSlide = t_Int + 1;
			showSlide(newSlide);
		}	
		
		function stopLoop(){
			window.clearInterval(loop);
		}
		
		function showSlide(id){
			stopLoop();
				if(id > count){
					id = 1;
				}else if(id < 1){
					id = count;
				}
								
				$("#FC_imgGallery>img").hide();
				$("#FC_imgGallery>img#" + id).fadeIn(2000);
				$(".pagination").removeClass("pagination-dark");
				$("#t" + id).addClass("pagination-dark");
				sliderInt = id;
				sliderNext = id + 1;
				t_Int = id;
				t_Next = id + 1;
			startLoop();		
		}	
		</script-->	
	</div>
                </div>					
				</div>
				<div class= "article_wrap">
                <article>
                    <header>
                        <h1>Welcome to HandStack!</h1>
                        <h2>HandStack allows you to connect with cool people doing cool stuff in your area and beyond.</h2>
                    </header> 
                </article>
                <aside>
                	<ul>
                		<li>share tasks</li>
                		<li>organize on the go</li>
                		<li>connect your team</li>
                		<li>collaborate with others</li>
                		<li>publicise your event</li>
                	</ul>
                </aside>					
				</div>
            </div> <!-- #main -->
<?php
include 'includes/foot.html'
?>