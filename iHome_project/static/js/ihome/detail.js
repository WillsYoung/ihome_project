function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){

    // 获取当前页面url来获取房间号
    var path = location.search;
    alert(path);
    var id = path.split('=')[1];

    $.get('/house/detail/' + id + '/', function (data) {
        if (data.code==200){
            console.log(data.house);

            var swiper_url = '';
            for (var i = 0; i < data.house.images.length; i++){
                swiper_url += '<li class="swiper-slide" style="width: auto"><img src="' + data.house.images[i] + '"></li>'
            }
            $('.swiper-wrapper').html(swiper_url);
            var mySwiper = new Swiper ('.swiper-container', {
            loop: true,
            autoplay: 2000,
            autoplayDisableOnInteraction: false,
            pagination: '.swiper-pagination',
            paginationType: 'fraction'
            });
            $(".book-house").show();


            var house_price_content = '￥<span>' + data.house.price + '</span>/晚';
            $('.house-price').html(house_price_content);

            var detail_header_content = '<h2 class="house-title">' + data.house.title + '</h2>' +
                '                <div class="landlord-pic"><img src="'+ data.house.user_avatar +'"></div>\n' +
                '                <h2 class="landlord-name">房东： <span>' + data.house.user_name + '</span></h2>';
            $('.detail-header').html(detail_header_content);

            var house_addr = '<li>' + data.house.address + '</li>';
            $('.house-info-list').html(house_addr);

            var house_type_content = '<li>\n' +
                '                    <span class="icon-house"></span>' +
                '                    <div class="icon-text">' +
                '                        <h3>出租' + data.house.room_count + '间</h3>' +
                '                        <p>房屋面积:' + data.house.acreage + '平米</p>' +
                '                        <p>房屋户型:' + data.house.unit + '</p>' +
                '                    </div>' +
                '                </li>' +
                '                <li>' +
                '                    <span class="icon-user"></span>' +
                '                    <div class="icon-text">' +
                '                        <h3>宜住' + data.house.capacity + '人</h3>' +
                '                    </div>' +
                '                </li>' +
                '                <li>' +
                '                    <span class="icon-bed"></span>' +
                '                    <div class="icon-text">' +
                '                        <h3>卧床配置</h3>' +
                '                        <p>' + data.house.beds + '</p>' +
                '                    </div>' +
                '                </li>';
            $('.house-type').html(house_type_content);

            var house_deposit = '<li>收取押金<span>' + data.house.deposit + '</span></li>' +
                '<li>最少入住天数<span>' + data.house.min_days + '</span></li>' +
                '<li>最多入住天数<span>' + data.house.max_days + '</span></li>';
            $('#house-deposit-info').html(house_deposit);

            var facilities = '';
            for(var j = 0; j < data.house.facilities.length; j++){
                facilities += '<li><span class="' + data.house.facilities[j].css + '"></span>' +  data.house.facilities[j].name + '</li>'
            }
            $('.house-facility-list').html(facilities);

            var a_url = '/house/booking/?id=' + data.house.id;
            $('.book-house').attr('href', a_url);
            alert('ok')
        }

        if(data.booking){
            alert('这是你自己发布的房源，确定要预定吗？')
        }
    })
});
