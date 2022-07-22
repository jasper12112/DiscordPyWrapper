const hidden_id = document.getElementById("selectorid");
const action_button = document.getElementById("action_button");

const reason_field = document.getElementById("reason");
const action_select = document.getElementById("action_select");


action_button.onclick = () => {
    if(reason_field.value != null && reason_field.value != "")
    {
        if(hidden_id.value != 1 && hidden_id.value != "1" && hidden_id.value != null && hidden_id.value != "")
        {
            if(action_select.value == "warn")
            {
                axios.get('/api/get/user/' + hidden_id.value)
                .then(function (response) {
                    if(confirm("Are you sure you want to warn user: " + response.data.user.username)){
                        var xhr = new XMLHttpRequest();
                        xhr.open("POST", "/warn", true);
                        xhr.setRequestHeader('Content-Type', 'application/json');
                        xhr.send(JSON.stringify({
                            'user_id': hidden_id.value,
                            'reason': reason_field.value,
                        }));
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
            }
            else
            {
                axios.get('/api/get/user/' + hidden_id.value)
                .then(function (response) {
                    if(confirm("Are you sure you want to mute user: " + response.data.user.username)){
                        var xhr = new XMLHttpRequest();
                        xhr.open("POST", "/mute", true);
                        xhr.setRequestHeader('Content-Type', 'application/json');
                        xhr.send(JSON.stringify({
                            'user_id': hidden_id.value,
                            'reason': reason_field.value,
                        }));
                    }
                })
                .catch(function (error) {
                    console.log(error);
                });
            }
        }
    }
}

function showResults(val) {
  if (val == '') {
    return;
  }
  let list = '';
  fetch('/api/search/members/' + val).then(
   function (response) {
     return response.json();
   }).then(function (data) {
       names = [];
        let autodiv = document.getElementById("autocomp");
        autodiv.innerHTML = "";
       for (var user of data) 
        {
            let text_el = document.createElement("p");
            text_el.innerHTML = user['user']['username'];
            text_el.className="user_button";
            text_el.id = user['user']['id'];
            text_el.onclick = function()
            {
                console.log(text_el.innerText);
                console.log(text_el.id);
                source.value = text_el.innerText;
                hidden_id.value = text_el.id;

                autodiv.innerHTML = "";
            }
            autodiv.appendChild(text_el);
        }
     return true;
   }).catch(function (err) {
     console.warn('Something went wrong.', err);
     return false;
   });
}

const inputHandler = function(e) {
  showResults(e.target.value)
}

const source = document.getElementById('selector');
source.addEventListener('input', inputHandler);