function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


$.get('/user/auths/', function (data) {

    if (data.code == 200){
        $('#id-name').val(data.id_name);
        $('#id-card').val(data.id_card);

        $('.btn-success').hide();
    }
});



$("#form-auth").submit(function (e) {
    e.preventDefault();
    $(this).ajaxSubmit({
        url: '/user/auth/',
        type: 'PUT',
        dataType: 'json',
        success: function (data) {
            if (data.code == 200){
                $('.btn-success').hide();
                $('.error-msg').hide();
            }else {
                $('.error-msg').show();
            }

        },
        error: function () {
            alert('请求失败')
        }
    });
    return false;
});