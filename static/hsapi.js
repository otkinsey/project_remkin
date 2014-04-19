/*

Registration
Login

searchbox
<div id="e-23" class="event">
<img class="eventimage" />
<div id="tasklist" class="tasklist tl-eid">
<div id="tl-tid" class="tasklistitem">
<div id="t-tid" class="task">
<div id="eventlist" class="">
<div id="el-23" class="eventlistitem">
<div id="mapcontainer" class=""></div>
<div id="myprofile" class="profile">
<img class="profileimage" />
<div id="interestname" class="interest" >
*/






function loadlist(){

$.getJSON( "/search/", function( data ) {
var items = [];
$.each( data['events'], function( key, val ) {
items.push( "<li id='" + key + "' onClick='showevent(\""+ key +"\")'>" + val['eventName'] + "</li>" )
});
$( "#eventlist" ).replaceWith(
$( "<ul/>", { "id": "#eventlist",
"class": "eventlist",
html: items.join( "" )
})
);
});


}
var foo={};


function showevent(eid){
foo=eid;

$.getJSON( "/search/",{'eventid': eid}, function( data, eid ) {
var items = [];
$.each( data['events'][foo], function( key, val ) {
items.push( "<li id='" + key + "'>" + key+ " : "+val + "</li>" );
});

$( "#eventpane" ).replaceWith(

$( "<ul/>", { "id": "eventpane",
"class": "my-new-list",
html: items.join( "" )
})
);

});




}












function makeEvent(){
    var url = "/make/"; // the script where you handle the form input.
    $.ajax({
           type: "POST",
           url: url,
           data: {




                },
           success: function(data)
           {
               loadlist(); // show response from the php script.
           }
         });

});
