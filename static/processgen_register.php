<?php
/*************Do not generate output if your intention is to redirect*****/
/****mail($)*******/
		function check_input($data, $problem=''){
			$data= trim($data);
			$data= stripslashes($data);
			$data= htmlspecialchars($data);
			if($problem && strlen($data) == 0){
				display_error($problem);	
			}
			return $data;	
		}

$name= check_input($_POST["fullname"]);
$organization= check_input($_POST['organization']);
$email= check_input($_POST['email']);
$comments= check_input($_POST['comments']);


if(	is_string($name) && !empty($name))
	
{

	$message= 
		"	
		To: Handstack
		
		From: $name
		
		Company: $organization
		
		Email: $email

		You received a communication from the above named individual.  Their comments are provided below:
		
		$comments";
	
	mail("info@wpkinsey.com", "services", $comments, "From:" . $email);

    
  include 'includes/head.html';

?> 
	<div class= "pgHead">
		<span class= "span_pgHead">We appreciate Your Interest</span>
	</div> 
<div class= "pgCont" id= "thankyou_pgCont">
<div id= "SpcHld_L">
	<img src="images/FC_team.png">
	<?php //var_dump($firstName, $lastName, $companyName, $address, $city, $state, $zipCode, $email);
	
	//echo "<br> $message"; ?>
</div>
</div>	
<?php
	// Include HTML footer file
	include 'includes/foot.html';
?>


<?php
}
else {

    include 'includes/head.html';
?>
	<div class= "pgHead" >
		<div class= "span_pgHead" id= "contactSpan1">Please review the information.</div>
	</div>
	<div class="pgCont" id="formPgCont">
	<!------Page Content Begins------->
	
	<div id= "error">
		<?php 
		
		function display_error($error){
	
			echo	"<div id= \"error\"> $error</div>";
		}
		
		/*function check_input($data, $problem=''){
			$data= trim($data);
			$data= stripslashes($data);
			$data= htmlspecialchars($data);
			if($problem && strlen($data) == 0){
				display_error($problem);	
			}
			return $data;	
		}*/
			
$firstName= check_input($_POST['fullname']);
$lastName= check_input($_POST['organization']);
$companyName= check_input($_POST['companyName']);
$address= check_input($_POST['email']);
$city= check_input($_POST['password']);

//var_dump($firstName, $lastName, $companyName, $address, $city, $state, $zipCode, $email);


/*function check_input($data, $problem=''){
			$data= trim($data);
			$data= stripslashes($data);
			$data= htmlspecialchars($data);
			if($problem && strlen($data) == 0){
				display_error($problem);		
			}
}*/



$error_msg= "display_error";
		
		
?>
	</div>

        <div class="main-container">
            <div class="main wrapper clearfix">

                <article>
                    <header>
                        <h1>SignUp with HandStack!
						<form method="post" action="processgen_form.php">
							<input type= "text" name="fullname" placeholder= "full name"><br>
							<input type= "text" name="organization" placeholder= "organization name"><br>
							<input type= "text" name="email" placeholder= "email "><br>
							<textarea name="comments" placeholder= "comments" cols= "30" rows= "5"></textarea>
							<input type= "submit" value= "send">
						</form>
                </article>

                <!--aside>
                    <h3>aside</h3>
                    <p>Lr. Nunc vel vehicula ante. Etiam bibendum iaculis libero, eget molestie nisl pharetra in. In semper consequat est, eu porta velit mollis nec. Curabitur posuere enim eget turpis feugiat tempor. Etiam ullamcorper lorem dapibus velit suscipit ultrices.</p>
                </aside-->

            </div> <!-- #main -->
        </div> <!-- #main-container -->

        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
        <script>window.jQuery || document.write('<script src="js/vendor/jquery-1.10.1.min.js"><\/script>')</script>

        <script src="js/main.js"></script>

        <script>
            var _gaq=[['_setAccount','UA-XXXXX-X'],['_trackPageview']];
            (function(d,t){var g=d.createElement(t),s=d.getElementsByTagName(t)[0];
            g.src='//www.google-analytics.com/ga.js';
            s.parentNode.insertBefore(g,s)}(document,'script'));
        </script>
<?php

    include 'includes/foot.html';
?>
	
<?php	
}
?>