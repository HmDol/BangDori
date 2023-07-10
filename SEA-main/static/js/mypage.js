function changeMenu() {
    var path = window.location.pathname;
    const previous_menu = document.querySelector(".clicked");
    
    document.querySelector("#myinfo-list").addEventListener("click", (e) => {
        previous_menu.classList.remove(".clicked");
        window.location.href = "/profiles/myinfo";
        document.querySelector("#myinfo-list").classList.add(".clicked");
    })

    document.querySelector("#mynotice-list").addEventListener("click", (e) => {
        previous_menu.classList.remove(".clicked");
        window.location.href = "/profiles/mypost";
        document.querySelector("#mynotice-list").classList.add(".clicked");
    })

    document.querySelector("#bookmark-list").addEventListener("click", (e) => {
        previous_menu.classList.remove(".clicked");
        document.querySelector("#bookmark-list").classList.add(".clicked");
        window.location.href = "/profiles/favorites";
    })

    document.querySelector("#address-list").addEventListener("click", (e) => {
        previous_menu.classList.remove(".clicked");
        document.querySelector("#address-list").classList.add(".clicked");
        window.location.href = "/profiles/address";
    })

    document.querySelector("#corporate-list").addEventListener("click", (e) => {
        previous_menu.classList.remove(".clicked");
        document.querySelector("#corporate-list").classList.add(".clicked");
        window.location.href = "/profiles/corporate";
    })
}

function init() {
    changeMenu();
}

init();