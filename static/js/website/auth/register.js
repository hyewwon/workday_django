const membername = document.getElementById("membername");
const email = document.getElementById("email");
const password = document.getElementById("password");
const check_password = document.getElementById("check-password");
const phone_no = document.getElementById("phone-no");
const company = document.getElementById("company");
const department = document.getElementById("department");
const image = document.getElementById("image");

const check_dupl_email = document.getElementById("check-dupl-email");
const btn_submit = document.getElementById("btn-submit");

const membername_feedback = document.getElementById("membername-feedback");
const email_feedback = document.getElementById("email-feedback");
const password_feedack = document.getElementById("password-feedback");
const check_password_feedback = document.getElementById("check-password-feedback");
const phone_no_feedback = document.getElementById("phone-no-feedback");
const company_feedback = document.getElementById("company-feedback");
const department_feedback = document.getElementById("department-feedback");
const image_feedback = document.getElementById("image-feedback");

let checked_email = false;

// 이메일 중복검사
check_dupl_email.addEventListener("click", async () =>{
    if(!checkEmail()){
        return false;
    }
    check_dupl_email.disabled = true;
    email.disabled = true;
    try{
        const response = await fetch("/api/check-email/", {
            method: "POST",
            headers : {'X-CSRFToken': csrftoken, "Content-Type":"application/json" },
            body : JSON.stringify({
                "email" : email.value
            })
        })
        const result = await response.json();
        if(response.status != 200){
            check_dupl_email.disabled = false;
            email.disabled = false;
            email_feedback.innerText = "중복된 이메일 입니다.";
            email_feedback.style.color = "red";
            email.focus();
        }else{
            check_dupl_email.disabled = false;
            email.disabled = false;
            email_feedback.innerText = "사용가능한 이메일 입니다.";
            email_feedback.style.color = "green";
            email.focus();
            checked_email = true;
        }
    }
    catch(error){
        alert(error);
    }
})


// 가입
btn_submit.addEventListener("click", async () =>{
    if(!validation()){
        return false;
    }
    btn_submit.disabled = true;
    const data = new FormData(document.getElementById("registerForm"));
    try{
        const response = await fetch("/api/registration/", {
            method: "POST",
            headers : {'X-CSRFToken': csrftoken},
            body : data
        })
        const result = await response.json();
        if(response.status != 201){
            alert(result.message);
            btn_submit.disabled = false;
        }else{
            alert(result.message);
            location.href = "/login/";
        }
    }
    catch(error){
        alert(error);
    }
})


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
    
    if(!checkEmail()){
        return false;
    }
    if(!checked_email){
        email_feedback.innerText = "이메일 중복검사를 해주세요";
        email_feedback.style.color = "red";
        email.focus();
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

    if(phone_no.value == ""){
        phone_no_feedback.innerText = "전화번호를 입력해 주세요."
        phone_no_feedback.style.color = "red";
        return false;
        
    }if(company.value == ""){
        company_feedback.innerText = "회사명을 선택해주세요."
        return false;
        
    }if(department.value == ""){
        department_feedback.innerText = "부서명을 선택해 주세요."
        return false;
    }
    
    return true;
    
}

async function getDepartmentList(){
    company_feedback.innerHTML = "";
    department.innerHTML ="";
    const selected_company = document.getElementById("company");
    try{
        const response = await fetch(`/api/department-list/${selected_company.value}/`, {
            method: "GET"
        })
        const result = await response.json();
        if(result.success == false){
            alert(result.message);
        }else{
            document.getElementById("departmentSelect").style.display = "block";

            let default_option = document.createElement("option");
            default_option.setAttribute("value", "");
            default_option.innerHTML = "부서명을 선택해주세요."
            default_option.selected = true;
            default_option.disabled = true;
            department.appendChild(default_option);
            for (let index = 0; index < result.length; index++) {
                let option = document.createElement("option");
                option.setAttribute("value", result[index].id);
                option.innerHTML = result[index].name;
                department.appendChild(option);
            }     
        }
    }
    catch(error){
        alert(error);
    }
}


membername.oninput = function(){
    membername_feedback.innerHTML = "";
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
department.onchange = function(){
    department_feedback.innerHTML = "";
}
check_password.oninput = function(){
    image_feedback.innerHTML = "* 얼굴이 나오는 이미지를 입력해주세요";
    image_feedback.style.color = "black";
}
