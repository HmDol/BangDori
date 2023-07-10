const banner_content = document.querySelector(".banner-content"),
    banner = document.querySelector(".banner"),
    banner_count = document.querySelector(".banner-count"),
    counts = document.querySelectorAll(".count");

const SHOWING = "showing",
    CLICKED_BANNER = "js-clicked-count";

let mode = 'auto';

function handleClick() {
    counts.forEach(count => {
        count.addEventListener("click", (event) => {
            const current_slide = banner_content.querySelector(`.${SHOWING}`);
            const current_count = banner_count.querySelector(`.${CLICKED_BANNER}`);
            const click_count = event.target.classList[0];
            mode = 'click';
            if(current_count.classList.contains(click_count)) {
                null;
            } else {
                showBanner(current_slide, current_count, click_count);
            }
        });
    })
}

function showBanner(current_slide, current_count, click_count){
    const clicked_slide = banner_content.querySelector(`.${click_count}`);
    const clicked_count = banner_count.querySelector(`.${click_count}`);

    clicked_slide.classList.add(SHOWING);
    clicked_count.classList.add(CLICKED_BANNER);

    current_slide.classList.remove(SHOWING);
    current_count.classList.remove(CLICKED_BANNER);
}

function autoMoving() {
    const current_slide = banner_content.querySelector(`.${SHOWING}`);
    const current_count = banner_count.querySelector(`.${CLICKED_BANNER}`);

    current_slide.classList.remove(SHOWING);
    current_count.classList.remove(CLICKED_BANNER);

    if(!current_slide.classList.contains('fourth')) {
        const next_slide = current_slide.nextElementSibling;
        const next_count = current_count.nextElementSibling;

        if(next_slide !== null) {
            next_slide.classList.add(SHOWING);
            next_count.classList.add(CLICKED_BANNER);    
        } else {
            const first_count = banner_count.querySelector(".count");
            banner.classList.add(SHOWING);
            first_count.classList.add(CLICKED_BANNER);    
        }
    } else {
        const first_count = banner_count.querySelector(".count");
        banner.classList.add(SHOWING);
        first_count.classList.add(CLICKED_BANNER);
    }
}

function autoBanner() {
    let timer = setInterval(function () {
        if(mode === 'click') {
            mode = 'auto';
        } else if(mode == 'auto') {
            autoMoving();
        } else if(mode == 'stop') {
            clearInterval(timer);
        }
    }, 3000)
}

function init() {
    handleClick();
    autoBanner();
}

init();