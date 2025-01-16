var storeId = document.getElementById('storeId').value;

$(document).ready(function() {


    $('.language .toggle').click(function () {
        $(this).next().slideToggle();
    });

//khoong click được chuột phải
    if (in_array(storeId, [93682])) {
        $(document).bind('contextmenu', function (e) {
            return false;
        })
    }

    if ($('#load-purchase-product').length) {
        // load sản phẩm fake
        ajaxLoadView({
            view: 'purchaseProduct',
            delay: 1000,
            onSuccess: function (rs) {
                $('#load-purchase-product').html(rs)
            }
        });
    }
    if ($('#phistory-bar').length) {
        ajaxLoadView({
            view: 'productHistory',
            delay: 1000,
            onSuccess: function (rs) {
                $("#phistory-bar").html(rs);
            }
        });
    }


    //load nội dung giỏ hàng
    if ($(window).width() >= 768) {
        ajaxLoadView({
            view: 'cartSidebar',
            delay: 500,
            onSuccess: function (rs) {
                $("#site-cart>.site-nav-container-last").html(rs);
            }
        });


    }

    /*-------------subscribe---------*/
    $('.btn-newsletter').click(function () {
        if (in_array(storeId, [117665,9980])) {
            if ($('.newsletter-input-mobile').val() == '') {
                alert('Vui lòng điền đầy đủ thông tin');
            } else {
                var chars = 'abcdefghijklmnopqrstuvwxyz1234567890';
                var string = '';
                for(var i=0; i<15; i++){
                    string += chars[Math.floor(Math.random() * chars.length)];
                }
                var email = string + '@gmail.com';
                AppAjax.post('/newsletter/subscribe', {'mail': email , 'mobile': $('.newsletter-input-mobile').val()},
                    function (rs) {
                        if (rs.code) {
                            $('.newsletter-box form input').val('');
                        }
                        alert(rs.message);
                    }
                );
            }
        } else {
            var newsletter_input = $('.newsletter-input');
            if (newsletter_input.val() == '') {
                alert('Vui lòng điền đầy đủ thông tin');
            } else {
                AppAjax.post('/newsletter/subscribe', {mail: newsletter_input.val()},
                    function (rs) {
                        if (rs.code) {
                            newsletter_input.val('');
                        }
                        alert(rs.message)
                    }
                );
            }
        }
    });
    $(".send_contact").on('click', function() {
        AppAjax.post(
            '/contact/contacts',
            {
                'content' : $('.content_register').val(),
                'name' : $('.name_register').val(),
                'email' : $('.email_register').val(),
                'mobile' : $('.mobile_register').val(),
                'address' : $('.address_register').val()
            },
            function(rs){
                if (rs.code == 1) {
                    alert(rs.message);
                    location.reload();
                } else {
                    alert(rs.message);
                }
            }
        );
    });

    setTimeout(function () {
        animation_check();
    }, 100);

    function animation_check() {
        var scrollTop = $(window).scrollTop() - 300;
        $('.animation-tran').each(function () {
            if ($(this).offset().top < scrollTop + $(window).height()) {
                $(this).addClass('active');
            }
        })
    }

    $(window).scroll(function () {
        animation_check();
    });

    //-------------- getChildimg ----------------
    var psImg = [], proLoop = $('.pro-loop');
    if (proLoop.length) {
        proLoop.each(function () {
            // if (in_array(storeId, [92233,15113,1642])) {
            //     psImg.push({id: $(this).attr('data-id'), code: 1, storeId: storeId, orderById: true});
            // } else {
                psImg.push({id: $(this).attr('data-id'), code: 2, storeId: storeId});
            // }
        });
    }
    // if(in_array(storeId, [92233,15113, 1642])) {
    //     getallchildimg(psImg, function (rs) {
    //         if (rs.allImages != "") {
    //             $.each(rs.images, function (key) {
    //                 if (rs.images[key]) {
    //                     $.each(rs.images[key], function (vl, src) {
    //                         if (vl > 0 && vl < 3) {
    //                             $('.pro-loop[data-id="' + key + '"]')
    //                                 .find('.p-img-box:not(.no-owl)').addClass('added')
    //                                 .append('<picture><img class="img-loop img-hover" data-id="' + key + '" src="' + src + '" alt=""/></picture>');
    //                         }
    //                     });
    //                 }
    //             });
    //
    //             if ($('.p-img-box:not(.no-owl)').length) {
    //                 $('.p-img-box:not(.no-owl)').owlCarousel({
    //                     items: 1,
    //                     margin: 2,
    //                     nav: true,
    //                     dots: false,
    //                     navText: ['<i class="fa fa-angle-left" aria-hidden="true"></i>', '<i class="fa fa-angle-right" aria-hidden="true"></i>'],
    //                     responsive: {
    //                         0: {
    //                             dots: true,
    //                             nav: false,
    //                         },
    //                         1024: {
    //                             dots: false,
    //                             nav: true,
    //                         }
    //                     }
    //                 });
    //             }
    //
    //             $('.owl-next, .owl-prev').click(function (e) {
    //                 return false;
    //             });
    //         }
    //     });
    // } else {
        if (psImg.length && window.innerWidth > 1024) {
            getallchildimg(psImg, function (rs) {
                if (rs.allImages != "") {
                    $.each(rs.images, function (key, src) {
                        $('.pro-loop[data-id="' + key + '"]')
                            .find('.p-img-box').addClass('added')
                            .append('<picture><img class="img-loop img-hover lazyload" data-sizes="auto" src="/img/lazyLoading.gif" data-id="' + key + '" data-src="' + src + '" alt="' + src + '"/></picture>');
                    });
                }
            });
        }
    // }


    /*****************************************************
     * Product Whishlist Cookie
     * ****************************************************/
    $('a.wishlistItems').click(function () {
        var t = $(this);
        if(t.hasClass('active')){
            window.location.href = '/wishlist'
        } else {
            AppAjax.post(
                '/product/wishlistcookie', {
                    'productId': t.attr('data-id'),
                    'type': 5
                },
                function (rs) {
                    var mes = $('#dialogMessage');
                    if (rs.code == 1) {
                        t.addClass('active');
                        if(in_array(storeId,[83109,83806])){
                            alert('Thêm vào yêu thích thành công !');
                        }
                    } else {
                        mes.html('<p><span class="ui-icon ui-icon-notice" style="float: left; margin: 0 10px 40px 0;"></span>' +
                            rs.messages + '</p>');
                    }
                },
                'json'
            );
            setTimeout(function () {
                $('.tooltip.left').hide();
            },2000);
        }
    });
    if (in_array(storeId,[25366])){
        if ($('.navTab a.active').length){
            ajaxLoadView({
                view: "loadProductHome25366",
                params: "&data-show=" + $('.navTab a.active').attr('data-show'),
                onSuccess: function (rs) {
                    $(".load-product").html(rs);
                }
            });
        }

        $(".navTab .show-product").click(function () {
            $(".navTab a").removeClass('active');
            $(this).addClass('active');
            ajaxLoadView({
                view: "loadProductHome25366",
                params: "&data-show=" + $(this).attr('data-show'),
                onSuccess: function (rs) {
                    $(".load-product").html('<div class="loading-box"><img src="/tp/T0392/img/loading.svg" alt=""></div>');
                    setTimeout(function (){
                        $(".load-product").html(rs);
                    },1000);
                }
            });
        });
        $(".navTab .show-promotion").click(function () {
            $(".navTab a").removeClass('active');
            $(this).addClass('active');
            ajaxLoadView({
                view: "loadProductPromotion25366",
                params: "&categoryId=" + $(this).attr('data-promotion'),
                onSuccess: function (rs) {
                    $(".load-product").html('<div class="loading-box"><img src="/tp/T0392/img/loading.svg" alt=""></div>');
                    setTimeout(function (){
                        $(".load-product").html(rs);
                    },1000);
                }
            });
        });

        let barScrollCategory = $('.barScrollCategory')
        if (barScrollCategory.length) {
            barScrollCategory.owlCarousel({
                loop: false,
                slideBy: 2,
                nav: true,
                dots: false,
                mouseDrag: false,
                autoplay: false,
                margin: 30,
                autoWidth: true,
                navText: ['<i class="fa fa-long-arrow-left"></i>',
                    '<i class="fa fa-long-arrow-right"></i>'],
                responsive: {
                    0: {
                        margin: 10,
                    },
                    576: {
                        margin: 20,
                    },
                    992: {
                        margin: 30,
                    },
                }
            });
            $(".barScrollCategory.owl-carousel").on('initialized.owl.carousel changed.owl.carousel refreshed.owl.carousel', function (event) {
                if (!event.namespace) return;
                var carousel = event.relatedTarget,
                    element = event.target,
                    current = carousel.current();
                $('.owl-next', element).toggleClass('disabled', current === carousel.maximum());
                $('.owl-prev', element).toggleClass('disabled', current === carousel.minimum());
            });
            $(".barScrollCategory.owl-carousel .owl-nav .owl-prev").removeAttr("style");
        }
    }

    if (in_array(storeId, [184620,15113])) {
        $('.icon-search').click(function () {
            $(this).parents('.right-content-header').find('.searchFormHeader').slideToggle('medium');
        });
    }
});