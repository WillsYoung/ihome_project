function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $.get('/house/area_facility/', function (data) {
        var area_html_list = '';
        for(var i = 0; i < data.area_list.length; i++){

           var area_html = '<option value="' + data.area_list[i].id + '">' + data.area_list[i].name + '</option>';
           console.log(data.area_list[i].name);
           console.log(data.area_list[i].id);
           console.log(data)
            console.log(data.area_list[i]);

            area_html_list += area_html;
        }
        $('#area-id').html(area_html_list);

        var facility_html_list = '';
        for(var j = 0; j < data.facility_list.length; j++){

           var facility_html = '<li>' +
               '<div class="checkbox">' +
               '<label>' +
               '<input type="checkbox" name="facility" value="' + data.facility_list[j].id +'">' + data.facility_list[j].name +
               '</label>' +
               '</div>' +
               '</li>';

            facility_html_list += facility_html;
        }
        $('.house-facility-list').html(facility_html_list);
    });

    $('#form-house-info').submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url: '/house/newhouse/',
            type: 'post',
            dataType: 'json',
            success: function (data) {
                if(data.code==200){
                    $('#form-house-info').hide();
                    $('#form-house-image').show();
                    $('#house-id').val(data.house_id);
                }
            },
            error: function () {
                alert('请求失败')
            }
        })
        return false;
    })

    $('#form-house-image').submit(function () {

        $(this).ajaxSubmit({
            url: '/house/newhousepicture/',
            type: 'post',
            dataType: 'json',
            success: function (data) {
                if(data.code == 200){
                    var img = '<img src="' + data.url + '">';
                    $('.house-image-cons').append(img);
                }
            },
            error: function () {
                alert('请求失败')
            }
        })
        return false;
    })


})