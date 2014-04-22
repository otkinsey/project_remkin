
lasttask={};

function loadtasklist(eid){
    $.getJSON( "/tasksearch/?eventid="+eid.toString(),function(data){buildlist(data)});
}

function buildlist(data){
 //var items = [];

console.log(data)
        for (var tsk in data['tasks']) {


       Task= $( "<div/>", { "id": tsk ,"class": "taskitem"})
    Task.html( data.tasks[tsk]["taskTitle"] )
    Task.append("<input type='checkbox' value="+data.tasks[tsk]["taskStatus"]+">");
    Task.append("");


Task.appendTo("#tasklist");



        }

}

