document.addEventListener("DOMContentLoaded", function(){
    const today = getToday();
    if(document.getElementById("today")){
        document.getElementById("today").innerHTML = `${today[0]}년 ${today[1]}월 ${today[2]}일`
        document.getElementById("month").innerHTML = `${today[0]}년 ${today[1]}월`
    }

    // 회사 위도 경도
    const latitude = 37.50831227647185;
    const longitude = 127.11131230010045;

    window.navigator.geolocation.getCurrentPosition(
        function(position){
            alert(position.coords.latitude)
            alert(position.coords.longitude)
            alert(Math.floor(position.coords.accuracy))
        }
    )


});


function getTime(){
    const today = new Date();
    let h = today.getHours();
    let m = today.getMinutes();
    let s = today.getSeconds();

    return [h, m >= 10 ? m : "0" + m, s >= 10 ? s : "0" + s]
}

function getToday(){
    const today = new Date();
    let Y = today.getFullYear();
    let M = today.getMonth() + 1;
    let D = today.getDate();
    
    return [Y, M >= 10 ? M : "0" + M, D >= 10 ? D : "0" + D]
}

function checkAttendance(){
    const current_time = getTime();
    $.ajax({
        type:"POST",
        url:"/api/attendance/",
        headers:{
            'X-CSRFToken': csrftoken,
            'Authorization': `Bearer ${getCookie("access_token")}`
        },
        data:{
            "time" : `${current_time[0]}시 ${current_time[1]}분 ${current_time[2]}초`,          
            "attend_id" : ""
        },
        success : function(data){
            alert("출근체크 되었습니다.");
            const attendance_time = document.getElementById("attendance-time");
            const leave_time = document.getElementById("leave-time");
            attendance_time.innerHTML = `<span>${current_time[0]}시 ${current_time[1]}분 ${current_time[2]}초</span><span class="badge border-success border-1 text-success">출근</span>`;
            leave_time.innerHTML = `<button class="btn btn-danger btn-sm" onclick="checkLeave(${data.attend_id});">퇴근</button>`
        },
        error : function(error){
          alert(`체크 실패.. (출근 체크 시간 : ${current_time[0]}시 ${current_time[1]}분 ${current_time[2]}초)`);
        }
    })
}


function checkLeave(attend_id){
    const current_time = getTime();
    $.ajax({
        type:"POST",
        url:"/api/attendance/",
        headers:{
            'X-CSRFToken': csrftoken,
            'Authorization': `Bearer ${getCookie("access_token")}`
        },
        data:{
            "time" : `${current_time[0]}시 ${current_time[1]}분 ${current_time[2]}초`,          
            "attend_id" : attend_id
        },
        success : function(data){
            alert("퇴근체크 되었습니다.");
            location.reload();
        },
        error : function(error){
          alert(`체크 실패.. (퇴큰 체크 시간 : ${current_time[0]}시 ${current_time[1]}분 ${current_time[2]}초)`);
        }
    })
}


