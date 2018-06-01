function logout() {
    $.get("/user/logout/", function(data){
        if (data.code==200) {
            location.href = "/user/login/";
        }
    })
}

$(document).ready(function(){
    $.ajax({
        url: '/user/getuser/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            // alert('success');
            if(data.code == 200){
                // alert('success1');
                $('#user-mobile').html(data.user.phone);
                // console.log(data)
                $('#user-name').html(data.user.name);
                $('#user-avatar').attr('src', data.user.avatar);
            }

        },
        error: function () {
            alert('failed')
        }
    })
})