const membername = document.getElementById("membername");
const username = document.getElementById("username");
const email = document.getElementById("email");
const password = document.getElementById("password");
const check_password = document.getElementById("check-password");
const phone_no = document.getElementById("phone-no");
const department = document.getElementById("department");

const check_dupl_username = document.getElementById("check-dupl-username");
const check_dupl_email = document.getElementById("check-dupl-email");
const btn_submit = document.getElementById("btn-submit");

const membername_feedback = document.getElementById("membername-feedback");
const username_feedback = document.getElementById("username-feedback");
const email_feedback = document.getElementById("email-feedback");
const password_feedack = document.getElementById("password-feedback");
const check_password_feedback = document.getElementById("check-password-feedback");
const phone_no_feedback = document.getElementById("phone-no-feedback");

let checked_id = false;
let checked_email = false;

// 아이디 중복검사
check_dupl_username.addEventListener("click", () =>{
    if(!checkID()){
        return false;
    }
    check_dupl_username.disabled = true;
    username.disabled = true;
    $.ajax({
        type:"POST",
        url:"/api/check-username/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data : {
            "username" : username.value
        },
        success : function(data){
            check_dupl_username.disabled = false;
            username.disabled = false;
            username_feedback.innerText = data.message;
            username_feedback.style.color = "green";
            checked_id = true;
        },
        error: function(error){
            check_dupl_username.disabled = false;
            username.disabled = false;
            username_feedback.innerText = error.responseJSON.message;
            username_feedback.style.color = "red";
            username.focus();
        }
    })
    
})

// 이메일 중복검사
check_dupl_email.addEventListener("click", () =>{
    if(!checkEmail()){
        return false;
    }
    check_dupl_email.disabled = true;
    email.disabled = true;
    $.ajax({
        type:"POST",
        url:"/api/check-email/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data : {
            "email" : email.value
        },
        success: function(data){
            check_dupl_email.disabled = false;
            email.disabled = false;
            email_feedback.innerText = "사용가능한 이메일 입니다.";
            email_feedback.style.color = "green";
            email.focus();
            checked_email = true;
        },
        error :function(error){
            check_dupl_email.disabled = false;
            email.disabled = false;
            email_feedback.innerText = "중복된 이메일 입니다.";
            email_feedback.style.color = "red";
            email.focus();
        }
    })
})


// 가입
btn_submit.addEventListener("click", () =>{
    if(!validation()){
        return false;
    }
    btn_submit.disabled = true;
    const data = new FormData(document.getElementById("registerForm"));
    $.ajax({
        type:"POST",
        url:"/api/registration/",
        headers: {
            'X-CSRFToken': csrftoken
        },
        data : data,
        enctype : "multipart/form-data",
        processData : false,
        contentType : false,
        success: function(data){
            alert(data.message);
            location.href = "/login/";
        },
        error :function(error){
            alert(error.responseJSON.message);
            btn_submit.disabled = false;
        }
    })
})

// 아이디 유효성검사
function checkID(){
    let reg_id = /^[a-z]+[a-z0-9]{5,19}$/g;
    if(username.value == ""){
        username_feedback.innerText = "아이디를 입력해주세요";
        username_feedback.style.color = "red";
        username.focus();
        return false;
    }
    if(!reg_id.test(username.value)){
        username_feedback.innerText = "영문자로 시작하는 6~20자 영문자 또는 숫자이어야 합니다.";
        username_feedback.style.color = "red";
        username.focus();
        return false;
    }

    if(username.value.includes("admin")){
        username_feedback.innerText = "'admin'이란 단어를 포함 할 수 없습니다."
        username_feedback.style.color = "red";
        username.focus();
        return false;
    }
    
    return true;
}

//이메일 유효성 검사
function checkEmail(){
    let reg_email = /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/;
    if(email.value == ""){
        email_feedback.innerText = "이메일을 입력해주세요";
        email_feedback.style.color = "red";
        email.focus();
        return false;
    }
    if(!reg_email.test(email.value)){
        email_feedback.innerText = "잘못된 이메일 형식입니다";
        email_feedback.style.color = "red";
        email.focus();
        return false;
    }
    return true;
}


//비밀번호 유효성 검사
function checkPassword(){
    let reg_password = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()+.,~]{8,16}$/
    let checkNum = password.value.search(/[0-9]/g); // 숫자사용
    let checkEng = password.value.search(/[a-z]/ig); // 영문사용
    if(password.value == ""){
        password_feedack.innerText = "비밀번호를 입력해주세요";
        password_feedack.style.color = "red";
        password.focus();
        return false;
    }
    if(!reg_password.test(password.value)){
        password_feedack.innerText = "숫자와 영문자 조합으로 8~16자리를 사용해야 합니다.";
        password_feedack.style.color = "red";
        password.focus();
        return false;
    }
    if(checkNum < 0 || checkEng < 0){
        password_feedack.innerText = "숫자와 영문자를 조합하여야 합니다";
        password_feedack.style.color = "red";
        password.focus();
        return false;
    }

    return true;
}


// 전체 유효성 검사
function validation(){
    if(membername.value==""){
        membername_feedback.innerText = "이름을 입력해주세요";
        membername_feedback.style.color = "red";
        membername.focus();
        return false;
    }
    if(!checkID()){
        return false;
    }
    if(!checked_id){
        username_feedback.innerText = "아이디 중복검사를 해주세요";
        username_feedback.style.color = "red";
        username.focus();
        return false;
    }
    if(!checkPassword()){
        return false;
    }
    if(check_password.value == ""){
        check_password_feedback.innerText = "비밀번호 확인을 입력해주세요";
        check_password_feedback.style.color = "red";
        check_password.focus();
        return false;
    }
    if(password.value != check_password.value){
        check_password_feedback.innerText = "비밀번호가 일치하지 않습니다";
        check_password_feedback.style.color = "red";
        check_password.focus();
        return false;
    }
    
    if(!checkEmail()){
        return false;
    }
    if(!checked_email){
        email_feedback.innerText = "이메일 중복검사를 해주세요";
        email_feedback.style.color = "red";
        email.focus();
        return false;
    }

    if(phone_no.value == ""){
        phone_no_feedback.innerText = "전화번호를 입력해 주세요."
        phone_no_feedback.style.color = "red";
        return false;
    
    }
    return true;
    
}

membername.oninput = function(){
    membername_feedback.innerHTML = "";
}
username.oninput = function(){
    username_feedback.innerHTML = "영문자로 시작하는 6~20자 영문자 또는 숫자이어야 합니다.";
    username_feedback.style.color = "black";
    checked_id = false;
}
email.oninput = function(){
    email_feedback.innerHTML = "";
    email_feedback.style.color = "black";
    checked_email = false;
}
password.oninput = function(){
    password_feedack.innerHTML = "숫자와 영문자 조합으로 8~16자리를 사용해야 합니다.";
    password_feedack.style.color = "black";
}
check_password.oninput = function(){
    check_password_feedback.innerHTML = "";
}
phone_no.oninput = function(){
    phone_no_feedback.innerHTML = "";
}