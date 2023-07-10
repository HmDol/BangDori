const email_box = document.querySelector("#regEmail"),
    year_box = document.querySelector("#register_user_year"),
    month_box = document.querySelector("#register_user_month"),
    day_box = document.querySelector("#register_user_day"),
    select_email_box = document.querySelector(".select-email-box"),
    input_email_box = document.querySelector(".input-email-box");

const DIRECT = "hidden";

function setAddress() {
    let option;

    let address = [
        {value: 'gmail.com', register_user_email: 'gmail.com'},
        {value: 'naver.com', register_user_email: 'naver.com'},
        {value: 'daum.com', register_user_email: 'daum.com'},
        {value: 'kakao.com', register_user_email: 'kakao.com'},
        {value: 'direct', register_user_email: '직접 입력'},
    ];

    address.unshift({value: '', register_user_email: '주소 선택'});

    for (const addr of address) {
        option = document.createElement("option");
        option.value = addr.value;
        option.innerText = addr.register_user_email;
        email_box.appendChild(option);
    }
}

function setBirth() {
    let option;

    for (let i = 1970; i <= 2022; i++) {
        option = document.createElement("option");
        option.value = i.toString();
        option.innerText = i.toString();
        year_box.appendChild(option);
    }
    for (let i = 1; i <= 12; i++) {
        option = document.createElement("option");
        option.value = i.toString().padStart(2, 0);
        option.innerText = i.toString();
        month_box.appendChild(option);
    }
    for (let i = 1; i <= 31; i++) {
        option = document.createElement("option");
        option.value = i.toString().padStart(2, 0);
        option.innerText = i.toString();
        day_box.appendChild(option);
    }
}

function changeEmail(event) {
    if (event.target.value === 'direct') {
        // console.log("yes");
        select_email_box.innerText = "";

        select_email_box.classList.add(DIRECT);
        input_email_box.classList.remove(DIRECT);
    } else {
        input_email_box.value = "";

        input_email_box.classList.add(DIRECT);
        select_email_box.classList.remove(DIRECT);

        select_email_box.innerText = event.target.value;
    }
}

function init() {
    setAddress();
    setBirth();
    email_box.addEventListener("change", changeEmail);
}

init();