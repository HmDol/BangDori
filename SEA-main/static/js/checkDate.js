const dates = document.querySelectorAll(".js-date");

function checkBoardDate() {
    const now = new Date();

    dates.forEach(date => {
        const tmp = date.innerHTML.split(/[년|월|일| ]/);

        const board_time = tmp.filter(i => {
            return i !== '';
        }) 

        if(now.getFullYear() > parseInt(board_time[0])) {
            date.innerHTML = `${now.getFullYear() - parseInt(board_time[0])}년 전`;
        } else if(now.getMonth() > parseInt(board_time[1])) {
            date.innerHTML = `${now.getMonth() - parseInt(board_time[1])}달 전`;
        } else if(now.getDate() > parseInt(board_time[2])) {
            date.innerHTML = `${now.getDate() - parseInt(board_time[2])}일 전`;
        } else {
            if(board_time[4] === '오전') {
                const t = board_time[3].split(':');
                if(t[0] >= 1 && t[0] < 10){
                    t[0] = `0${parseInt(t[0])}`;
                }
                board_time[3] = t.join(":");
                date.innerHTML = board_time[3];
            } else {
                const t = board_time[3].split(':');
                if(t[0] != 12){
                    t[0] = `${parseInt(t[0]) + 12}`;
                }
                else{
                    t[0] = `0${parseInt(t[0]) - 12}`;
                }
                board_time[3] = t.join(":");
                date.innerHTML = board_time[3];
            }
        }
    })
}

function init() {
    checkBoardDate();
}

init();
