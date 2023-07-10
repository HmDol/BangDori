// 유효성을 검사하기 위한 변수
let validId = Boolean(false);
let validNickname = Boolean(false);

$(function () {
    $('#idBtn').click(function () {
        let username = $('#idBox').val();

        if (username.length < 1) {
            alert("사용하실 아이디를 입력해주세요.");
            return;
        }

        $.ajax({
            url: '/idcheck',
            type: 'get',
            data: {'user': username},
            dataType: 'json',
            success: function (response) {
                if (response.data === "exist") {
                    alert("이미 존재하는 아이디입니다.");
                } else {
                    alert("사용할 수 있는 아이디입니다.");
                    $('#idBtn').hide();
                    validId = true;
                }
            },
            error: function (xhr, error) {
                alert("서버와의 통신에서 문제가 발생했습니다.");
                console.error("error : " + error);
            }
        })
    })
})

$(function () {
    $('#nicknameBtn').click(function () {
        let nickname = $('#nicknameBox').val();

        if (nickname.length < 1) {
            alert("사용하실 닉네임을 입력해주세요.");
            return;
        }

        $.ajax({
            url: '/idcheck',
            type: 'get',
            data: {'nickname': nickname},
            dataType: 'json',
            success: function (response) {
                if (response.data === "exist") {
                    alert("이미 존재하는 닉네임입니다.");
                } else {
                    alert("사용할 수 있는 닉네임입니다.");
                    $('#nicknameBtn').hide();
                    validNickname = true;
                }
            },
            error: function (xhr, error) {
                alert("서버와의 통신에서 문제가 발생했습니다.");
                console.error("error : " + error);
            }
        })
    })
})

function isValid() {
    /* 중복확인 통과했는지 확인 */
    if (!validId) {
        alert("아이디 중복확인을 해주세요.");
        return false;
    }

    if (!validNickname) {
        alert("닉네임 중복확인을 해주세요.");
        return false;
    }
}