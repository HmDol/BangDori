const move_btn = document.querySelector(".testABC"),
    dabang_board = document.querySelector(".dabang_board"),
    comparing_house_box = document.querySelector(".house-section");

const MOVE_BOARD = "moving-board";
const SHOW_HOUSE_BOX = "show-house-box";

function moveBoard(event){
    dabang_board.classList.add(MOVE_BOARD);
    comparing_house_box.classList.add(SHOW_HOUSE_BOX);
}

function init() {
    move_btn.addEventListener("click", moveBoard);
}

init();