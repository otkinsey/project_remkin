

function loadtasklist(eid){

    $.getJSON( "/tasksearch/?eventid="+eid.toString(), function( data ) {

        var items = [];

        $.each( data['tasks'], function( key, val ) {

            items.push( "<li id='" + key + "' >" + val['taskTitle'] + "</li>" )

        });

        $( "#tasklist" ).replaceWith(

        $( "<ul/>", { "id": "#tasklist",
            "class": "taskitem",
        html: items.join( "" )
        })
        );
    });


}
