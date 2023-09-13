const username = document.getElementById("username");
const password = document.getElementById("password");
const username_feedback = document.getElementById("username-feedback");
const password_feedback = document.getElementById("password-feedback");
const btn_login = document.getElementById("btn-login");

btn_login.addEventListener("click", function(){
    if(!validation()){
        return false;
    }
    btn_login.disabled = true;
    $.ajax({
        type:"POST",
        url:"/api/login/",
        headers: {'X-CSRFToken': csrftoken},
        data:{
            "username": username.value,
            "password" : password.value
        },
        success : function(data){
            setCookie("access_token", data.jwt_token.access_token, tokenPayload(data.jwt_token.access_token).exp);
            setCookie("refresh_token_index_id", data.jwt_token.refresh_token_index_id, data.jwt_token.refresh_token_exp);
            const URLSearch = new URLSearchParams(location.search);
            if(URLSearch.has('next')){
                location.href = location.search.split('?next=')[1];
            }else{
                location.href = "/";
            }
        },
        error: function(error){
            alert(error.responseJSON.message);
            btn_login.disabled = false;
        }
    })
})


function validation(){
    if(username.value == ""){
        username_feedback.innerText = "아이디를 입력해 주세요.";
        username_feedback.style.color = "red";
        return false;
    }
    if(password.value == ""){
        password_feedback.innerText = "비밀번호를 입력해 주세요.";
        password_feedback.style.color = "red";
        return false;
    }

    return true;
}


username.oninput = function(){
    username_feedback.innerHTML = "";
}

password.oninput = function(){
    password_feedback.innerHTML = "";
}
