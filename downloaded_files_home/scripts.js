var storeId = document.getElementById('storeId').value;
var inputQuantity = $('input[name="quantity"]');
var plusQuantity = function () {
    if (inputQuantity.val() != undefined) {
        var currentVal = parseInt(inputQuantity.val());
        if (!isNaN(currentVal)) {
            inputQuantity.val(currentVal + 1);
        } else {
            inputQuantity.val(1);
        }
    } else {
        console.log('error: Not see elemnt ' + inputQuantity.val());
    }
};
var minusQuantity = function () {
    if (inputQuantity.val() != undefined) {
        var currentVal = parseInt(inputQuantity.val());
        if (!isNaN(currentVal) && currentVal > 1) {
            inputQuantity.val(currentVal - 1);
        }
    } else {
        console.log('error: Not see elemnt ' + inputQuantity.val());
    }
};
function getCartModal() {
    var cart = null, siteNavMobile = $('#site-nav--mobile');
    $('#cartform').hide();
    $('#site-overlay').addClass("active");
    $('.main-body').addClass("sidebar-move");
    siteNavMobile.addClass("active");
    siteNavMobile.removeClass("show-filters").removeClass("show-search").addClass("show-cart");
}


$(document).ready(function () {

    let cookieName = 'COMPARE_STORE_PRODUCT',
        maxProductCount = 3;
    $('.compare').click(function () {
        let t = $(this);
        if (t.hasClass('active')) {
            $.post(
                'product/addcompare',
                {'productId': t.attr('data-id'), 'type': 11},
                function (rs) {
                    if (rs.code == 1) {
                        t.removeClass('active');
                    }
                }
            )
        }else {
            // Lấy danh sách ID sản phẩm từ cookies
            let productIds = getCookie(cookieName) ? JSON.parse(getCookie(cookieName)) : {};
            if (Object.keys(productIds).length >= maxProductCount) {
                alert('Đã đạt tối đa ' + maxProductCount + ' sản phẩm.');
                return;
            }else{
                $.post(
                    '/product/addcompare', {
                        'productId': t.attr('data-id'),
                        'type': 10
                    },
                    function (rs) {
                        var mes = $('#dialogMessage');
                        if (rs.code == 1) {
                            t.addClass('active');
                        } else {
                            mes.html('<p><span class="ui-icon ui-icon-notice" style="float: left; margin: 0 10px 40px 0;"></span>' +
                                rs.messages + '</p>');
                        }
                    },
                    'json'
                );
            }
        }
    });
    // var ps = [];
    // $('.pro-loop').each(function () {
    //     var t = $(this);
    //     ps.push({id: t.attr('data-id')});
    // });
    // CompareProductLoad(ps);
    // function CompareProductLoad(ps) {
    //     if (ps.length) {
    //         if($('.checkCookies').val() != "") {
    //             var esult = JSON.parse($('.checkCookies').val());
    //             $.each(esult, function (key, vl) {
    //                 // console.log('.prd' + key + ' .wishlistItems');
    //                 if (vl <= 0) {
    //                     $('.prd' + key + ' .compare').removeClass('active');
    //                 } else {
    //                     $('.prd' + key + ' .compare').addClass('active');
    //                 }
    //             });
    //         }
    //     }
    // }
    if ($(".fancybox-album").length) {
        $(".fancybox-album").fancybox({
            fitToView: true,
            closeBtn: true,
            padding: 0
        });
    }

    if (in_array($storeId, [157317])) {
        $(".form-wrap a").click(function () {
            var t = $(this), target = $(this).attr('data-target');
            $(".form-wrap a").removeClass('active');
            t.addClass('active');
            $(".form-access").hide();
            $(target).show();
        });
        $(".form-access #btnsignin").click(function () {
            AppAjax.ajax({
                type: "POST",
                data: $(".form-signin").serialize(),
                cache: false,
                dataType: 'json',
                url: "/user/ajaxsignin",
                success: function(rs) {
                    if(rs.code){
                        window.location.href = '/';
                    }
                    else if(rs.message['username'] != undefined){
                        alert(rs.message['username']);
                    }
                    else if(rs.message['email'] != undefined){
                        alert(rs.message['email']);
                    } else {
                        alert(rs.message);
                    }
                }
            });
        });
        $(".form-access #btnsingup").click(function () {
            AppAjax.ajax({
                type: "POST",
                data: $(".form-signup").serialize(),
                cache: false,
                dataType: 'json',
                url: "/user/ajaxsignup",
                success: function(rs){
                    var $email = $('.form-signup #email').val();
                    if(rs.code || validateEmail($email)){
                        $("#formAcount input[type='text'], #formAcount input[type='password']").val('');
                        alert('Bạn đã đăng ký thành công');
                        $(".signin-btn").addClass('active');
                        $(".form-access").hide();
                        $(".form-signin").show();
                    }else{
                        alert('mật khẩu không đúng định dạng hoặc email đã tồn tại. Vui lòng kiểm tra lại!');
                    }
                }
            });
        });
        $("#btn_get_password").click(function () {
            AppAjax.ajax({
                type: "POST",
                data: {
                    username:$('#newpassword').val()
                },
                cache: false,
                dataType: 'json',
                url: "/user/ajaxgetpassword",
                beforeSend:function () {
                    $('body .loadings').addClass('is');
                },
                success: function(rs) {
                    $('body .loadings').removeClass('is');
                    if(rs.code){
                        $("form.f #username").val('');
                        var mess = '<div class="modal-body text-center">\
                        <div class="desc-modal alert alert-success">Vui lòng kiểm tra email và ấn vào đường dẫn tạo mật khẩu mới!</div>\
                            <div class="form-group clearfix text-center"><button type="button" class="close btn close-singup w100 btn-primary" data-dismiss="modal">\n' +
                            '<a class="btn close-singup w100 btn-primary">OK</a>\n' +
                            '</button></div>' +
                            '</div>';
                        $('#modalShow .modal-content').html(mess);
                        $('#modalShow').modal('show');
                    }
                    else if(!rs.code){
                        var mess = '<div class="modal-body text-center"><div class="desc-modal alert alert-danger"> '+rs.message+'</div></div>';
                        $('#modalShow .modal-content').html(mess);
                        $('#modalShow').modal('show');
                    }
                }
            });
        });
    }
    let pathname = window.location.pathname;
    if (pathname == '/user/forgotpassword'){
        $('.get_password').addClass('hide');
        $('.signin-btn').removeClass('active');
        $('.reset_password').addClass('active');
        $(".form-access").hide();
        $(".reset_password").show();
    }
    $("#UserForgotPassword #btn_reset_password").click(function (e) {
        e.preventDefault();
        AppAjax.ajax({
            type: "POST",
            data: $("#UserForgotPassword").serialize(),
            cache: false,
            dataType: 'json',
            url: "/user/ajaxgetforgotpassword",
            beforeSend:function () {
                $('body .loadings').addClass('is');
            },
            success: function(rs) {
                $('body .loadings').removeClass('is');
                if(rs.code){
                    alert('Đổi lại mật khẩu thành công!');
                    window.location.href = '/';
                } else {
                    alert(rs.message);
                }
            }
        });
    });
    $('.cancelOrder').click(function (e) {
        e.preventDefault();
        var msg = $('#dMsg');
        msg.html('<p>Bạn có chắc chắn muốn hủy đơn hàng này?</p>');
        msg.dialog({
            title: "Thông báo", modal: true, show: 'scale',
            buttons: [
                {
                    text: "OK", click: function () {
                        AppAjax.post(
                            '/order/cancel', {id: $('.cancelOrder').attr('data-id')},
                            function (rs) {
                                window.location.reload();
                            },
                            'json'
                        );
                    }
                },
                {
                    text: "Cancel", click: function () {
                        $(this).dialog("close");
                    }
                }
            ]
        });
    });



    if ($(window).width() < 768) {
        $('.footer-title').on('click', function () {
            $(this).toggleClass('active').parent().find('.footer-content').stop().slideToggle('medium');
        });
    } else {
        if(in_array(storeId,[90716])){
            $('.footer-title').on('click', function () {
                $(this).next().stop().slideToggle('fast');
            });
        }else{
            $('.footer-title').on('click', function () {
                $('.footer-content').stop().slideToggle('fast');
            });
        }

    }


    $("#flip1").on('click', function () {
        var $this = $(this), $description = $('.cate-content');
        if ($this.hasClass('active')) {
            $description.removeClass('comment-fill');
            $(this).removeClass('active');
            $this.html('<span>Xem thêm</span>');
        } else {
            $this.addClass('active');
            $this.html('<span>Thu gọn</span>');
            $description.addClass('comment-fill');
        }
        $description.slideDown();
    });

    var popupHomeCookie = $('#popupHome.cookie');
    if(popupHomeCookie.length){
        let timeOut = 0;
        if (in_array(storeId, [92233, 662])) {
            timeOut = 7000;
        }
        setTimeout(function () {
            popupHomeCookie.modal('show');
        }, timeOut)
    }

    $('body').on('click', '.cart_remove', function(){
        let t = $(this);
        if((confirm(msgRemoveCartItem + ' ?') == true)){
            $.post(
                '/cart/remove',
                {'psId': $(this).attr('data-id')},
                function(){
                    if (t.hasClass('cart_remove_index') && in_array(storeId, [92233,15113, 8206])) {
                        window.location.href = '/cart';
                    } else {
                        ajaxLoadView({
                            view: 'cartSidebar',
                            onSuccess: function (rs) {
                                $("#site-cart>.site-nav-container-last").empty();
                                $("#site-cart>.site-nav-container-last").html(rs);
                                $('#myCart').modal('show');
                                $('.modal-backdrop').css({'height': $(document).height(), 'z-index': '99'});
                                getCartModal()
                            }
                        });
                    }
                }
            );
        }
    });
});

// Mainmenu sidebar
$(document).on("click", "span.icon-subnav", function () {
    if ($(this).parent().hasClass('active')) {
        $(this).parent().removeClass('active');
        $(this).siblings('ul').slideUp();
    } else {
        if ($(this).parent().hasClass("level0") || $(this).parent().hasClass("level1")) {
            $(this).parent().siblings().find("ul").slideUp();
            $(this).parent().siblings().removeClass("active");
        }
        $(this).parent().addClass('active');
        $(this).siblings('ul').slideDown();
    }
});

//Click event to scroll to top
$(document).on("click", ".back-to-top", function () {
    $(this).removeClass('show');
    $('html, body').animate({
        scrollTop: 0
    }, 800);
});

/* scroll */
$(window).scroll(function () {
    /* scroll top */
    var backToTopBtn = $('.back-to-top');
    if (backToTopBtn.length > 0 && $(window).scrollTop() > 500) {
        backToTopBtn.addClass('show');
    } else {
        backToTopBtn.removeClass('show');
    }
    /* scroll header */
    if ($(window).width() < 768) {
        var scroll = $(window).scrollTop();
        var height_header = $('.main-header').outerHeight();
        if (scroll < 320) {
            $(".main-header").removeClass("scroll-menu");
            if($('.bottom-header').length && in_array(storeId, [92233, 8206])) {
                $('.bottom-header').removeClass('fixed').css('top', 0);
            }
            $('.fixed_scroll').removeClass('affix-mobile');

        } else {
            $(".main-header").addClass("scroll-menu");
            if($('.bottom-header').length && in_array(storeId, [92233, 8206])) {
                $('.bottom-header').addClass('fixed').css('top', height_header);
            }
            $('.fixed_scroll').addClass('affix-mobile');
        }
    } else {
        if (in_array(storeId, [70105, 146765, 92233,184620,15113])){
            var height_header = $('.fixed_scroll').height();
            if ($(window).scrollTop() >= height_header) {
                $('.fixed_scroll').addClass('affix-mobile');
            } else {
                $('.fixed_scroll').removeClass('affix-mobile');
            }
        }
        else {
            var height_header = $('.main-header').height();
            if ($(window).scrollTop() >= height_header) {
                $('.main-header').addClass('affix-mobile');
                if($('.campaign-page').length && in_array(storeId, [79592,157317])) {
                    $('.campaign-page .campaginTable thead').css('top', height_header);
                }
                if($('.bottom-header').length && in_array(storeId, [92233, 8206])) {
                    $('.bottom-header').addClass('fixed').css('top', height_header);
                }
            } else {
                $('.main-header').removeClass('affix-mobile');
                if($('.campaign-page').length && in_array(storeId, [79592,157317])) {
                    $('.campaign-page .campaginTable thead').css('top', 0);
                }
                if($('.bottom-header').length && in_array(storeId, [92233, 8206])) {
                    $('.bottom-header').removeClass('fixed').css('top', 0);
                }
            }
        }
    }
});


// Menu sidebar
$(document).on('click', '.tree-menu .tree-menu-lv1', function () {
    $this = $(this).find('.tree-menu-sub');
    $('.tree-menu .has-child .tree-menu-sub').not($this).slideUp('fast');
    $(this).find('.tree-menu-sub').slideToggle('fast');
    $(this).toggleClass('menu-collapsed');
    $(this).toggleClass('menu-uncollapsed');
    var $this1 = $(this);
    $('.tree-menu .has-child').not($this1).removeClass('menu-uncollapsed');
});

// Dropdown Title
$('.title_block').click(function () {
    $(this).next().slideToggle('medium');
});

$(document).on("click", ".dropdown-filter", function () {
    if ($(this).parent().attr('aria-expanded') == 'false') {
        $(this).parent().attr('aria-expanded', 'true');
    } else {
        $(this).parent().attr('aria-expanded', 'false');
    }
});

$(document).ready(function () {
    // nhanh.init();

    colorVariant();

    // this.quickview();
    $(document).on('click', '.quickView', function () {

        var proId = $(this).attr("data-id");
        if(in_array(storeId,[90716])){
            var products = [];
            products = [{id: proId, quantity: 1}];
            addToCart(products, 1, function (rs) {
                if (rs.status == 1) {
                    AppAjax.post('/product/child?childId=' + proId,{},
                        function (rs) {
                            if (rs.code == 1) {
                                ajaxLoadView({
                                    view: 'cartSidebar',
                                    onSuccess: function (rs) {
                                        $("#site-cart>.site-nav-container-last").empty();
                                        $("#site-cart>.site-nav-container-last").html(rs);
                                        $('#myCart').modal('show');
                                        $('.modal-backdrop').css({'height': $(document).height(), 'z-index': '99'});
                                        getCartModal()
                                    }
                                });
                            }
                        },
                        'json'
                    );
                } else {
                    alert(rs.messages);
                }
            });
        }else{
            var url = 'product/q' + proId;
            if((in_array(storeId,[2071])) && ($(window).width() < 991)){
                $('#navigation--list--mobile').addClass('hidden--mobile');
                url = 'product/q' + proId +'?viewMobile=1';
            }
            $.ajax({
                url: url,
                type: 'GET',
                dataType: 'text',
                success: function (data) {
                    $("#quickview-cart-desktop").html(``);
                    // $("#quickview-cart-desktop").html(data);
                    $('#quickview-cart').modal('show');
                },
                error: function () {
                    // Nếu không thành công, chèn nội dung HTML mặc định
                    $("#quickview-cart-desktop").html(`
                    <script defer type="text/javascript" src="https://web.nvnstatic.net/tp/T0298/js/pQuickview.js?v=3"></script>

                    <button type="button" class="close" data-dismiss="modal">
                        <img src="https://web.nvnstatic.net/tp/T0298/img/tmp/iconclose.png?v=7"  alt="Đóng">
                    </button>
                    
                    <div class="col-md-8 col-sm-7 col-xs-12">
                        <div class="clearfix hidden-xs col-sm-1 thumbnails small-img">
                            <div class="row">
                                
                                            <div class="  thumbnail thumdelete clickItem" data-index="0" 
                                                data-option="do" data-zoom="https://pos.nvncdn.com/609d6b-117900/ps/20241231_osj61gUr3I.jpeg">
                                                <img class="img-fluid img-thumbnail"
                                                     src="https://pos.nvncdn.com/609d6b-117900/ps/20241231_osj61gUr3I.jpeg">
                                            </div>
                                        
                                            <div class="  thumbnail thumdelete clickItem" data-index="1" 
                                                data-option="do" data-zoom="https://pos.nvncdn.com/609d6b-117900/ps/20241231_bKQCUHcvYO.jpeg">
                                                <img class="img-fluid img-thumbnail"
                                                     src="https://pos.nvncdn.com/609d6b-117900/ps/20241231_bKQCUHcvYO.jpeg">
                                            </div>
                                        
                                            <div class="  thumbnail thumdelete clickItem" data-index="2" 
                                                data-option="do" data-zoom="https://pos.nvncdn.com/609d6b-117900/ps/20250103_NqFdn6YrqJ.jpeg">
                                                <img class="img-fluid img-thumbnail"
                                                     src="https://pos.nvncdn.com/609d6b-117900/ps/20250103_NqFdn6YrqJ.jpeg">
                                            </div>
                                        
                                            <div class="  thumbnail thumdelete clickItem" data-index="3" 
                                                data-option="do" data-zoom="https://pos.nvncdn.com/609d6b-117900/ps/20250103_qQBN9cYL9D.jpeg">
                                                <img class="img-fluid img-thumbnail"
                                                     src="https://pos.nvncdn.com/609d6b-117900/ps/20250103_qQBN9cYL9D.jpeg">
                                            </div>
                                                </div>
                        </div>
                    
                        <div class="clearfix col-sm-11">
                            <div id="slide-image"></div>
                            <div class="hinh360" style="display:none">
                                <div id="mySpriteSpin"></div>
                            </div>
                            <div class="videoProduct" style="display:none">
                                <iframe src="" width="100%" height="470" frameborder="0" allow="autoplay; fullscreen"
                                        allowfullscreen=""></iframe>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 col-sm-5 col-xs-12" id="detail-product">
                        <div class="product-title">
                            <h1>SƠ MI DOLCE LỤA NỮ HOÀNG MARTINI G5EJ1T HP5ZS</h1>
                            <span class="pro-soldold">Tình trạng: <span class="statusProduct">Còn hàng</span></span>
                        </div>
                            <div class="product-price sale-undo" id="price-preview">
                            
                                                                                    <p class="pro-price highlight tp_product_price">
                                                                                        9,500,000₫
                                                                                        
                                                                                    </p>
                                                                                            </div>
                    
                    
                        <form id="add-item-form" action="" method="post" class="variants clearfix">
                            <div class="select-swatch clearfix ">
                                                    <div id="variant-swatch-1" class=" swatch clearfix">
                                            <div class="header">kích thước</div>
                                            <div class="select-swap attr-size req" data-column="i1">
                                                                                <div data-value="" class=" n-sd swatch-element">
                                                        <label data-value="1944589" class="active">
                                                            <span>40</span>
                                                            <img class="crossed-out" src="https://web.nvnstatic.net/tp/T0298/img/soldout.png?v=7" />
                                                        </label>
                                                    </div>
                                                                        </div>
                                        </div>
                                        
                            </div>
                    
                            <div class="selector-actions">
                                <div class="quantity-area clearfix hide">
                                    <input type="button" value="-" onclick="minusQuantity()" class="qty-btn">
                                    <input type="text" id="quantity" name="quantity" value="1" min="1" class="quantity-selector">
                                    <input type="button" value="+" onclick="plusQuantity()" class="qty-btn">
                                </div>
                    
                                <div class="wrap-addcart clearfix">
                                    <button type="button" id="add-to-cart" class="btnAddToCart" data-psid="40777448" data-selId="40777448" 
                                                    title="Vui lòng chọn màu sắc hoặc kích cỡ!" data-ck="0">SỞ HỮU NGAY</button>            </div>
                            </div>
                        </form>
                    
                        <div class="product-description">
                            <div class="title-bl">
                                <h2>
                                    Thông số sản phẩm                <span class="icon-open"></span>
                                </h2>
                            </div>
                            <div class="description-content">
                                <div class="main_details">
                                    Đang cập nhật nội dung.            </div>
                            </div>
                        </div>
                        <div class="product-description">
                            <div class="title-bl">
                                <h2>
                                    Mô tả sản phẩm                <span class="icon-open"></span>
                                </h2>
                            </div>
                            <div class="description-content">
                                <div class="description-productdetail">
                                    Đang cập nhật nội dung.            </div>
                            </div>
                        </div>
                        <center class="centerDetial">
                            <a href="/so-mi-dolce-lua-nu-hoang-martini-g5ej1t-hp5zs-p40777448.html">Xem chi tiết sản phẩm &gt;&gt;</a>
                        </center>
                    </div>
                    
                    <div id="divzoom">
                        <div class="divzoom_main">
                                            <div class="product-thumb text-center">
                                        <img class="product-image-feature"
                                             src="https://pos.nvncdn.com/609d6b-117900/ps/20241231_osj61gUr3I.jpeg"
                                             alt="SƠ MI DOLCE LỤA NỮ HOÀNG MARTINI G5EJ1T HP5ZS">
                                    </div>
                                                    <div class="product-thumb text-center">
                                        <img class="product-image-feature"
                                             src="https://pos.nvncdn.com/609d6b-117900/ps/20241231_bKQCUHcvYO.jpeg"
                                             alt="SƠ MI DOLCE LỤA NỮ HOÀNG MARTINI G5EJ1T HP5ZS">
                                    </div>
                                                    <div class="product-thumb text-center">
                                        <img class="product-image-feature"
                                             src="https://pos.nvncdn.com/609d6b-117900/ps/20250103_NqFdn6YrqJ.jpeg"
                                             alt="SƠ MI DOLCE LỤA NỮ HOÀNG MARTINI G5EJ1T HP5ZS">
                                    </div>
                                                    <div class="product-thumb text-center">
                                        <img class="product-image-feature"
                                             src="https://pos.nvncdn.com/609d6b-117900/ps/20250103_qQBN9cYL9D.jpeg"
                                             alt="SƠ MI DOLCE LỤA NỮ HOÀNG MARTINI G5EJ1T HP5ZS">
                                    </div>
                                        </div>
                        <div id="positionButtonDiv" class="hidden">
                            <p>
                                <span>
                                    <button type="button" class="buttonZoomIn"><i></i></button>
                                    <button type="button" class="buttonZoomOut"><i></i></button>
                                </span>
                            </p>
                        </div>
                        <button id="closedivZoom"><i></i></button>
                    </div>
                    
                    
                    <div class="hidden images">
                                    <div name-new="_sd05041" class="item itemdelete" data-original="https://pos.nvncdn.com/609d6b-117900/ps/20241231_osj61gUr3I.jpeg"
                                     data-option="do" data-variant="SD05041">
                                    <a href="https://pos.nvncdn.com/609d6b-117900/ps/20241231_osj61gUr3I.jpeg"
                                       title="Click để xem" data-option="do"
                                       data-image="https://pos.nvncdn.com/609d6b-117900/ps/20241231_osj61gUr3I.jpeg"
                                       data-zoom-image="https://pos.nvncdn.com/609d6b-117900/ps/20241231_osj61gUr3I.jpeg"
                                       rel="lightbox-do">
                                        <img class="img-fluid img-responsive"
                                             src="https://pos.nvncdn.com/609d6b-117900/ps/20241231_osj61gUr3I.jpeg">
                                        <p class="click-p"
                                           href="https://pos.nvncdn.com/609d6b-117900/ps/20241231_osj61gUr3I.jpeg"
                                           data-zoom-image="https://pos.nvncdn.com/609d6b-117900/ps/20241231_osj61gUr3I.jpeg"
                                           rel="lightbox-do">
                                            <i class="fa fa-search" aria-hidden="true"></i>
                                            Click xem hình lớn hơn
                                        </p>
                                    </a>
                                </div>
                                            <div name-new="_sd05041" class="item itemdelete" data-original="https://pos.nvncdn.com/609d6b-117900/ps/20241231_osj61gUr3I.jpeg"
                                     data-option="do" data-variant="SD05041">
                                    <a href="https://pos.nvncdn.com/609d6b-117900/ps/20241231_bKQCUHcvYO.jpeg"
                                       title="Click để xem" data-option="do"
                                       data-image="https://pos.nvncdn.com/609d6b-117900/ps/20241231_bKQCUHcvYO.jpeg"
                                       data-zoom-image="https://pos.nvncdn.com/609d6b-117900/ps/20241231_bKQCUHcvYO.jpeg"
                                       rel="lightbox-do">
                                        <img class="img-fluid img-responsive"
                                             src="https://pos.nvncdn.com/609d6b-117900/ps/20241231_bKQCUHcvYO.jpeg">
                                        <p class="click-p"
                                           href="https://pos.nvncdn.com/609d6b-117900/ps/20241231_bKQCUHcvYO.jpeg"
                                           data-zoom-image="https://pos.nvncdn.com/609d6b-117900/ps/20241231_bKQCUHcvYO.jpeg"
                                           rel="lightbox-do">
                                            <i class="fa fa-search" aria-hidden="true"></i>
                                            Click xem hình lớn hơn
                                        </p>
                                    </a>
                                </div>
                                            <div name-new="_sd05041" class="item itemdelete" data-original="https://pos.nvncdn.com/609d6b-117900/ps/20241231_osj61gUr3I.jpeg"
                                     data-option="do" data-variant="SD05041">
                                    <a href="https://pos.nvncdn.com/609d6b-117900/ps/20250103_NqFdn6YrqJ.jpeg"
                                       title="Click để xem" data-option="do"
                                       data-image="https://pos.nvncdn.com/609d6b-117900/ps/20250103_NqFdn6YrqJ.jpeg"
                                       data-zoom-image="https://pos.nvncdn.com/609d6b-117900/ps/20250103_NqFdn6YrqJ.jpeg"
                                       rel="lightbox-do">
                                        <img class="img-fluid img-responsive"
                                             src="https://pos.nvncdn.com/609d6b-117900/ps/20250103_NqFdn6YrqJ.jpeg">
                                        <p class="click-p"
                                           href="https://pos.nvncdn.com/609d6b-117900/ps/20250103_NqFdn6YrqJ.jpeg"
                                           data-zoom-image="https://pos.nvncdn.com/609d6b-117900/ps/20250103_NqFdn6YrqJ.jpeg"
                                           rel="lightbox-do">
                                            <i class="fa fa-search" aria-hidden="true"></i>
                                            Click xem hình lớn hơn
                                        </p>
                                    </a>
                                </div>
                                            <div name-new="_sd05041" class="item itemdelete" data-original="https://pos.nvncdn.com/609d6b-117900/ps/20241231_osj61gUr3I.jpeg"
                                     data-option="do" data-variant="SD05041">
                                    <a href="https://pos.nvncdn.com/609d6b-117900/ps/20250103_qQBN9cYL9D.jpeg"
                                       title="Click để xem" data-option="do"
                                       data-image="https://pos.nvncdn.com/609d6b-117900/ps/20250103_qQBN9cYL9D.jpeg"
                                       data-zoom-image="https://pos.nvncdn.com/609d6b-117900/ps/20250103_qQBN9cYL9D.jpeg"
                                       rel="lightbox-do">
                                        <img class="img-fluid img-responsive"
                                             src="https://pos.nvncdn.com/609d6b-117900/ps/20250103_qQBN9cYL9D.jpeg">
                                        <p class="click-p"
                                           href="https://pos.nvncdn.com/609d6b-117900/ps/20250103_qQBN9cYL9D.jpeg"
                                           data-zoom-image="https://pos.nvncdn.com/609d6b-117900/ps/20250103_qQBN9cYL9D.jpeg"
                                           rel="lightbox-do">
                                            <i class="fa fa-search" aria-hidden="true"></i>
                                            Click xem hình lớn hơn
                                        </p>
                                    </a>
                                </div>
                                </div>
                    
                    <!-- source thumb slide -->
                    <div class="hidden thumbnails-hidden">
                        
                                        <div class="  thumbnail thumdelete clickItem" data-option="do"
                                             data-zoom="https://pos.nvncdn.com/609d6b-117900/ps/20241231_osj61gUr3I.jpeg">
                                            <img class="img-fluid img-thumbnail"
                                                 src="https://pos.nvncdn.com/609d6b-117900/ps/20241231_osj61gUr3I.jpeg">
                                        </div>
                                    
                                        <div class="  thumbnail thumdelete clickItem" data-option="do"
                                             data-zoom="https://pos.nvncdn.com/609d6b-117900/ps/20241231_bKQCUHcvYO.jpeg">
                                            <img class="img-fluid img-thumbnail"
                                                 src="https://pos.nvncdn.com/609d6b-117900/ps/20241231_bKQCUHcvYO.jpeg">
                                        </div>
                                    
                                        <div class="  thumbnail thumdelete clickItem" data-option="do"
                                             data-zoom="https://pos.nvncdn.com/609d6b-117900/ps/20250103_NqFdn6YrqJ.jpeg">
                                            <img class="img-fluid img-thumbnail"
                                                 src="https://pos.nvncdn.com/609d6b-117900/ps/20250103_NqFdn6YrqJ.jpeg">
                                        </div>
                                    
                                        <div class="  thumbnail thumdelete clickItem" data-option="do"
                                             data-zoom="https://pos.nvncdn.com/609d6b-117900/ps/20250103_qQBN9cYL9D.jpeg">
                                            <img class="img-fluid img-thumbnail"
                                                 src="https://pos.nvncdn.com/609d6b-117900/ps/20250103_qQBN9cYL9D.jpeg">
                                        </div>
                                    </div>
                    
                    <div class="checkValue hide">
                        <div class="item360deg" data-color="do"></div>
                    
                        <div class="item360deg" data-color="xanh-la"></div>
                    
                        <div class="item360deg" data-color="den"></div>
                    </div>
                    
                    
                    
                    
                    `);
                },
                complete: function () {
                    // Hiển thị modal bất kể thành công hay thất bại
                    $('#quickview-cart').modal('show');
                }
            });
        }
    });

    $(document).on('click', '.close-quick-view', function () {
        $('#quickview-cart').modal('hide');
    });

    $(window).scroll(function () {
        if ($(this).scrollTop() > 0) {
            $('#bttop').fadeIn();
        } else {
            $('#bttop').fadeOut();
        }
    });

    $('#bttop').click(function () {
        $('body,html').animate(
            {scrollTop: 0}, 800);
    });

    // this.mmMenu();

        if ($(window).width() < 1200) {
            if (!in_array(storeId, [63398,79592,157317,7888])) {
                let $options = {}
                if (in_array(storeId, [112918])) {
                    $options = {
                        navbar : {
                            title : 'Home',
                        }
                    }
                }
                if (in_array(storeId, [152328])) {
                    $options = {
                        "slidingSubmenus": false,
                    }
                }
                $('#menu-mobile').mmenu($options);

            }
            flagg = true;
            if (flagg) {
                $('.hamburger-menu').click(function () {
                    $('#menu-mobile').removeClass('hidden');
                    flagg = false;
                })
            }
        } else {
            $("#menu-mobile").remove();
        }


    $(".filterSmallScreen").click(function () {
        $("body").addClass("openFilter");
    });
    $(".btn_filter_cancel, .innerSidebarFilter .filterTitle .fa").click(function () {
        $("body").removeClass("openFilter");
    });

    // this.removeDiv();
    if ($(window).width() < 992) {
        $(".removeMobile").remove();
    } else {
        $(".removeDesktop").remove();
    }

    if (!in_array(storeId, [92233,15113])) {
        setTimeout(function () {
            var height = $("#site-header").outerHeight() - 1;
            $(".outerHeightHeader").css("min-height", height);
        }, 100);
    }

    // Check Out Of Stock Script
    if($('body .pro-loop').length){
        var ps = [];
        $('.pro-loop').each(function(){
            ps.push({
                storeId: storeId,
                id: $(this).attr('data-Id')
            });
        });

        if(ps.length){
            var $sold = 'Hết hàng';
            if (in_array(storeId,[2071])){
              $sold = 'Hết hàng online'
            }
            if (in_array(storeId,[176660])){
                $sold = 'Hàng đang về';
            }
            if (in_array(storeId,[79592,157317,7888,118144, 1549])){
                $sold = 'Tạm hết';
            }
            checkInventory(ps, function(rs){
                if(rs.inventories != ""){
                    $.each(rs.inventories, function(Id, ivt){
                        if(ivt <= 0){
                            if (in_array(storeId,[106510])){
                                $('.pro-loop[data-Id="'+ Id +'"]').find('.product-img.image-resize').append('<div class="out-of-stock">SOLD</div>');
                            }else{
                                $('.pro-loop[data-Id="'+ Id +'"]').find('.product-img.image-resize').append('<div class="out-of-stock">'+ $sold +'</div>');
                            }
                        } else {
                            if (in_array(storeId, [92233,15113, 8206]) && ivt <= 20) {
                                $('.promo-products .pro-loop[data-Id="'+ Id +'"]').find('.box-pro-detail').append('<div class="ivt-num">Chỉ còn duy nhất '+ ivt +' sản phẩm</div>');
                            }
                        }
                    });
                }
            });
        }
    }

    // Disable download Image
    if (in_array(storeId, [126453])){
        $('img, #slide-image').on({
            "contextmenu": function(e) {
                e.preventDefault();
            }
        });
    }

    if (in_array(storeId,[102954])){
        setTimeout(function () {
            $('.purchase-content:first').addClass('showP');
        }, 3000);
        setInterval( function(){
            if ($('.purchase-content:last').hasClass('showP')) {
                iNext = $('.purchase-content:first')
            } else {
                iNext = $('.purchase-content.showP').next()
            }
            var iShow = $('.purchase-content.showP');
            iShow.removeClass('showP');
            setTimeout(function () {
                iNext.addClass('showP')
            }, 3000)
        }, 8000 );

        $('.close-purchase').click(function () {
            $('.purchase-content.showP').removeClass('showP')
        })
    }
    if (in_array(storeId,[184620,15113])) {
        let currLoc = $(location).attr('href');
        let homeLoc = $('#url_homepage').val();
        if (homeLoc !== currLoc){
            $('body').addClass('page');
        }
        var initializeCarousel = function(selector, options) {
            var el = $(selector);
            var carousel;
            var orderedBreakpoints = Object.keys(options.responsive).map(Number).sort((a, b) => b - a);
            var severalRows = Object.values(options.responsive).some(config => config.rows > 1);

            var viewport = function() {
                return window.innerWidth || document.documentElement.clientWidth || console.warn('Cannot detect viewport width.');
            };

            var getRowsColsNb = function() {
                var width = viewport();
                var rowsNb, colsNb;

                for (var breakpoint of orderedBreakpoints) {
                    if (width >= breakpoint || breakpoint === orderedBreakpoints[orderedBreakpoints.length - 1]) {
                        rowsNb = options.responsive[breakpoint].rows || 1;
                        colsNb = options.responsive[breakpoint].items;
                        break;
                    }
                }
                return { rowsNb, colsNb };
            };

            var updateCarousel = function() {
                var { rowsNb, colsNb } = getRowsColsNb();
                var slides = el.find('[data-slide-index]');
                var slidesNb = slides.length;

                if (carousel) {
                    carousel.trigger('destroy.owl.carousel');
                    el.empty().append(slides); // Reset slides
                    el.find('.fake-col-wrapper').remove();
                }
                var perPage = rowsNb * colsNb;
                var fakeColsNb = Math.ceil(slidesNb / perPage) * colsNb;

                for (var i = 0; i < fakeColsNb; i++) {
                    var fakeCol = $('<div class="fake-col-wrapper"></div>').appendTo(el);
                    for (var j = 0; j < rowsNb; j++) {
                        var index = Math.floor(i / colsNb) * perPage + (i % colsNb) + j * colsNb;
                        if (index < slidesNb) {
                            slides.eq(index).detach().appendTo(fakeCol);
                        }
                    }
                }
                carousel = el.owlCarousel(options);
            };

            if (severalRows) {
                $(window).on('resize', updateCarousel);
                updateCarousel();
            } else {
                carousel = el.owlCarousel(options);
            }
        };

        initializeCarousel('#carousel1', {
            items: 4,
            margin: 20,
            nav: true,
            pagination: false,
            slideBy: 'page',
            navText: ['<i class="fa fa-angle-left" aria-hidden="true"></i>', '<i class="fa fa-angle-right" aria-hidden="true"></i>'],
            responsive: {
                0: { items: 2, rows: 8 },
                768: { items: 2, rows: 3 },
                991: { items: 4, rows: 4 }
            }
        });
        initializeCarousel('#carousel2', {
            items: 4,
            margin: 20,
            nav: true,
            pagination: false,
            slideBy: 'page',
            navText: ['<i class="fa fa-angle-left" aria-hidden="true"></i>', '<i class="fa fa-angle-right" aria-hidden="true"></i>'],
            responsive: {
                0: { items: 2, rows: 8 },
                768: { items: 2, rows: 3 },
                991: { items: 4, rows: 4 }
            }
        });

        $("#slider2").hide();
        $('#shop-new-arrivals').on('click', function () {
            $(".home-block-new-main").hide();
            $("#slider1").show();
            $(this).parents('.home-block-new').find('#slider1').addClass('active');
            $('#slider2').removeClass('active');
            $('#shop-new-arrivals').addClass('shop-active');
            $('#shop-bestseller').removeClass('shop-active');
        });
        $('#shop-bestseller').on('click', function () {
            $(".home-block-new-main").hide();
            $("#slider2").show();
            $(this).parents('.home-block-new').find('#slider2').addClass('active');
            $('#slider1').removeClass('active');
            $('#shop-bestseller').addClass('shop-active');
            $('#shop-new-arrivals').removeClass('shop-active');
        });
    }

    if (in_array(storeId, [146732])) {
        $("#searchAction").change(function () {
            $(".searchHeader").attr('action', $(this).val());
        });
    }
});

// this.colorVariant()
function colorVariant () {
    $(".variantColor li").hover(function (e) {
        e.preventDefault();
        $(this).parents(".variantColor").find("li").removeClass("active");
        $(this).addClass("active");
        var imgVariant1 = $(this).find("a").attr("data-img");
        var imgVariant2 = $(this).find("a").attr("data-img-hover");
        $(this).parents(".product-block").find(".product-img picture:nth-child(1) img").attr("src", imgVariant1);
        $(this).parents(".product-block").find(".product-img picture:nth-child(2) img").attr("src", imgVariant2);
    });
}



