function page(num){
    let urlParams = new URLSearchParams(window.location.search);
    urlParams.set('page', num);
    window.location.href = `?${urlParams.toString()}`;
}

// api용 pagination
function setPagination(page, pagelist){
    const pagination = document.getElementById("pagination");
    let html = ``
    // 이전페이지
    if(page != pagelist[0]){
        html += `
            <li class="page-item">
                <a class="page-link" href="javascript:;" onclick="page(${Number(page)-1})">이전</a>
            </li>
        `
    } else{
        html += `
            <li class="page-item disabled">
                <a class="page-link" tabindex="-1" aria-disabled="true" href="javascript:;">이전</a>
            </li>
        `
    }
    // 페이지 리스트
    for(let i=0; i<pagelist.length; i++){
        if(pagelist[i] == page){
            html+=`
                <li class="page-item active" aria-current="page">
                    <a class="page-link" href="javascript:;">${Number(page)}</a>
                </li>
            `
        }
        else{
            if(pagelist[i] == '…'){
                html += `
                    <li class="page-item"><span class="page-link" style="cursor: pointer;">${pagelist[i]}</span></li>
                `
            }
            else{
                html += `
                    <li class="page-item">
                        <a class="page-link" href="javascript:;" onclick="page(${Number(pagelist[i])})">${pagelist[i]}</a>
                    </li>
                `
            }
        }
    }
    // 다음페이지
    if(page != pagelist[pagelist.length-1]){
        html += `
            <li class="page-item">
                <a class="page-link" href="javascript:;" onclick="page(${Number(page)+1})">다음</a>
            </li>
        `
    } else{
        html += `
            <li class="page-item disabled">
                <a class="page-link" tabindex="-1" aria-disabled="true" href="javascript:;">다음</a>
            </li>
        `
    }
    pagination.innerHTML = html;
}
