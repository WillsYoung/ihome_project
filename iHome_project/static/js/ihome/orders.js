//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    $(".order-comment").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-comment").attr("order-id", orderId);
    });

    var path = location.search;
    var id = path.split('=')[1];


    $.get('/order/order/' + id , function (data) {
        console.log(data);
        if(data.code==200){
            // alert('order request1');

            // if (data.id==0){
            //     var a_url = '/user/my/';
            //     $('.nav-btn').attr('href', a_url);
            // }else {
            //     var a_url = '/house/booking/?id=' + data.id + '/';
            //     $('.nav-btn').attr('href', a_url);
            // }


            var order_content = ' <ul class="orders-list"></ul>';

            console.log(data.orders.length);
            console.log(data.orders);

            for (var i = 0; i < data.orders.length; i++) {

                order_content += '<div class="order-title">' +
                '                 <h3>订单编号：' + data.orders[i].order.order_id + '</h3>' +
                '                 <div class="fr order-operate">' +
                '                 <button type="button" class="btn btn-success order-comment" data-toggle="modal" data-target="#comment-modal">发表评价</button>' +
                '                 </div>' +
                '                 </div>' +
                '                 <div class="order-content">' + '<img src="' + data.orders[i].house.image + '">' +
                '                        <div class="order-text">' +
                '                            <h3>' + data.orders[i].house.title +'</h3>' +
                '                            <ul>' +
                '                                <li>创建时间：' + data.orders[i].order.create_date +'</li>' +
                '                               <li>入住日期：' + data.orders[i].order.begin_date +'</li>' +
                '                              <li>离开日期：' + data.orders[i].order.end_date +'</li>' +
                '                               <li>合计金额：￥' + data.orders[i].order.amount +'(共' + data.orders[i].order.days +'晚)</li>' +
                '                               <li>订单状态：待接单</li>' +
                '                            </ul>' +
                '                        </div></div>';


            }
            $('.orders-con').html(order_content);

        }
    })

});