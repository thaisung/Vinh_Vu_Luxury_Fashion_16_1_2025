$(function () {
    var storeId = $('#storeId').val();
    if($(".datepicker").length){
        $( ".datepicker" ).datepicker({ dateFormat: 'dd/mm/yy' });
    }
    // $('.section-customer-information .section-content-text').hide();
    // if ( window.location.href.includes('checkout') ) {
    //     $('#form_update_location').parent().append('<h3 class="notice" style="color:#f77705;font-style:italic;margin: 1.5em auto 0.3em 5px;">Vui lĂ²ng nháº­p Ä‘áº§y Ä‘á»§ thĂ´ng tin Ä‘á»‹a chá»‰ Ä‘á»ƒ nháº­n hĂ ng nhanh hÆ¡n!</h3>');
    //     $('.order-summary.order-summary-is-collapsed').find('h3').remove();
    //     $('.order-summary.order-summary-is-collapsed').append('<h3 class="notice-checkout" style="font-weight: 400; padding: 10px; border: 1px solid #f77705; line-height: 18px; margin: 0;">Juno sáº½ XĂC NHáº¬N Ä‘Æ¡n hĂ ng báº±ng TIN NHáº®N SMS hoáº·c Gá»ŒI ÄIá»†N. Báº¡n vui lĂ²ng kiá»ƒm tra TIN NHáº®N hoáº·c NGHE MĂY ngay khi Ä‘áº·t hĂ ng thĂ nh cĂ´ng vĂ  CHá»œ NHáº¬N HĂ€NG</h3>');
    // }
    // $('input[data-discount-field="true"]').closest('.fieldset').prepend('<div style="color:#f77705;margin-left:9px;font-weight:bold;display:none;">Nháº­p mĂ£ giáº£m giĂ¡ táº¡i Ä‘Ă¢y (náº¿u cĂ³)</div>')

    Address.load('#cityId', '#districtId', '#wardId');
    $('input[name="paymentMethod"]').change(function () {
        var t = $(this), baokimId = $('#baokimPmMethodId');
        if ($(t.attr('data-show')).length) {
            baokimId.removeAttr('value');
        } else {
            baokimId.val('Baokim');
        }
        if (t.hasClass('baokim')) {
            baokimId.val('Baokim');
        }
        if (t.hasClass('cod')) {
            baokimId.val('cod');
        }
        $('.transfer-infor, .cod_description, .fundiin-desc').slideUp();
        $('.listBank').slideUp();
        $('.listBank>span').removeClass('active');
        $(t.attr('data-show')).slideDown();
        if (t.val() == 1) {
            $('.cod_description').slideDown();
        }
        if (t.val() == 100) {
            $('.fundiin-desc').slideDown();
        }
        if (in_array(storeId, [102850, 29296])) {
            baokimId.val($(this).val());
            $(".chosen-method").text($(this).attr('data-method'))
        }
        if($('.onlyOneBank').length && !$('.listBankWrp').hasClass('deactive_bank')){
            $('.listBankWrp .form-group').removeClass('active').addClass('active');
            $('.listBankWrp .form-group.active .item-Bank').find("input[name='banks']").prop("checked", true);
            let bankId = $('.listBankWrp .form-group.active .item-Bank').attr('data-bankId'),
                bankAccountNumber = $('.listBankWrp .form-group.active .item-Bank').attr('data-bankNumber'),
                bankAccountHolder = $('.listBankWrp .form-group.active .item-Bank').attr('data-bankHolder'),
                bankName = $('.listBankWrp .form-group.active .item-Bank').attr('data-bankName'),
                resultContainer = $('.rs_' + bankAccountNumber),
                amount = $('#showTotalMoney').attr('value');
            if($('#showTotalMoney').attr('current-value') !== undefined){
                amount = $('#showTotalMoney').attr('current-value');
            }
            $("input[name='banks']").attr('checked',false);
            GetQRPaymentCode.load(bankId,bankAccountNumber,bankAccountHolder,bankName,resultContainer, amount);
        }
        // $(".fundiin-desc").slideUp();
        // if (t.hasClass('fundiin')) {
        //     $(".fundiin-desc").slideDown();
        // }
    });
    $('.item-Bank').on('click', function (e) {
        $('.listBankWrp .form-group').removeClass('active');
        $('#baokimPmMethodId').val('Bank');
        $(this).parents('.form-group').addClass('active');
        $('.item-Bank').find("input[name='banks']").prop("checked", false);
        $(this).find("input[name='banks']").prop("checked", true);
        let bankId = $(this).attr('data-bankId'),
            bankAccountNumber = $(this).attr('data-bankNumber'),
            bankAccountHolder = $(this).attr('data-bankHolder'),
            bankName = $(this).attr('data-bankName'),
            resultContainer = $('.rs_' + bankAccountNumber),
            amount = $('#showTotalMoney').attr('value');
        if ($('#showTotalMoney').attr('current-value') !== undefined) {
            amount = $('#showTotalMoney').attr('current-value');
        }
        GetQRPaymentCode.load(bankId, bankAccountNumber, bankAccountHolder, bankName, resultContainer, amount);
        e.preventDefault();
    });
    $('.transfer-infor').slideUp();
    $('.transfer').change(function () {
        $(this).parent('.radio-wrapper').find('.transfer-infor').slideDown();
        $('.listBank').slideUp();
    });

    $('.listBank>span').click(function () {
        $('#baokimPmMethodId').val($(this).attr('data-baokimPmId'));
        $('.listBank>span').removeClass('active');
        $(this).addClass('active');
    });

    if ($('.cod[name="paymentMethod"]:checked')) {
        $('#baokimPmMethodId').val('Baokim');
    }
    $('input[name="checkBoxGift"]').change(function () {
        window.location.href = $(this).val();
    });

    if (in_array(storeId, [92233,149448, 15113, 1642,106986,34369,175218])) {
        $(".coupon").click(function () {
            $(".coupon").removeClass('active');
            $(this).addClass('active');
            var code = $(this).find('.d-code').text();
            $("#coupon").val(code)
        });
    }

    let currency = '';
    if (in_array(storeId, [102850, 29296])) {
        currency = 'Ä‘';
    }

    CheckCouponCode.load('#cityId', '#districtId', '#coupon', '#getCoupon', '#txtCode', '#shipFee', '#showTotalMoney' , currency);

    if(in_array(storeId,[79592,157317, 7888])) {
        $('#submitCart').click(function () {
            window.location.href = '/user/signin?redirectUri='+ encodeURIComponent('/cart/checkout');
        });
        $('input[name="shippingMethod"]').change(function () {
            var t = $(this);
            if (t.hasClass('cod')) {
                $('.note-shipping').slideDown();
            }else {
                $('.note-shipping').slideUp();
            }
        });
    }else {
        CustomerShipFee.load('#cityId', '#districtId', '#shipFee', '#showTotalMoney', '#coupon');
    }
    // Check khĂ¡ch hĂ ng nháº­p sdt sáº½ show ra thĂ´ng tin + CTKM Ä‘Æ¡n hĂ ng theo khĂ¡ch hĂ ng Ä‘Ă³
    if(in_array(storeId,[81])){
        // ======= Check user mobile promotion ==================
        $(document).on("click", ".checkCustomer" , function() {
            $(this).hide();
            CheckPromotionOrder.load('#totalDiscount','#showTotalMoney','#shipFee','');
            $('input[name="customerName"]').val($(this).attr('data-name'));
            $('input[name="customerEmail"]').val($(this).attr('data-email'));
            $('input[name="customerAddress"]').val($(this).attr('data-address'));
            Address.getDistricts($(this).attr('data-cityLocationId'), '#districtId');
            Address.getWards($(this).attr('data-districtLocationId'), '#wardId');
            $('#cityId option[value='+$(this).attr('data-cityLocationId')+']').attr('selected','selected');
            $('#districtId option[value='+$(this).attr('data-districtLocationId')+']').attr('selected','selected');
            $('#wardId option[value='+$(this).attr('data-wardLocationId')+']').attr('selected','selected');
            $('#orderDiscount').show();
        });

        $(document).mouseup(function (e) {
            if ($(e.target).closest("#searchCustomer").length === 0) {
                $("#searchCustomer").hide();
            }
        });
        var mobile = $('#formCheckOut input[name="customerMobile"]'),
            userSignIn = $('.userSignIn');
        if(userSignIn.length <= 0){
            if(isset($.cookie('cod'))){
                let user = json_decode($.cookie('cod'));
                searchCustomer(user.mobile);
            }
            mobile.autocomplete({
                source: function() {
                    searchCustomer(mobile.val());
                }
            });
            mobile.keyup(function() {
                if (!$(this).val().length) {
                    $('#searchCustomer').slideUp();
                }
            }).
            focus(function() {
                if ($(this).val().length) {
                    $('#searchCustomer').slideDown();
                } else {
                    $(this).attr('placeholder', '');
                }
            }).
            focusout(function() {
                if (!$('#searchCustomer a').click) {
                    if (!$(this).val().length) {
                        $(this).attr('placeholder', msgSearchProduct).val('');
                    }
                    $('#searchCustomer').slideUp();
                }
            });
        }
        // ======= End Check user mobile promotion ==================
    }


    var isSubmited = false, viewSuccess = $('#viewSuccess').val();
    

    if (in_array(storeId, [98159])) {
        let fundiinJson = "https://fundiin.vn/merchant-gateway/api/merchant-website-ui-config/checkout/get-by-domain?domain=https://butuni.com/";
        $.getJSON(fundiinJson, {
            format: "json"
        }).done(function (data) {
            $('.fundiin-tittle').html('<img alt="fundiin" src="'+data.title_image+'"><span>' + data.title_text +'</span>');
            $('.fundiin-desc ').html(data.description);
        });
    }

    if (in_array(storeId, [102850, 29296])) {
        $(".buy-more").click(function (e) {
            e.preventDefault();
            if ($(this).attr('data-ck') > 0) {
                var qty = 1,
                    products = [{id: $(this).attr('data-id'), quantity: qty}];
                addToCart(products, 1, function(rs){
                    if (rs.status == 1) {
                        ajaxLoadView({
                            view: 'cartSidebar',
                            onSuccess: function (rs) {
                                $("#site-cart>.site-nav-container-last").empty();
                                $("#site-cart>.site-nav-container-last").html(rs);
                                $(".cart-checkout").addClass('loadingChange');
                                $(".addNoty").addClass('in');
                                $(".cart-noty").remove();
                                setTimeout(function () {
                                    ajaxLoadView({
                                        view: 'loadProductCheckout102850',
                                        onSuccess: function (rs) {
                                            $('.product-checkout').html(rs);
                                        }
                                    });
                                    ajaxLoadView({
                                        view: 'loadPriceCheckout102850',
                                        onSuccess: function (rs) {
                                            $('.total-checkout').html(rs);
                                        }
                                    });
                                    ajaxLoadView({
                                        view: 'loadButtonCheckout102850',
                                        onSuccess: function (rs) {
                                            $('.total-money-text').html(rs);
                                        }
                                    });
                                    $(".cart-checkout").removeClass('loadingChange');
                                    $(".addNoty").removeClass('in');
                                }, 2000);
                            }
                        });
                    } else {
                        alert(rs.messages);
                    }
                });
            } else {
                if ($(window).width() < 768) {
                    window.location.href = $(this).attr('data-href');
                } else {
                    var url = '/product/q' +  $(this).attr('data-id');
                    $.ajax({
                        url: url,
                        type: 'GET',
                        dataType: 'text',
                        success: function (data) {
                            $("#quickview-cart-desktop").html(data);
                            $('#quickview-cart').modal('show');
                        }
                    });
                }
            }
        });
        $('.pci-remove').on('click', function () {
            $(".removeNoty").addClass('in');
            var psId = $(this).attr('data-id');
            $.post(
                '/cart/remove',
                {'psId': psId},
                function () {
                    $(".cart-checkout").addClass('loadingChange');
                    setTimeout(function () {
                        ajaxLoadView({
                            view: 'loadProductCheckout102850',
                            onSuccess: function (rs) {
                                $('.product-checkout').html(rs);
                            }
                        });
                        ajaxLoadView({
                            view: 'loadPriceCheckout102850',
                            onSuccess: function (rs) {
                                $('.total-checkout').html(rs);
                            }
                        });
                        ajaxLoadView({
                            view: 'loadButtonCheckout102850',
                            onSuccess: function (rs) {
                                $('.total-money-text').html(rs);
                            }
                        });
                        $(".cart-checkout").removeClass('loadingChange');
                        $(".removeNoty").removeClass('in');
                    }, 2000);
                }
            );
        });
    }

    // $('.cart_remove').on('click', function () {
    //     var psId = $(this).attr('data-id');
    //     var check = confirm('Báº¡n muá»‘n xĂ³a sáº£n pháº©m nĂ y ?');
    //     if (check) {
    //         $.post(
    //             '/cart/remove',
    //             {'psId': psId},
    //             function () {
    //                 window.location.reload();
    //             }
    //         );
    //     }
    // });
    
    // tieu diem
    if($('#cusUsedPoint').length) {
        mobile = $.trim($('.customerPointCheck').val());
        var time = '1000';
        if (in_array(storeId, [175246])) {
            time = '5000';
        }
        if (mobile) {
            customerPoint(mobile);
        }
        $('.customerPointCheck').change(function () {
            customerPoint($(this).val());
        });
        $('#cusUsedPoint').keyup(function () {
            var t = $(this);
            setTimeout(function () {
                var cusUsedPoint = t.val();
                var mobile = $('.customerPointCheck').val();
                var ttmoney = parseInt($('.block_Points').attr('data-money'));
                var ship = parseInt($('#shipFee').text().replace('â‚«', '').replace(',', '').replace(' ', '').replace('vnÄ‘', ''));
                if (!ship) {
                    ship = 0;
                }
                var couponDiscount = 0;
                if (parseInt($('#txtCode').attr('data-coupon')) > 0) {
                    couponDiscount = parseInt($('#txtCode').attr('data-coupon'));
                }
                // console.log(cusUsedPoint);
                if (cusUsedPoint && mobile) {
                    AppAjax.post(
                        '/customer/infocustomer',
                        {
                            mobile: mobile,
                            cusUsedPoint: cusUsedPoint
                        },
                        function (rs) {
                            if (rs.code == 1) {
                                $('#moneyPoint b').html($.number(rs.money) + ' Ä‘');
                                $('#moneyPoint').show();
                                var tt_after = ttmoney + ship - couponDiscount - parseInt(rs.money);
                                if (tt_after < 0) {
                                    tt_after = 0;
                                }
                                $('#showTotalMoney').html($.number(tt_after) + 'Ä‘');
                            } else {
                                if (rs.messages) {
                                    alert(rs.messages);
                                }
                                $('#moneyPoint').hide();
                                $('#cusUsedPoint').val('');
                                $('#showTotalMoney').html($.number(ttmoney + ship - couponDiscount) + 'Ä‘');
                            }
                        }
                    )
                } else {
                    $('#moneyPoint').hide();
                    $('#cusUsedPoint').val('');
                    $('#showTotalMoney').html($.number(ttmoney + ship - couponDiscount) + 'Ä‘');
                }
            },time);
        });
    }
});
function customerPoint(mobile) {
    if (! validateMobile(mobile)) {
        alert(msgInvalidMobile);
        $('.customerPointCheck').val('');
        $('#cusUsedPoint').val('');
        $('#cusPoint').html('0 ' + txtPoint);
    } else {
        AppAjax.post(
            '/customer/infocustomer',
            {
                mobile: mobile
            },
            function (rs) {
                if (rs.code == 1) {
                    $('#cusPoint').html($.number(rs.point) +" "+ txtPoint);
                } else {

                    $('#cusUsedPoint').val('');
                    $('#cusPoint').html('0 ' + txtPoint);
                    if (rs.messages) {
                        alert(rs.messages);
                    }
                }
            }
        )
    }
}
function searchCustomer(mobile){
    let s = $('#searchCustomer');
    s.slideDown();
    AppAjax.post(
        '/customer/search',
        {
            customerMobile: mobile,
            showCustomerAjax: 1
        },
        function(rs) {
            s.empty();
            if (rs.code === 1) {
                if(rs.data.name !== null){
                    // CheckPromotionOrder.load('#totalDiscount','#showTotalMoney','#shipFee','');
                    // $('#orderDiscount').show();
                    s.append('<a class="checkCustomer" data-mobile="' + rs.data.mobile + '" data-name="'+rs.data.name+'" data-cityLocationId="'+rs.data.cityLocationId+'" data-districtLocationId="'+rs.data.districtLocationId+'" data-wardLocationId="'+rs.data.wardLocationId+'" data-address="'+rs.data.address+'" data-email="'+rs.data.email+'">' + rs.data.name + '</a>');
                }
            }
        }
    );
}