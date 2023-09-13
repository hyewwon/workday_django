const board_type = document.getElementById("board-type");
const title = document.getElementById("title");
const content = document.getElementById("content");
const anony_flag = document.getElementById("anony-flag");
const board_type_feedback = document.getElementById("board-type-feedback");
const title_feedback = document.getElementById("title-feedback");
const content_feedback = document.getElementById("content-feedback");

const btn_edit = document.getElementById("btn-save");

function saveBoard(){
    if(!validation()){
        return false;
    }
    if(!confirm("작성하시겠습니까?")){
        return false;
    }
    btn_edit.disabled = true;
    const data = new FormData(document.getElementById("createForm"));
    data.append("anonymous_flag", anony_flag.checked == true ? "1" : "0");
    $.ajax({
        type:"POST",
        url:"/api/free-board-create/",
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
            // location.href = data.next;
        },
        error :function(error){
            alert(error.responseJSON.message);
            btn_edit.disabled = false;
        }
    })

}


// 유효성 검사
function validation(){
    if(board_type.value==""){
        board_type_feedback.innerText = "글 분류를 선택해 주세요.";
        board_type_feedback.style.color = "red";
        board_type.focus();
        return false;
    }

    if(title.value == ""){
        title_feedback.innerText = "제목을 입력해 주세요."
        title_feedback.style.color = "red";
        return false;
    
    }

    if(content.value == ""){
        content_feedback.innerText = "내용을 입력해 주세요."
        content_feedback.style.color = "red";
        return false;
    
    }
    
    return true;
}



board_type.oninput = function(){
    board_type_feedback.innerHTML = "";
}

title.oninput = function(){
    title_feedback.innerHTML = "";
}

content.oninput = function(){
    content_feedback.innerHTML = "";
}
