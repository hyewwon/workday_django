const membername = document.getElementById("membername");
const company = document.getElementById("company");
const department = document.getElementById("department");

const btn_submit = document.getElementById("btn-submit");

const membername_feedback = document.getElementById("membername-feedback");
const company_feedback = document.getElementById("company-feedback");
const department_feedback = document.getElementById("department-feedback");


// 가입
btn_submit.addEventListener("click", async () =>{
    if(!validation()){
        return false;
    }
    if(!confirm("신청하시겠습니까?")){
        return false;
    }
    btn_submit.disabled = true;
    const data = new FormData(document.getElementById("registerForm"));
    const url = new URLSearchParams(location.search);
    data.append("access_token", url.get("access_token"))
    try{
        const response = await fetch("", {
            method: "POST",
            headers : {'X-CSRFToken': csrftoken},
            body : data
        })
        const result = await response.json();
        if(result.success == false){
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


// 전체 유효성 검사
function validation(){
    if(membername.value==""){
        membername_feedback.innerText = "이름을 입력해주세요";
        membername_feedback.style.color = "red";
        membername.focus();
        return false;
    }
    
    if(company.value == ""){
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
department.onchange = function(){
    department_feedback.innerHTML = "";
}