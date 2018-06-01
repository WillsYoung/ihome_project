$(document).ready(function(){
    $(".auth-warn").show();

    $.get('/house/auth_myhouse/', function (data) {
        if (data.code==200){

            $(".auth-warn").hide();
            var house_list_html = '';
            for(var i = 0; i < data.house_list.length; i++){
                console.log(data.house_list[i]);
                var house_html = '';
                house_html += '<li>' +
                    '<a href="/house/detail/?id=' + data.house_list[i].id + '">' +
                    '<div class="house-title">' +
                    '<h3>房屋ID:' + data.house_list[i].id + '——' + data.house_list[i].title + '</h3>' +
                    '</div>' +
                    '<div class="house-content">' +
                    '<img src="'  + data.house_list[i].image + '">' +
                    '<div class="house-text">' +
                    '<ul>' +
                    '<li>位于：' + data.house_list[i].area + '</li>' +
                    '<li>价格：￥' + data.house_list[i].price + '2/晚</li>' +
                    '<li>发布时间：'+ data.house_list[i].create_time + '</li>' +
                    '</ul>' +
                    '</div> ' +
                    '</div>' +
                    '</a>' +
                    '</li>';

                house_list_html += house_html;

            }

            $('#houses-list').append(house_list_html)
        }
    })
});

