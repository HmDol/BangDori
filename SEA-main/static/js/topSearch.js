const body = document.querySelector("body"),
  top_search = body.querySelector(".top-search-form"),
  search = top_search.querySelector(".search"),
  reset = top_search.querySelector(".reset"),
  keyword = top_search.querySelector(".top-search-keyword");

const SHOWING_BOARD = "showing-board";
const VISIBLE = "visible";

function handleClick(event) {
  if (event.target.classList.contains("top-search-keyword")) {
    top_search.classList.add(SHOWING_BOARD);
  } else {
    top_search.classList.remove(SHOWING_BOARD);
  }
}

function loadCancel() {
  if (keyword.value != "") {
    reset.classList.add(VISIBLE);
  } else {
    reset.classList.remove(VISIBLE);
  }
}

function searchKeyword() {
  location.href = "/?search_keyword=" + `${keyword.value}`;
}

function resetKeyword() {
  keyword.value = "";
}

function init() {
  body.addEventListener("click", handleClick);
  loadCancel();
  setInterval(loadCancel, 100);
}

init();
