var MessageLogger=function(idMessageList){
  var messageList=$(idMessageList);
  var messages=[];

  var refresh=function(){
    messageList.innerHTML=buildMessages()
  };

  var buildMessages=function(){
    var html="";
    for(var i=0;i<messages.length;i++){
      html+="<li class=\"message\">"+messages[i]+"</li>";
    }
    return html;
  };

  this.addMessage=function(message){
    messages.push(message);
    refresh();
  };

  this.clear=function(){
    messages=[];
    refresh();
  };
}
