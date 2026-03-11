(function(){
  var el = document.createElement('div');
  el.id = 'college-agent';
  el.style.border = '1px solid #ccc';
  el.style.padding = '10px';
  el.style.maxWidth = '400px';
  el.innerHTML = '' +
    '<div id="ca-messages" style="height:200px;overflow:auto"></div>' +
    '<input id="ca-input" style="width:100%;" placeholder="Ask a question..."/>';
  document.body.appendChild(el);
  var msgBox = el.querySelector('#ca-messages');
  var input = el.querySelector('#ca-input');
  input.addEventListener('keydown', function(e){
    if(e.key==='Enter'){
      var text = input.value.trim();
      if(!text) return;
      var p = document.createElement('div'); p.textContent = 'You: '+text;
      msgBox.appendChild(p);
      fetch('/chat',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({message:text})})
      .then(r=>r.json())
      .then(j=>{
        var q = document.createElement('div'); q.textContent = 'Agent: '+j.answer;
        msgBox.appendChild(q);
        msgBox.scrollTop = msgBox.scrollHeight;
      });
      input.value='';
    }
  });
})();
