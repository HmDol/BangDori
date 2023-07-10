function loadImage() {
    let input = document.createElement("input");

    input.type = "file";
    input.accept = "image/png, image/gif, image/jpeg";

    input.onchange = function (e) {
        document.querySelector(".write-content");

        let selectFile = document.querySelector("#inputImage").files[0];
        const file = URL.createObjectURL(selectFile);
        document.querySelector(".write-content").src = file;
    }

    input.click();
}

document.getElementById('upload-image-file').onchange = function () {
    var src = URL.createObjectURL(this.files[0]);
    document.getElementById('upload-image-file-label').textContent = "사진 첨부됨";
}

function leftAlign() {
    document.querySelector(".write-content").style.textAlign = "left";
    document.getElementById("alignStatus").value = "left";
}

function middleAlign() {
    document.querySelector(".write-content").style.textAlign = "center";
    document.getElementById("alignStatus").value = "center";
}

function rightAlign() {
    document.querySelector(".write-content").style.textAlign = "right";
    document.getElementById("alignStatus").value = "right";
}