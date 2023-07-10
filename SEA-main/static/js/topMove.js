const top_move_btn = document.querySelector(".scroll-top-btn");

const VISIBLE2 = "visible";

function checkOnload() {
    window.onload = function() {
        setTimeout (function () {
        scrollTo(0, 0);
        }, 100);
    }
}

function checkTopMove(){
    if(window.scrollY >= 116) {
        top_move_btn.classList.add(VISIBLE2);
    } else {
        top_move_btn.classList.remove(VISIBLE2);
    }
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    })
}

function init() {
    checkTopMove();
    checkOnload();
    top_move_btn.addEventListener("click", scrollToTop);
    setInterval(checkTopMove, 500);
}

init();