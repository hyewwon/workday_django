
document.addEventListener('DOMContentLoaded', function() {
  var events = [];
  $.ajax({
    type:"GET",
    url:"/api/vacation/",
    headers:{
      'Authorization': `Bearer ${getCookie("access_token")}`
    },
    success : function(data){
      data.vacation.forEach(e => {
        events.push({
          "title" : `[${e.department__name}] ${e.user__last_name}`,
          "start": e.start_date,
          "end": e.end_date
        })
      });
      var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'dayGridMonth',
          events: events
        });
        calendar.render();
      
    },
    error : function(error){
      alert("데이터 로딩 실패...");
      var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'dayGridMonth',
          events: events
        });
        calendar.render();
    }
  })
});

const start_date = document.getElementById("start-date");
const end_date = document.getElementById("end-date");
const regist_type = document.getElementById("regist-type");
let request_type = "POST";

function registVacation(){
  if(start_date.value == ""){
    start_date.focus();
    return false;
  }
  if(start_date.value >= end_date.value){
    alert("시작일을 더 빠르게 설정해주세요.");
    return false;
  }
  const today = getTodayDate();
  if(today >= start_date.value){
    alert("오늘 날짜보다 늦게 설정해주세요.");
    return false;
  }
  if(regist_type.value == "2"){
    request_type = "PUT";
  }
  if(!confirm("저장하시겠습니까?")){
    return false;
  }
  const data = new FormData(document.getElementById("vacationForm"));
  $.ajax({
    type:request_type,
    url:"/api/vacation/",
    headers:{
      'X-CSRFToken': csrftoken,
      'Authorization': `Bearer ${getCookie("access_token")}`
    },
    data: data,
    enctype : "multipart/form-data",
    processData : false,
    contentType : false,
    success : function(data){
      location.reload();
    },
    error : function(error){
      alert("저장 실패..");
    }
  })
}

function deleteDate(vac_id){
  if(!confirm("정말 삭제하시겠습니까?")){
    return false;
  }
  console.log(vac_id)
  $.ajax({
    type:"DELETE",
    url:"/api/vacation-delete/",
    headers:{
      'X-CSRFToken': csrftoken,
      'Authorization': `Bearer ${getCookie("access_token")}`
    },
    data: {"vacation_id" : vac_id},
    success : function(data){
      location.reload();
    },
    error : function(error){
      alert("삭제 실패..");
    }
  })

}

function changeForm(){
  const regist_type = document.getElementById("regist-type");
  if(regist_type.value == "2"){
    start_date.value = "";
    end_date.value = "";
    document.getElementById("user_vacation_table").hidden = false;
    document.getElementById("date-form").hidden = true;
  }else{
    start_date.value = "";
    end_date.value = "";
    document.getElementById("user_vacation_table").hidden = true;
    document.getElementById("date-form").hidden = false;
  }
}


function getDateForm(vac_id, vac_start_date, vac_end_date){
  document.getElementById("vacation-id").value = vac_id;
  start_date.value = vac_start_date;
  end_date.value = vac_end_date;
  document.getElementById("date-form").hidden = false;
}

function getTodayDate(){
  var today = new Date();

  var year = today.getFullYear();
  var month = ('0' + (today.getMonth() + 1)).slice(-2);
  var day = ('0' + today.getDate()).slice(-2);
  var dateString = year + '-' + month  + '-' + day;
  return dateString
}