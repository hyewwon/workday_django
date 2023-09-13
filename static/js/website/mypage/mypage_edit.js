const user_name = document.getElementById("user-name");
const email = document.getElementById("email");
const phone_no = document.getElementById("phone-no");
const note = document.getElementById("note");
const user_name_feedback = document.getElementById("user-name-feedback");
const email_feedback = document.getElementById("email-feedback");
const phone_no_feedback = document.getElementById("phone-no-feedback");
const check_dupl_email = document.getElementById("check-dupl-email");
const btn_edit = document.getElementById("btn-edit");
const original_email = document.getElementById("original_email");

const old_password = document.getElementById("old-password");
const new_password1 = document.getElementById("new-password1");
const new_password2 = document.getElementById("new-password2");
const old_password_error = document.getElementById("old-password-error");
const new_password1_error = document.getElementById("new-password1-error");
const new_password2_error = document.getElementById("new-password2-error");
const btn_password_edit = document.getElementById("btn-password-edit");
const btn_modal = document.getElementById("btn_modal");

function resetModal(){
    old_password.value = "";
    new_password1.value = "";
    new_password2.value = "";
    old_password_error.innerText = "";
    new_password1_error.innerText = "";
    new_password2_error.innerText = "";
}


let checked_email = false;

function editUser(){
    if(!validation()){
        return false;
    }
    if(!confirm("수정하시겠습니까?")){
        return false;
    }
    btn_edit.disabled = true;
    const data = new FormData(document.getElementById("editForm"));
    $.ajax({
        type:"PUT",
        url:"/api/mypage-edit/",
        headers: {
            'X-CSRFToken': csrftoken,
            'Authorization': `Bearer ${getCookie("access_token")}`
        },
        data : data,
        enctype : "multipart/form-data",
        processData : false,
        contentType : false,
        success: function(data){
            alert(data.message);
            location.href = data.next;
        },
        error :function(error){
            alert(error.responseJSON.message);
            btn_edit.disabled = false;
        }
    })

}

// 이메일 중복검사
check_dupl_email.addEventListener("click", () =>{
    if(email.value == original_email.value){
        email_feedback.innerText = "새로운 이메일로 변경 후 검사해 주세요";
        email_feedback.style.color = "red";
        return false;
    }
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

function editPassword(){
    if(!passwordValidation()){
        return false;
    }
    if(!confirm("변경하시겠습니까?")){
        return false;
    }
    btn_password_edit.disabled = true;
    const data = new FormData(document.getElementById("editPasswordForm"));
    $.ajax({
        type:"PUT",
        url:"/api/mypage-password-edit/",
        headers: {
            'X-CSRFToken': csrftoken,
            'Authorization': `Bearer ${getCookie("access_token")}`
        },
        data : data,
        enctype : "multipart/form-data",
        processData : false,
        contentType : false,
        success: function(data){
            alert(data.message);
            location.reload();
        },
        error :function(error){
            alert(error.responseJSON.message);
            btn_password_edit.disabled = false;
        }
    })

}


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


// 전체 유효성 검사
function validation(){
    if(user_name.value==""){
        user_name_feedback.innerText = "이름을 입력해주세요";
        user_name_feedback.style.color = "red";
        user_name.focus();
        return false;
    }

    if(!checkEmail()){
        return false;
    }
    if(!checked_email && (email.value != original_email.value)){
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


function passwordValidation(){
    if(old_password.value == ""){
        old_password_error.innerText = "현재 사용중인 비밀번호를 입력해 주세요";
        old_password_error.style.color = "red";
        return false;
    }
    if(new_password1.value == ""){
        new_password1_error.innerText = "새로운 비밀번호를 입력해 주세요";
        new_password1_error.style.color = "red";
        return false;
    }
    if(new_password2.value == ""){
        new_password2_error.innerText = "새로운 비밀번호 확인을 입력해 주세요";
        new_password2_error.style.color = "red";
        return false;
    }

    return true;
}


user_name.oninput = function(){
    user_name_feedback.innerHTML = "";
}

email.oninput = function(){
    email_feedback.innerHTML = "";
    email_feedback.style.color = "black";
    checked_email = false;
}

phone_no.oninput = function(){
    phone_no_feedback.innerHTML = "";
}

old_password.oninput = function(){
    old_password_error.innerHTML = "";
}

new_password1.oninput = function(){
    new_password1_error.innerHTML = "";
}

new_password2.oninput = function(){
    new_password2_error.innerHTML = "";
}