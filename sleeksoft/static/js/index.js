var $storeId = document.getElementById('storeId').value;
$(document).ready(function () {
    setTimeout(function () {
        var height = jQuery(".tab-content").outerHeight() / 2;
        $(".product-lists-home").css("min-height", height);
    }, 500);
    $(".tab-pane:not(.active) .product-lists").hide();

    // this.sliderCollection();
    var itemShow = 2, attr_show = $('.slideProductBanner').attr('data-slide-to-show');
    if (attr_show) {
        itemShow = attr_show;
    }
    $('.slideProductBanner').slick({
        centerPadding: '20px',
        slidesToShow: itemShow,
        autoplay: true,
    });

    // this.clickPanel();
    if(!in_array($storeId, [106986,34369])) {
        $(document).on("click", ".sectionContentTab a:not(.notClick)", function () {
            var link = $(this).attr("href");
            window.location.href = link;
        });
    }

    if (in_array($storeId, [662, 15113])) {
        $(".sliderMobileBannerHome").owlCarousel({
            items: 3,
            nav: false,
            navText: ['<i class="fa fa-chevron-left"></i>', '<i class="fa fa-chevron-right"></i>'],
            touchDrag: true,
            responsive: {
                0: {
                    items: 1,
                },
                992: {
                    items: 2,
                },
                1024: {
                    items: 3
                }
            }
        });
    }

    // this.removeOptimize();
    if ($(window).width() >= 768) {
        $(".visible-xs").remove();
    } else {
        // this.slideBannerMobile();
        var $slideToshow = 1;
        var $nav = true;
        if(in_array($storeId, [662])) {
            $nav = false;
        }
        if(in_array($storeId, [132241,11503])) {
            var $slideToshow = 2;
        }
        if (!in_array($storeId, [72396,17637,106986,34369,662])){
            $('.sliderMobileBannerHome').on('init', function () {
                $('.sliderMobileBannerHome .slick-list').css('display', 'block');
            });
            $('.sliderMobileBannerHome').slick({
                slidesToShow: $slideToshow,
                autoplay: true,
                arrows: $nav,
                lazyLoad: 'ondemand',
            });
        }
    }
    if (in_array($storeId, [187852,15113])) {

        if ($(".section-category-home .categories-home-list").length) {
            $(".section-category-home .categories-home-list").owlCarousel({
                items: 4,
                nav: true,
                dots: true,
                loop: true,
                autoplay: true,
                autoplayTimeout: 3000,
                margin: 10,
                navText: ['<i class="fa fa-chevron-left"></i>', '<i class="fa fa-chevron-right"></i>'],
                lazyLoad: true,
                touchDrag: true,
                responsive: {
                    0: {
                        items: 2,
                    },
                    767: {
                        items: 1,
                    },
                    1024: {
                        items: 4
                    }
                }
            });
        }
        if ($(".bestseller-pro .product-lists-home").length) {
            $(".bestseller-pro .product-lists-home").owlCarousel({
                items: 4,
                nav: true,
                autoplay: true,
                dots: true,
                margin: 10,
                navText: ['<i class="fa fa-chevron-left"></i>', '<i class="fa fa-chevron-right"></i>'],
                lazyLoad: true,
                touchDrag: true,
                responsive: {
                    0: {
                        items: 2,
                    },
                    767: {
                        items: 1,
                    },
                    1024: {
                        items: 4
                    }
                }
            });
        }
        if ($('.videos-home-list').length){
            $('.videos-home-list').owlCarousel({
                loop: true,
                margin: 10,
                nav: false,
                autoplay: false,
                autoplayHoverPause: true,
                items: 1,
                responsive: {
                    0: {
                        items: 1
                    },
                    600: {
                        items: 2
                    },
                    1000: {
                        items: 4
                    }
                }
            });
        }

        $(document).on('click', '.video-link', function () {
            let videoUrl = $(this).data('video');
            $('#modal-video-container iframe').attr('src', videoUrl + '?autoplay=1&rel=0&muted=0');
        });
        $('#videoModal').on('hidden.bs.modal', function () {
            $('#modal-video-container iframe').attr('src', '');
        });
    }
    if ($('#load-pCategory').length) {
        // load danh mục sản phẩm trang chủ
        var $viewName = '';
        if(in_array($storeId,[41781])) {
            $viewName = 'homeCategory41781';
        }else if(in_array($storeId,[57850])) {
            $viewName = 'homeCategory57850';
        }else if(in_array($storeId, [70105])) {
            $viewName = 'homeCategory70105';
        }else if(in_array($storeId, [146765])) {
            $viewName = 'homeCategory146765';
        }else if(in_array($storeId, [158789])) {
            $viewName = 'homeCategory158789';
        }else {
            $viewName = 'homeCategory';
        }
        ajaxLoadView({
            view: $viewName,
            onSuccess: function (rs) {
                $('#load-pCategory').html(rs)
            }
        });
    }

    // if ($('#load-homeNews').length) {
    //     ajaxLoadView({
    //         view: 'homeNews',
    //         delay: 1700,
    //         onSuccess: function (rs) {
    //             $('#load-homeNews').html(rs)
    //         }
    //     });
    // }

    if ($('#load-homeAlbums').length) {
        ajaxLoadView({
            view: 'homeAlbums',
            delay: 2000,
            onSuccess: function (rs) {
                $('#load-homeAlbums').html(rs)
            }
        });
    }


    var trackingBannerHome1 = $('.trackingBannerHome1');
    if (trackingBannerHome1.length) {
        //nếu nhiều hơn 1 slide thì để loop là True
        var loop = false;
        var $nav = false;
        var $autoPlay = true;
        // if($(window).width() > 768 && (in_array($storeId,[92233,15113, 3676]))){
        //     $autoPlay = false;
        // }
        if($(window).width() < 768){
            if(in_array($storeId,[662])) {
                var $nav = false;
            } else {
                var $nav = true;
            }
        }
        if (in_array($storeId, [92233])) {
            $nav = true;
        }
        if ($('.trackingBannerHome1>a').length > 1) {
            loop = true;
        }
        if(in_array($storeId,[2071])){
            trackingBannerHome1.owlCarousel({
                items: 1,
                nav: $nav,
                dots: $nav,
                autoplay: true,
                autoplayTimeout: 4000,
                lazyLoad: true,
                touchDrag: true,
                navText: ['<i class="fa fa-chevron-left"></i>', '<i class="fa fa-chevron-right"></i>'],
                loop: false,
                responsive: {
                    0: {
                        items: 1,
                    },
                    767: {
                        items: 1,
                    },
                    1024: {
                        items: 1
                    }
                }
            });

        }else {
            trackingBannerHome1.owlCarousel({
                items: 1,
                nav: $nav,
                dots: true,
                autoplay: $autoPlay,
                autoplayTimeout: 4000,
                lazyLoad: true,
                touchDrag: true,
                loop: loop,
                responsive: {
                    0: {
                        items: 1
                    },
                    767: {
                        items: 1
                    },
                    1024: {
                        items: 1
                    }
                }
            });
        }
    }
    if(in_array($storeId,[116760])) {
        if($('.slide_bn_da').length) {
            $('.slide_bn_da').owlCarousel({
                items: 1,
                nav: false,
                dots: false,
                autoplay: true,
                margin: 30,
                responsive: {
                    0: {
                        items: 1
                    },
                    767: {
                        items: 3
                    }
                }
            })
        }
    }
    if(in_array($storeId,[41781])){
        $('.product-lists-home').owlCarousel({
            items: 4,
            nav: true,
            navText: ['‹' , '›'],
            // dots: false,
            autoplay: true,
            autoplayTimeout: 4000,
            lazyLoad: true,
            touchDrag: true,
            loop: false,
            responsive: {
                0: {
                    items: 2
                },
                767: {
                    items: 2
                },
                1024: {
                    items: 4
                }
            }
        });
        $('.banner-feedback').owlCarousel({
            items: 3,
            margin: 10,
            nav: false,
            navText: ['‹' , '›'],
            // dots: false,
            autoplay: true,
            autoplayTimeout: 4000,
            lazyLoad: true,
            touchDrag: true,
            loop: false,
            responsive: {
                0: {
                    items: 1
                },
                767: {
                    items: 1
                },
                1024: {
                    items: 3
                }
            }
        });
    }

    if(in_array($storeId,[57850,34285])) {
        /*******------- form subcribe popup -------*******/
        $('#contactFormSubmit-popup').click(function (e) {
            e.preventDefault();
            AppAjax.post('/newsletter/subscribe', {
                    mail: $('#contactFormEmail-popup').val(),
                    name: $('#contactFormName-popup').val(),
                    mobile: $('#contactFormPhone-popup').val(),
                    gender: $("input.genderList[name='gender']:checked").val(),
                },
                function (rs) {
                    if (rs.code == 1) {
                        $('#contactFormEmail-popup').val('');
                        parent.jQuery.fancybox.close();
                    }
                    alert(rs.message);
                });
        });
    }else {
        /*******------- form subcribe popup -------*******/
        $('#contactFormSubmit-popup').click(function (e) {
            e.preventDefault();
            AppAjax.post('/newsletter/subscribe', {
                    mail: $('#contactFormEmail-popup').val(),
                },
                function (rs) {
                    if (rs.code == 1) {
                        $('#contactFormEmail-popup').val('');
                        parent.jQuery.fancybox.close();
                    }
                    alert(rs.message);
                });
        });
    }
    if(in_array($storeId,[112857])) {
        if($('.testimonial_carousel').length){
                $('.testimonial_carousel').each(function(){
                    var $self = $(this);
                    $(this).carouFredSel({
                        auto: true,
                        scroll: { items : 1, fx: 'fade' },
                        prev : {
                            button : $self.parent('.testimonial_carousel_element').find('.prev')
                        },

                        next : {
                            button : $self.parent('.testimonial_carousel_element').find('.next')
                        },
                        height : 'auto',
                        width : '100%',
                        items : {
                            height : 'auto',
                            width: 'auto'
                        },

                    });

                });
            }
    }
});
