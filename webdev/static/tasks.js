
lasttask={};

function loadtasklist(eid){
    $.getJSON( "/tasksearch/?eventid="+eid.toString(),function(data){buildlist(data)});
}

function buildlist(data){
 //var items = [];

console.log(data)
        for (var tsk in data['tasks']) {

mode="";
       Task= $( "<div/>", { "id": tsk ,"class": "taskitem"})
    Task.html( data.tasks[tsk]["taskTitle"] )
    
    if (data.tasks[tsk]["taskStatus"]=="True"){
        mode=" checked ";}
    Task.append("<input type='checkbox' id='tstatus"+tsk+"' name='taskStatus"+tsk+"'"+ mode +"value='True' onClick='taskstatusupdate("+tsk+")'>");


Task.appendTo("#tasklist");



        }

}

function taskstatusupdate(tid){
console.log(tid)

mode="False"
if ($("#tstatus"+tid.toString()).is(":checked")) {
mode="True"
}
console.log (mode)

$.ajax({url: "/taskupdate/",
    type:"POST",
    data: {"taskStatus":mode,
           "taskid":tid.toString()
          }
    });


}

