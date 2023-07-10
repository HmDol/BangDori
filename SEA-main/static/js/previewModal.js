const preview_btns = document.querySelectorAll(".preview-article-btn"),
    modal = document.querySelector(".preview-modal"),
    overlay = document.querySelector(".overlay");

const OPEN = "open";

function openModal() {
    modal.classList.add(OPEN);
    overlay.classList.add(OPEN);
}

function closeModal() {
    modal.classList.remove(OPEN);
    overlay.classList.remove(OPEN);
}

function getArticleInfo(name, pk) {
    $.ajax({
        url: `/api/article/${name}/${pk}`,
        type: 'get',
        data: {},
        dataType: 'json',
        success: function (response) {
            let info = `조회 수 ${response.views} 추천 수 ${response.upvote} 댓글 수 ${response.comments}`
            document.getElementById("modal-title").textContent = response.title;
            document.getElementById("modal-date").textContent = response.date;
            document.getElementById("modal-article-writer").textContent = response.nickname;
            document.getElementById("modal-title").textContent = response.title;
            document.getElementById("modal-article-user").textContent = info;
            document.getElementById("modal-content").textContent = response.content;
            let img = response.img;
            console.log(img);
            $(".modal-img").attr("src",img)
        },
        error: function () {
            alert("게시글 정보를 불러올 수 없습니다.");
            closeModal();
        }
    });
}