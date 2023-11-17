const email = document.getElementById("email");
const password = document.getElementById("password");
const email_feedback = document.getElementById("email-feedback");
const password_feedback = document.getElementById("password-feedback");
const btn_login = document.getElementById("btn-login");

btn_login.addEventListener("click", async function(){
    if(!validation()){
        return false;
    }
    btn_login.disabled = true;
    try{
        const response = await fetch("/api/login/", {
            method: "POST",
            headers : {'X-CSRFToken': csrftoken, "Content-Type":"application/json" },
            body : JSON.stringify({
                "email": email.value,
                "password" : password.value,
                "login_type" : "workday"
            })
        })
        const result = await response.json();
        if(response.status != 200){
            alert(result.message);
            btn_login.disabled = false;
        }else{
            setCookie("access_token", result.jwt_token.access_token, tokenPayload(result.jwt_token.access_token).exp);
            setCookie("refresh_token_index_id", result.jwt_token.refresh_token_index_id, result.jwt_token.refresh_token_exp);
            const URLSearch = new URLSearchParams(location.search);
            if(URLSearch.has('next')){
                location.href = location.search.split('?next=')[1];
            }else{
                location.href = "/";
            }
        }
    }
    catch(error){
        alert(error);
    }
})

async function GoogleLogin(){
    btn_login.disabled = true;
    try{
        const response = await fetch("/api/oauth/google/login/", {
            method: "GET"
        })
        const result = await response.json();
        if(response.status != 200){
            alert(result.message);
            btn_login.disabled = false;
        }else{
            setCookie("access_token", result.jwt_token.access_token, tokenPayload(result.jwt_token.access_token).exp);
            setCookie("refresh_token_index_id", result.jwt_token.refresh_token_index_id, result.jwt_token.refresh_token_exp);
            const URLSearch = new URLSearchParams(location.search);
            if(URLSearch.has('next')){
                location.href = location.search.split('?next=')[1];
            }else{
                location.href = "/";
            }
        }
    }
    catch(error){
        alert(error);
    }
}


function validation(){
    if(email.value == ""){
        email_feedback.innerText = "이메일을 입력해 주세요.";
        email_feedback.style.color = "red";
        return false;
    }
    if(password.value == ""){
        password_feedback.innerText = "비밀번호를 입력해 주세요.";
        password_feedback.style.color = "red";
        return false;
    }

    return true;
}


email.oninput = function(){
    email_feedback.innerHTML = "";
}

password.oninput = function(){
    password_feedback.innerHTML = "";
}
