function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$('#form-avatar').submit(function () {
    // e.preventDefault();
    $(this).ajaxSubmit({
        url: '/user/profile/',
        type: 'PUT',
        dataType: 'json',
        success: function (data) {
            if (data.code== 200){
                $('#user-avatar').attr('src', data.url)
            }
        },
        error: function () {
            alert('failed')
        }
    });
    return false;
});

$('#form-name').submit(function (e) {
    // e.preventDefault();

    var name = $('user-name').val();
    $(this).ajaxSubmit({
        url: '/user/profile/',
        type: 'PUT',
        data: {'name': name},
        dataType: 'json',
        success: function (data) {

            alert('请求成功')
            if (data.code==200){
                $('.error-msg').hide();
            }else {
                $('.error-msg').show();
            }
        },
        error: function () {
            alert('请求失败')
        }
    })
    return false;

});






