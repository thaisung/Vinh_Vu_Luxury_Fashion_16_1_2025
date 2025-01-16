$(function () {
    $('input[name=customerName]').focus();
    $('input[name=username]').focus();
    if($('.btn-show-pass').length){
        $('.btn-show-pass').on('click', function(){
            $(this).find('i').toggleClass('fa-eye-slash');
            if($(this).find('i').hasClass('fa-eye-slash')) {
                $(this).next('input').attr('type','text');
            } else {
                $(this).next('input').attr('type','password');
            }
            $(this).next('input').focus();
        });
    }
    if($('.nvn_table_of_contents_heading').length){
        $(document).on('click', '.nvn_table_of_contents_heading', function(e) {
            e.preventDefault();
            $(this).next().slideToggle();
        });
    }
    // lưu cookie theo chi nhánh
    try {
        if ($('#loadStoreBranchs').length) {
            $('#loadStoreBranchs').modal({
                show: true,
                backdrop: 'static'
            });
            $('#storeBranch>button').click(function () {
                $.cookie('STORE_BRANCH', $(this).data('id'), {path: '/', expires: 10});
                $('#loadStoreBranchs').modal('hide');
                location.reload();
            });
        }
        $('.brandSelect').change(function () {
            $.cookie('STORE_BRANCH', $(this).val(), {path: '/', expires: 10});
            location.reload();
        });
    } catch (e) {
        // TODO: handle exception
    }
    if($('.showHideArticleSectionMenu').length) {
        $(".boxContentGuide").css('display', 'none');
        $(".showHideArticleSectionMenu").on('click',function () {
            if ($(this).text() == "show" || $(this).text() == "Show") {
                $(".boxContentGuide").css('display', 'block');
                $(this).text('hide');
            } else {
                $(".boxContentGuide").css('display', 'none');
                $(this).text('show');
            }
        });
    }
    // change Skin
    $('#settingSkins>div>.fa-cog').click(function () {
        $('#settingSkins').toggleClass('showSkin');
    });
    if ($('.tooltipSkin').length) {
        $('.tooltipSkin').tooltip();
    }

    $('#settingSkins>div>ul>li').click(function () {
        $.removeCookie("skin");
        $.cookie('skin', $(this).attr('data-color'), {path: '/'});
        location.reload();
    });
    $('#skinDefault').click(function () {
        $.removeCookie("skin");
        location.reload();
    });
    $(window).load(function(){
        // window.setTimeout( load_fb_chat, 8000);
        load_fb_chat();
    });
    $(document).on('click', '.userLike', function () {
        let type = $(this).attr('data-type'),
            userId = $(this).attr('data-userId'),
            commentId = $(this).attr('data-id');
        $.post(
            '/comment/likeComment',
            {
                'commentId': commentId,
                'typeId': type,
                'userId': userId
            },
            function (rs) {
                location.reload();
            }
        );
    });
    $(document).on('click', '.removeLike', function () {
        let type = $(this).attr('data-type'),
            userId = $(this).attr('data-userId'),
            commentId = $(this).attr('data-id');
        $.post(
            '/comment/removelike',
            {
                'commentId': commentId,
                'typeId': type,
                'userId': userId
            },
            function (rs) {
                location.reload();
            }
        );
    });
    if($('#ratingArea').length){
        ArticleContentView.init();
        ArticleContentView.initHover();
        ArticleContentView.checkRatedArticle($('#ratingArea').attr('data-id'));
    }
});
function load_fb_chat(){
    window.fbAsyncInit=function(){FB.init({xfbml:!0,version:"v9.0"})};function td_customerchat(){var t=document.createElement("script");t.async=!0,t.defer=!0,t.src="https://connect.facebook.net/vi_VN/sdk/xfbml.customerchat.js",document.body.appendChild(t)}window.addEventListener?window.addEventListener("load",td_customerchat,!1):window.attachEvent?window.attachEvent("onload",td_customerchat):window.onload=td_customerchat;
};
// window.fbAsyncInit = function() {
//     FB.init({
//         xfbml            : true,
//         version          : 'v14.0'
//     });
// };
// (function(d, s, id) {
//     var js, fjs = d.getElementsByTagName(s)[0];
//     if (d.getElementById(id)) return;
//     js = d.createElement(s); js.id = id;
//     js.src = 'https://connect.facebook.net/vi_VN/sdk/xfbml.customerchat.js';
//     fjs.parentNode.insertBefore(js, fjs);
// }(document, 'script', 'facebook-jssdk'));
/**
 * Hàm chung dùng để lẩy ảnh
 * Mục đích dùng để load ra ảnh thứ 2
 * productItems => Wrapper chứa sản phẩm có thuộc tính data-id + data-img
 * productHover => Ảnh muốn hover để hiện
 * type => Kiểu hiện ảnh, đang có 2 kiểu (picture hoặc image tag)
 * imgLazySource => Link ảnh lazyload muốn thêm vào khi load ảnh
 */
let productLoadImage = {
    load: function (productItems,productHover,type,imgLazySource) {
        $(productItems).each(function () {
            let productName = '';
            if($(productHover + $(this).attr('data-id')).attr('data-name')){
                productName = $(productHover + $(this).attr('data-id')).attr('data-name');
            }
            if(isNullAndUndef($(this).attr('data-img'))){
                if(type === 'picture'){
                    if(isNullAndUndef(imgLazySource)){
                        $(this).find(productHover + $(this).attr('data-id')).append('<source media="(max-width: 767px)" srcset="' + $(this).attr('data-img') + '">').append('<source media="(max-width: 767px)" srcset="' + $(this).attr('data-img') + '">').append('<img class="lazyload" alt="'+productName+'" src="'+imgLazySource+'" data-src="' + $(this).attr('data-img') + '">');
                    }else{
                        $(this).find(productHover + $(this).attr('data-id')).append('<source media="(max-width: 767px)" srcset="' + $(this).attr('data-img') + '">').append('<source media="(max-width: 767px)" srcset="' + $(this).attr('data-img') + '">').append('<img class="lazyload" alt="'+productName+'" src="/img/loading.gif" data-src="' + $(this).attr('data-img') + '">');
                    }
                }
                else if(type === 'image'){
                    $(this).find(productHover).attr('data-hover', $(this).attr('data-img'));
                    $(this).find(productHover).hover(function() {
                        if ($(this).attr('data-hover') != '') {
                            $(this).attr('tmp', $(this).attr('src')).attr('src', $(this).attr('data-hover')).attr('data-hover', $(this).attr('tmp')).removeAttr('tmp');
                        }
                    }).each(function () {
                        $('<img />').attr('src', $(this).attr('data-hover'));
                    });
                }
            }
        });
    },
    loadSlide: function (productItems,productHover,type,imgLazySource,lazyloadClass){
        $(productItems).each(function () {
            let productName = '';
            if($(productHover + $(this).attr('data-id')).attr('data-name')){
                productName = $(productHover + $(this).attr('data-id')).attr('data-name');
            }
            if(isNullAndUndef($(this).attr('data-img'))){
                if(type === 'picture'){
                    if(isNullAndUndef(imgLazySource)){
                        $(this).find(productHover + $(this).attr('data-id')).append('<source media="(max-width: 767px)" srcset="' + $(this).attr('data-img') + '">').append('<source media="(max-width: 767px)" srcset="' + $(this).attr('data-img') + '">').append('<img class="'+lazyloadClass+'" alt="'+productName+'" src="'+imgLazySource+'" data-src="' + $(this).attr('data-img') + '">');
                    }else{
                        $(this).find(productHover + $(this).attr('data-id')).append('<source media="(max-width: 767px)" srcset="' + $(this).attr('data-img') + '">').append('<source media="(max-width: 767px)" srcset="' + $(this).attr('data-img') + '">').append('<img class="'+lazyloadClass+'" alt="'+productName+'" src="/img/loading.gif" data-src="' + $(this).attr('data-img') + '">');
                    }
                }
                else if(type === 'image'){
                    $(this).find(productHover).attr('data-hover', $(this).attr('data-img'));
                    $(this).find(productHover).hover(function() {
                        if ($(this).attr('data-hover') != '') {
                            $(this).attr('tmp', $(this).attr('src')).attr('src', $(this).attr('data-hover')).attr('data-hover', $(this).attr('tmp')).removeAttr('tmp');
                        }
                    }).each(function () {
                        $('<img />').attr('src', $(this).attr('data-hover'));
                    });
                }
            }
        });
    }
};
/**
 * Hàm chung dùng để post data
 * Mục đích dùng để validate, chỉnh sửa, nâng cấp thì chỉ cần sửa ở 1 chỗ duy nhất
 * @type {{post: AppAjax.post}}
 */
var AppAjax = {
    // thêm hàm post để không phải sửa lại params chỉ cần thay $.post( => AppAjax.post(
    post: function (url, data, success, fail = false) {
        AppAjax.ajax({
            url: url,
            data: data,
            success: success,
            fail: fail
        });
    },

    ajax: function(options) {
        let url = options.url,
            userCommonCsrf = $("input[name='uctk']").val();
        if (! url || ! userCommonCsrf || userCommonCsrf !== $.cookie('nuctk')) {
            return false;
        }
        let dataPost = options.data ? options.data : '';
        if (! dataPost) {
            dataPost = {'userCommonCsrf' : userCommonCsrf};
        } else {
            // push userCommonCsrf vào data post lên
            // data truyền lên có thể có 3 dạng: data = id=1&storeId=2&type=..., hoặc data = {'a' : 1}, hoặc data = new FormData()
            if ($.isPlainObject(dataPost)) {
                dataPost.userCommonCsrf = userCommonCsrf;
            } else if ($.type(dataPost) === 'string') {
                dataPost += '&userCommonCsrf=' + userCommonCsrf;
            } else {
                dataPost.set('userCommonCsrf', userCommonCsrf);
            }
        }
        options.data = dataPost;
        options.type = 'POST';

        $.ajax(options);
    }
};

function mapGeneratorWithCurrentData(data, idMap) {
    let zoom = 17;
    if (data !== '') {
        query = data;
    }

    idMap.attr("src", generateMapUrl(query, zoom));
}

function generateMapUrl(query, zoom) {
    let googleMapsHostUrl = "https://maps.google.com/maps",
        paramString = "",
        urlParams = {
            hl: "vi",
            q: query,
            t: 'satellite',
            z: zoom,
            ie: "UTF8",
            iwloc: "B",
            output: "embed"
        };
    for (let key in urlParams) {
        paramString += key + "=" + urlParams[key] + "&";
    }
    return googleMapsHostUrl + "?" + encodeURI(paramString.replace(/.$/, ""));
}

function inIframe() {
    try {
        return window.self !== window.top;
    } catch (e) {
        return true;
    }
}

/**
 * @param products array
 * @param mode int (1=>add|2=>update)
 * @param callback (return data)
 */
function addToCart(products, mode, callback) {
    $.post(
        '/cart/add',
        {
            'products': products,
            'mode': mode
        },
        function (rs) {
            callback(rs);
        }
    );
}
function addToCartWithAttr(products, mode, attr = false, callback) {
    $.post(
        '/cart/add',
        {
            'products': products,
            'mode': mode,
            'attr': true,
        },
        function (rs) {
            callback(rs);
        }
    );
}

function addToBook(products, mode, callback) {
    $.post(
        '/cart/addbook',
        {
            'products': products,
            'mode': mode
        },
        function (rs) {
            callback(rs);
        }
    )
}

function addToBaseCart(options) {
    $.post('/carts/add', {'products': options.products, 'mode': options.mode},
        function (rs) {
            options.onSuccess(rs);
        }, 'json'
    );
}

function flyfly(options) {
    var position = options.position, itemDrag = options.iDrag, effect = options.effect;
    if (!effect) {
        effect = 'easeOutExpo';
    }
    if (itemDrag && position) {
        var itemClone = itemDrag.clone()
            .offset({
                top: itemDrag.offset().top,
                left: itemDrag.offset().left
            })
            .css({
                'opacity': '0.5',
                'position': 'absolute',
                'height': itemDrag.width(),
                'width': itemDrag.height(),
                'z-index': '999'
            })
            .appendTo($('body'))
            .animate({
                'top': position.offset().top + 5,
                'left': position.offset().left + 5,
                'width': position.width() - 10, 'height': position.height() - 10
            }, 1000, effect);
        itemClone.animate({
            'width': 0, 'height': 0
        }, function () {
            $(this).detach();
        });
    }
}

/**
 * remove cart items ($_$)
 * @param id int|array
 * @param callback (return data)
 * @param redirect bool
 */
function removeCart(id, redirect, callback) {
    if (!id) {/* remove all*/
        $.post('/cart/remove',
            function (rs) {
                if (redirect) {
                    window.location.reload();
                }
                callback(rs);
            }, 'json'
        );
    } else {
        $.post('/cart/remove', {'psId': id},
            function (rs) {
                if (redirect) {
                    window.location.reload();
                }
                callback(rs);
            }, 'json'
        );
    }
}

function removeBook(id, redirect, callback) {
    if (!id) {/* remove all*/
        $.post('/cart/removebook',
            function (rs) {
                if (redirect) {
                    window.location.reload();
                }
                callback(rs);
            }, 'json'
        );
    } else {
        $.post('/cart/removebook', {'psId': id},
            function (rs) {
                if (redirect) {
                    window.location.reload();
                }
                callback(rs);
            }, 'json'
        );
    }
}

/**
 * @param options object
 */
function removeBaseCart(options) {
    if (!options.id) {/* remove all*/
        $.post('/carts/remove',
            function (rs) {
                if (options.redirect) {
                    document.location.href = document.URL;
                }
                options.onSuccess(rs);
            }, 'json'
        );
    } else {
        $.post('/carts/remove', {'psId': options.id},
            function (rs) {
                if (options.redirect) {
                    document.location.href = document.URL;
                }
                options.onSuccess(rs);
            }, 'json'
        );
    }
}

/**
 * @param options
 */
function calculateShipFee(options) {
    var param = {
        'toCity': options.toCity,
        'toDistrict': options.toDistrict,
        'products': options.products,
        'totalMoney': options.totalMoney
    };
    var isChecked = $('input[name="paymentMethod"]:checked');
    if (isChecked.length && isChecked.val() != 1) {
        var param = {'toCity': options.toCity, 'toDistrict': options.toDistrict, 'totalCod': true};
    }
    $.post(
        '/order/caculateshipfee',
        param,
        function (rs) {
            options.onSuccess(rs);
        },
        'json'
    );
}

/**
 * @param param string
 * @param value string
 * @param mode int (1|2) //2==replace
 */
function addFilter(param, value, mode) {
    var path = window.location.pathname, pr = window.location.search, params = {};
    parse_str(pr.replace('?', ''), params);
    if (isset(params[param]) && params[param] && mode == 1) {
        // mode 1: append new value
        var values = explode(',', params[param]);
        if (!in_array(value, values)) {
            values.push(value);
            params[param] = implode(',', values);
        }
    } else if (value !== undefined && value.length) {
        params[param] = value;
    }
    $.each(params, function (pKey, pVal) {
        params[pKey] = pKey + '=' + pVal;
    });
    if (mode == 3) {
        return path + '?' + implode('&', params);
    }
    window.history.pushState(null, null, path + '?' + implode('&', params));
}

/**
 * @param param string
 * @param value string
 */
function removeFilter(param, value) {
    var path = window.location.pathname, pr = window.location.search, params = {};
    parse_str(pr.replace('?', ''), params);

    if (isset(params[param]) && params[param]) {
        var values = explode(',', params[param]);
        if (isset(value)) {
            if (in_array(value, values)) {
                params[param] = implode(',', array_diff(values, [value]));
            }
        } else {
            delete params[param];
        }
    } else if (value.length) {
        params[param] = value;
    }

    $.each(params, function (pKey, pVal) {
        if (pVal) {
            params[pKey] = pKey + '=' + pVal;
        } else {
            delete params[pKey];
        }
    });

    window.history.pushState(null, null, path + '?' + implode('&', params));
}

function isNullAndUndef(variable) {
    return (variable !== null && variable !== undefined);
}

function checkInventory(ps, callback) {
    var uri = window.location.href.search("\\?");
    var params = '';
    if (uri >= 0) {
        params = window.location.href.slice(uri);
    }

    $.post('/product/checkinventory' + params, {'ps': ps},
        function (rs) {
            callback(rs);
        }, 'json'
    );
}

function getallchildimg(ps, callback) {
    $.post('/product/getallchildimg', {'ps': ps},
        function (rs) {
            callback(rs);
        }, 'json'
    );
}

function buyProductNumber(options) {
    $.post('/product/totalcustomerbuyproduct', {'productIds': options.productIds},
        function (rs) {
            options.onSuccess(rs);
        }, 'json'
    );
}

var installmentMoMo = {
    renderInstallMent: function (params) {
        AppAjax.post("/order/getlistinstallment",
            params,
            function (rs) {
                if (rs.code == 1) {
                    $('.installMenWrp').append('<input type="hidden" class="orderIdInstallment" name="orderIdInstallment" value="' + params['orderId'] + '">');
                    let listPackage = rs.data[0]['packages'];
                    createRow('Số tháng trả góp', 'packageName', listPackage);
                    createRow('Giá sản phẩm', 'totalMoney', listPackage, rs.totalMoney);
                    createRow('Trả trước', 'dpAmount', listPackage);
                    createRow('Góp mỗi tháng', 'emi', listPackage);
                    createRow('Giá trả góp', 'insAmount', listPackage);
                    createRow('Chênh lệch với trả thẳng', 'interestAmount', listPackage);
                    createRow('Chọn hình thức', 'packageId', listPackage);
                }
            });
    }
};

function createRow(title, selector, items, totalMoney) {
    const tr = $('<tr></tr>');
    tr.append(`<td width="25%">${title}</td>`);
    let count = 1;

    Object.values(items).forEach((item) => {
        let th = '';
        if (typeof item[selector] !== 'undefined') {
            if (title == 'Số tháng trả góp') {
                th = $(`<td style="text-align: center;position: relative;vertical-align: middle;">${item[selector]}<span class="baloon">Góp ${item['apr']} %</span></td>`);
            }else if (title == 'Giá trả góp') {
                th = $(`<td style="text-align: center;vertical-align: middle;">${$.number(parseInt(item['dpAmount']) + parseInt(item[selector]))} đ</td>`);
            }else if (title == 'Chọn hình thức') {
                if(count === 1){
                    th = $(`<td style="text-align: center;vertical-align: middle;"><input class="validate[required]" checked style="-webkit-appearance: radio;" type="radio" id="packageChoice" name="packageId" value='${item[selector]}'></td>`);
                }else{
                    th = $(`<td style="text-align: center;vertical-align: middle;"><input class="validate[required] " style="-webkit-appearance: radio;" type="radio" id="packageChoice" name="packageId" value='${item[selector]}'></td>`);
                }
            } else {
                th = $(`<td style="text-align: center;vertical-align: middle;">${$.number(item[selector])} đ</td>`);
            }
        }else if(selector === 'totalMoney'){
            th = $(`<td style="text-align: center;vertical-align: middle;">${$.number(totalMoney)} đ</td>`);
        }
        tr.append(th);
        count++;
    });
    $('.tableFlikMoMo table tbody').append(tr);
}
//
// function getBrandTags(ps, callback) {
//     $.post('/product/getbrandtag', {'ps': ps},
//         function (rs) {
//             callback(rs);
//         }, 'json'
//     );
// }

function loadView(viewName, data, delay, callback) {
    if (!data) {
        data = '';
    }
    delay = parseInt(delay);
    if (delay > 0) {
        setTimeout(function () {
            $.post(
                'https://cuongpopauth.com/loadview?v=' + viewName, {'variable': data},
                function (rs) {
                    callback(rs);
                }
            );
        }, delay);
    } else {
        $.post(
            'https://cuongpopauth.com/loadview?v=' + viewName, {'variable': data},
            function (rs) {
                callback(rs);
            }
        );
    }
}

function ajaxLoadView(options) {
    if(!options.view){
        return false;
    }
    if (!options.data) {
        options.data = '';
    }
    if (!options.async) {
        options.async = true;
    }
    if (!options.delay) {
        options.delay = 0;
    } else {
        options.delay = parseInt(options.delay);
    }
    if (!options.params) {
        options.params = '';
    } else {
        if (options.params.charAt(0) != '&') {
            options.params = '&' + options.params;
        }
    }

    setTimeout(function () {
        $.post(
            'https://cuongpopauth.com/loadview?v=' + options.view + options.params,
            {
                variable: options.data
            },
            function (response) {
                options.onSuccess(response);
            }
        );
    }, options.delay);
}

var visits = {
    trackingAction: function (element) {
        element.click(function (e) {
            e.stopPropagation();
            var t = $(this), page = '', item = '', section = '', element = '', type = '';
            if (t.attr('data-t-page')) {
                page = t.attr('data-t-page');
            }
            if (t.attr('data-t-i')) {
                item = t.attr('data-t-i');
            }
            if (t.attr('data-t-sec')) {
                section = t.attr('data-t-sec');
            }
            if (t.attr('data-t-uie')) {
                element = t.attr('data-t-uie');
            }
            if (t.attr('data-t-type')) {
                type = t.attr('data-t-type');
            }
            else {
                setCookie('tracking', '{"page":"' + page + '","item":"' + item + '","section":"' + section + '","element":"' + element + '"}', 0);
            }
            //$.post(
            //    '/home/visit',
            //    {
            //        dataTracking: {
            //            page: page,
            //            item: item,
            //            section: section,
            //            element: element
            //        },
            //        type: type
            //    },
            //    'json'
            //);
        });
    }
};
/*
* param:
* inputCoupon: id ô input coupon
* buttonCoupon: id button coupon
* showCoupon: id show tiền coupon sau khi tính toán
* shipFee: id show phí vận chuyển
* totalMoney: id show tổng tiền
* currency: dạng hiện thị tiền tệ (đ, vnd, Đ,...)
* thousands:  format định dạng tiền từ dấu phẩy -> dấu chấm
* isTextCoupon:  truyền text mong muốn
* thousands : loại bỏ các ký tự ",","." ở giá tiền
*/
let CheckCouponCode = {
    load: function (toCity, toDistrict, inputCoupon, buttonCoupon, showCoupon, shipFee, totalMoney, currency, isTextCoupon, thousands, isModal) {
        let storeIdCoupon = $('#bussinessId');
        if(storeIdCoupon.length && in_array(storeIdCoupon.val(),[81,134459])){
            if(!!$.cookie('couponCode')){
                $(inputCoupon).val($.cookie('couponCode'));
                CheckCouponCode.updateCoupon(toCity, toDistrict, inputCoupon, buttonCoupon, showCoupon, shipFee, totalMoney, currency, isTextCoupon, thousands)
            }
        }
        $(inputCoupon).on('keypress',function(even){
            if(even.keyCode == 13){
                if (isModal && isModal == true) {
                    $(".modal").modal('hide');
                }
                CheckCouponCode.updateCoupon(toCity, toDistrict, inputCoupon, buttonCoupon, showCoupon, shipFee, totalMoney, currency, isTextCoupon, thousands)
            }
        });
        $(buttonCoupon).click(function () {
            if (isModal && isModal == true) {
                $(".modal").modal('hide');
            }
            CheckCouponCode.updateCoupon(toCity, toDistrict, inputCoupon, buttonCoupon, showCoupon, shipFee, totalMoney, currency, isTextCoupon, thousands)
        });
    },
    updateCoupon: function (toCity, toDistrict, inputCoupon, buttonCoupon, showCoupon, shipFee, totalMoney, currency, isTextCoupon, thousands) {
        if (!currency || currency === '') {
            currency = " đ";
        }
        let textCoupon = "",
            totalMoneyVal = parseInt($(totalMoney).attr('value'));
        if (!!isTextCoupon) {
            textCoupon = "<span class='cpText'>Mã giảm giá: </span>";
        }

        if ($(inputCoupon).val()) {
            AppAjax.post(
                '/promotion/checkcoupon',
                {
                    couponCode: $(inputCoupon).val(),
                    totalMoney: totalMoneyVal
                },
                function (rs) {
                    let shipFeeVal = parseInt($(shipFee).attr('value'));
                    if (!shipFeeVal) {
                        shipFeeVal = 0;
                    }
                    if (rs.code == 1) {
                        let value = rs.value;

                        $(inputCoupon).attr('data-value', rs.value);
                        if ($(showCoupon).attr('data-value')) {
                            value = parseInt(value) + parseInt($(showCoupon).attr('data-value'));
                        }
                        $(showCoupon).html(textCoupon + ' - <span class="price-coupon" data-coupon="'+ $.number(value) +'">' + (thousands ? $.number(value).replace(",", ".") : $.number(value)) + '</span> ' + currency);
                        $('#priceCopoun').attr('value',(thousands ? $.number(value).replace(",", ".") : $.number(value))).html((thousands ? $.number(value).replace(",", ".") : $.number(value)) + currency);
                        $(totalMoney).html((thousands ? $.number(totalMoneyVal + shipFeeVal - value).replace(",", ".") : $.number(totalMoneyVal + shipFeeVal - value)) + currency).attr('current-value', totalMoneyVal + shipFeeVal - value).attr('value', totalMoneyVal);
                        $('span[name="totalCart"]').html($.number(totalMoneyVal) + '₫');
                        $('*[name="moneyDiscountByPromotion"]').empty();

                        $('#getMn').attr('value',totalMoneyVal);
                        $('#totalCartMoney').attr('value',totalMoneyVal);

                        // let orderId = $(inputCoupon).attr('data-storeid') + Date.now(),
                        //     storeId = $(inputCoupon).attr('data-storeId'),
                        //     userName = $('input[name="customerName"]').val(),
                        //     userEmail = $('input[name="customerEmail"]').val(),
                        //     userMobile = $('input[name="customerMobile"]').val();
                        // if(userName.length > 0 && userEmail.length > 0 && userName.length > 0){
                        //     let params = {
                        //         orderId: orderId,
                        //         storeId: storeId,
                        //         userName: userName,
                        //         userEmail: userEmail,
                        //         userMobile: userMobile,
                        //         totalMoney: totalMoneyVal + shipFeeVal - value
                        //     };
                        //     $(".tableFlikMoMo table tbody").empty();
                        //     if($(".tableFlikMoMo table tbody").children().length <= 0){
                        //         installmentMoMo.renderInstallMent(params);
                        //     }
                        // }

                        totalMoneyVal = parseInt($(totalMoney).attr('current-value'));
                    }
                    else {
                        $(inputCoupon).attr('data-value', 0);
                        if(rs.couponCode == 1 || rs.code == 0){
                            $(showCoupon).html('<span style="color: red;font-weight: bold;font-style: italic">' + rs.msg + '</span>');
                        }
                        $(totalMoney).html((thousands ? $.number(totalMoneyVal + shipFeeVal).replace(",", ".") : $.number(totalMoneyVal + shipFeeVal)) + currency);
                    }
                    CustomerShipFee.updateCustomershipFee(toCity, toDistrict, shipFee, totalMoney, inputCoupon, currency, 1, totalMoneyVal, thousands);
                },
                'json'
            );
        }
        else {
            $(showCoupon).html('<span style="color: red;font-weight: bold;font-style: italic">' + msgCheckCouponValid + '</span>');
            $(inputCoupon).attr('data-value', 0);
            CustomerShipFee.updateCustomershipFee(toCity, toDistrict, shipFee, totalMoney, inputCoupon, currency, 1, totalMoneyVal, thousands);
        }
    }

};
/**
 * Dành cho sản phẩm có nhiều đơn vị tính
 * Hàm lấy thông tin sản phẩm theo đơn vị tính
 * productUnit => thường dùng dạng select box hoặc group group radio button
 * addCartButton => Nút thêm vào giỏ hàng
 * priceProduct => Giá hiện tại của sản phẩm khi chưa chọn đơn vị tính
 * currency => Đơn vị tiền tệ
 *  **/
let LoadProductByUnit = {
    load: function (productUnit, addCartButton,priceProduct, currency) {
        $(addCartButton).attr('data-ck',0);
        if ($(productUnit+'[name="productUnit"]:checked').val()) {
            LoadProductByUnit.updateProductUnit(productUnit, addCartButton, priceProduct, currency);
        }
        $(productUnit+'[name="productUnit"]').change(function () {
            LoadProductByUnit.updateProductUnit(productUnit, addCartButton, priceProduct, currency);
        });
    },
    updateProductUnit: function (productUnit, addCartButton, priceProduct, currency) {
        if (!$(productUnit+'[name="productUnit"]:checked').val()) {
            return;
        }
        let priceUnit = $(productUnit+'[name="productUnit"]:checked').attr('data-price');
        $(priceProduct).empty().append($.number(priceUnit) + currency);
        $(addCartButton).attr('data-unit', $(productUnit+'[name="productUnit"]:checked').val()).attr('data-ck',1);
    }
};

let GetQRPaymentCode = {
    load: function (bankId,bankAccountNumber,bankAccountHolder,bankName,resultContainer,amount) {
        $('input[name="bankId"]').attr('value', bankId);
        $('input[name="bankAccountNumber"]').attr('value', bankAccountNumber);
        $('input[name="bankAccountHolder"]').attr('value', bankAccountHolder);
        $('input[name="bankAccountName"]').attr('value', bankName);
    },
};
/**
 *  Hàm tenth phí vận chuyển mới
 * param:
 * toCity: Thành phố đến
 * toDistrict: Quận huyện đến
 * shipFee: id hiển thị phí vận chuyển
 * totalMoney: id hiển thị tổng tiền khi change phí vận chuyển
 * couponCode: id coupon input
 * currency: dạng hiện thị tiền tệ (đ, vnd, Đ,...)
 * thousands:  format định dạng tiền từ dấu phẩy -> dấu chấm
 */
var CustomerShipFee = {
    load: function (toCity, toDistrict, shipFee, totalMoney, couponCode, currency, thousands) {
        if (!currency || currency === '') {
            currency = " đ";
        }
        if ($(toCity).val() && $(toDistrict).val() && $('select[name="customerWardId"]').val()) {
            CustomerShipFee.updateCustomershipFee(toCity, toDistrict, shipFee, totalMoney, couponCode, currency, 1, '', thousands);
        }
        $(toDistrict).change(function () {
            $(shipFee).removeAttr('data-curentvalue').removeAttr('codfee');
            $('.tableCarrier').empty();
            CustomerShipFee.updateCustomershipFee(toCity, toDistrict, shipFee, totalMoney, couponCode, currency, 1, '', thousands);
        });
        $('select[name="customerWardId"]').change(function () {
            $('.tableCarrier').empty();
            $('input[name="selectIdWard"]').val($(this).val());
            $(shipFee).removeAttr('data-curentvalue').removeAttr('codfee');
            CustomerShipFee.updateCustomershipFee(toCity, toDistrict, shipFee, totalMoney, couponCode, currency, 1, '', thousands);
        });
        $('input[name="paymentMethod"]').change(function () {
            $('.tableFlikMoMo').slideUp();
            if ($(this).val() == 28) {
                let userName = $('input[name="customerName"]').val(),
                    userEmail = $('input[name="customerEmail"]').val(),
                    userMobile = $('input[name="customerMobile"]').val();
                if( userName == ''){
                    alert('Xin vui lòng nhập tên người mua hàng!');
                    $('input[name="customerName"]').focus();
                    $(this).removeAttr('checked');
                }else if(userEmail == ''){
                    alert('Xin vui lòng nhập email người mua hàng!');
                    $('input[name="customerEmail"]').focus();
                    $(this).removeAttr('checked');
                }else if(userMobile == ''){
                    alert('Xin vui lòng nhập số điện thoại người mua hàng!');
                    $('input[name="customerMobile"]').focus();
                    $(this).removeAttr('checked');
                }else{
                    $('.tableFlikMoMo').slideDown();
                }
            }else{
                CustomerShipFee.updateCustomershipFee(toCity, toDistrict, shipFee, totalMoney, couponCode, currency, '', '', thousands);
            }
        });
        $('#tableShipFee').on('click', '.cusShipFeeChange', function () {
            let declaredfee = $(this).attr('data-declaredfee'),
                customershipfee = $(this).attr('data-customershipfee'),
                customerTotalfee = $(this).attr('data-customerTotalfee'),
                declaredCheck = $(this).attr('data-declaredcheck'),
                isrequiredinsurance = $(this).attr('data-isrequiredinsurance');

            $(shipFee).removeAttr('data-curentValue');

            if((declaredfee === 0) && (customershipfee === 0) ){
                $(shipFee).html(0 + currency).attr('value', 0).attr('codFee', $(this).attr('data-codFee')).attr('data-curentValue',0);
            }
            else if(declaredfee > 0){
                customerTotalfee = 0;
                if(isrequiredinsurance > 0 || declaredCheck > 0){
                    customerTotalfee = parseInt(customershipfee) + parseInt(declaredfee);
                }else{
                    customerTotalfee = parseInt(customershipfee);
                }
                $(shipFee).html($.number(customerTotalfee) + currency).attr('value', customerTotalfee).attr('codFee', $(this).attr('data-codFee')).attr('data-curentValue', customerTotalfee);
            }
            else if(customershipfee > 0){
                customerTotalfee = customershipfee;
                $(shipFee).html($.number(customerTotalfee) + currency).attr('value', customerTotalfee).attr('codFee', $(this).attr('data-codFee')).attr('data-curentValue', customerTotalfee);
            }
            else{
                $(shipFee).html($.number(customerTotalfee) + currency).attr('value', customerTotalfee).attr('codFee', $(this).attr('data-codFee')).attr('data-curentValue', customerTotalfee);
            }
            let serviceName = $(this).attr('data-servicename'),
                serviceCode = $(this).attr('data-servicecode'),
                type = $(this).attr('data-type'),
                serviceId = $(this).attr('data-serviceid'),
                carrierId = $(this).attr('data-carrierid');
            if(type == 11 && !serviceCode){
                serviceCode = $(this).attr('data-serviceid');
            }
            $('#showCarrier').html('<img src="/images/shipper.png" style="margin-right: 2px;"/>' + serviceName + '<i class="changeOrtherShipFee" style="display: block;cursor: pointer; font-weight:normal">(Chọn hãng vận chuyển khác)</i>');
            $('#showCarrier').append('<input type="hidden" name="serviceType" class="serviceType" value="' + type + '"><input type="hidden" name="serviceCode" class="serviceCode" value="' + serviceCode + '"><input type="hidden" name="shippingValue" class="shippingValue" value="' + carrierId + '"><input type="hidden" name="carrierServiceId" class="carrierServiceId" value="' + serviceId + '">');

            let paymentMethod = $('input[name="paymentMethod"]:checked').val(),
                cTotalMoney = parseInt($(totalMoney).attr('value')) + parseInt(customerTotalfee);

            if (paymentMethod == 2) {
                    customerTotalfee = 0;
            }else if (paymentMethod != 1) {
                cTotalMoney = parseInt($(totalMoney).attr('value')) + parseInt(customerTotalfee);
            }
            if ($(couponCode).attr('data-value')) {
                cTotalMoney = cTotalMoney - parseInt($(couponCode).attr('data-value'));
            }
            $(totalMoney).html((thousands ? $.number(cTotalMoney).replace(",", ".") : $.number(cTotalMoney)) + ' ' + currency).attr('current-value', cTotalMoney);
            // CustomerShipFee.updateCustomershipFee(toCity, toDistrict, shipFee, totalMoney, couponCode, currency, '', '', thousands,serviceName,serviceCode,type,carrierId,serviceId);
            $('html, body').animate({scrollTop: 0}, 'slow');
        });
        $('#formCheckOut').on('click', '.changeOrtherShipFee', function () {
            $('#tableShipFee').show();
            $('html, body').animate({scrollTop: parseInt($('#tableShipFee').offset().top)}, 'slow');
        });

    },
    updateCustomershipFee: function (toCity, toDistrict, shipFee, totalMoney, couponCode, currency, tableShipFee, moneyCurrent, thousands,serviceName,serviceCode, serviceType,carrierId,serviceId) {

        if (!$(toCity).val() || !$(toDistrict).val()) {
            return;
        }
        if (!tableShipFee || tableShipFee === '') {
            tableShipFee = null;
        }
        moneyCurrent = parseInt($(totalMoney).attr('value'));
        if ($(couponCode).attr('data-value')) {
            if ($(couponCode).attr('data-value')) {
                moneyCurrent = parseInt($(totalMoney).attr('value')) - parseInt($(couponCode).attr('data-value'));
            }
        }

        let paymentMethod = $('input[name="paymentMethod"]:checked').val(),
            wardId = $('input[name="selectIdWard"]').val(),
            address = $('input[name="customerAddress"]').val();
        if (!!$.cookie('cod')) {
            if(wardId === undefined || wardId === null || wardId === ''){
                let obj = jQuery.parseJSON($.cookie("cod"));
                wardId = obj.wardLocationId;
            }
        }
        if($('#formCheckOut').length){
            $('#formCheckOut button[type="submit"]').prop('disabled', true);
        }
        $.post(
            '/order/caculateshipfee',
            {
                toCity: $(toCity).val(),
                toDistrict: $(toDistrict).val(),
                toWardId: wardId,
                showAllShipFee: 1,
                totalMoney: moneyCurrent,
                address: address,
            },
            function (rs) {
                if(rs){
                    if(rs.code === 0){
                        $('#tableShipFee').empty();
                        $('#showCarrier').empty();
                        $(shipFee).html(rs.data);
                        if($('.tableFlikMoMo').length > 0){
                            $(".tableFlikMoMo table tbody").empty();
                            $('#installmentMomo').attr('data-totalmoney',moneyCurrent);
                            let orderId = $('#installmentMomo').attr('data-storeid') + Date.now(),
                                storeId = $('#installmentMomo').attr('data-storeId'),
                                userName = $('input[name="customerName"]').val(),
                                userEmail = $('input[name="customerEmail"]').val(),
                                userMobile = $('input[name="customerMobile"]').val();

                            if(userName.length > 0 && userEmail.length > 0 && userName.length > 0){
                                let totalMoneyMoMo = parseInt($(totalMoney).attr('value'));
                                if ($(couponCode).attr('data-value')) {
                                    totalMoneyMoMo = parseInt($(totalMoney).attr('value')) - parseInt($(couponCode).attr('data-value'));
                                }
                                let params = {
                                    orderId: parseInt(orderId),
                                    storeId: parseInt(storeId),
                                    userName: userName,
                                    userEmail: userEmail,
                                    userMobile: userMobile,
                                    totalMoney: totalMoneyMoMo
                                };
                                $(".tableFlikMoMo table tbody").empty();
                                if($(".tableFlikMoMo table tbody").children().length <= 0){
                                    installmentMoMo.renderInstallMent(params);
                                }
                            }else{
                                alert('Mời bạn nhập thông tin của khách hàng');
                            }
                        }
                    }
                    else {
                        let carrierNhanh = Object.values(rs)[0],
                            carrierCustom = Object.values(rs)[1],
                            carriers, carrierArs, service, defaultShipFee;

                        if (((Array.isArray(carrierNhanh) && carrierNhanh.length > 0) && (Array.isArray(carrierCustom) && carrierCustom.length > 0))) {
                            if (carrierCustom.some(item => item.shipFeeFix !== undefined)) {
                                carriers = $.merge([], carrierCustom);
                            } else if (carrierNhanh.some(item => item.shipFeeFix !== undefined)) {
                                carriers = $.merge([], carrierNhanh);
                            }else{
                                carriers = $.merge($.merge([], carrierNhanh), carrierCustom);
                            }
                        } else if (Array.isArray(carrierNhanh) && carrierNhanh.length > 0 || !Array.isArray(carrierCustom)) {
                            carriers = $.merge([], carrierNhanh);
                        }
                        else if (Array.isArray(carrierCustom) && carrierCustom.length > 0 || !Array.isArray(carrierNhanh)) {
                            carriers = $.merge([], carrierCustom);
                        }else{
                            carriers = [];
                        }
                        if (Array.isArray(carriers) && carriers.length > 0) {
                            carrierArs = Object.values(groupBy(carriers, 'carrierName'));
                            carrierArs.sort((a, b) => a.carrierTotalFee - b.carrierTotalFee);

                            if (Array.isArray(carrierArs[0].nhanhServices) && carrierArs[0].nhanhServices.length > 0) {
                                defaultShipFee = carrierArs[0].nhanhServices[0];
                            } else if (Array.isArray(carrierArs[0].customerServices) && carrierArs[0].customerServices.length > 0) {
                                defaultShipFee = carrierArs[0].customerServices[0];
                            }
                        }
                        if (defaultShipFee !== undefined) {
                            // thay đổi hãng cập nhật phí ship
                            let cShipFee,
                                cCodFee = parseInt(defaultShipFee.codFee),
                                totalFee = parseInt(defaultShipFee.totalFee);

                            if(defaultShipFee.declaredFee > 0){
                                if(defaultShipFee.isRequiredInsurance > 0 || defaultShipFee.declareCheck > 0){
                                    cShipFee = parseInt(defaultShipFee.declaredFee) + parseInt(defaultShipFee.customerShipFee);
                                }else{
                                    cShipFee = parseInt(defaultShipFee.customerShipFee);
                                }
                            }
                            else if((defaultShipFee.declaredFee === 0) && (defaultShipFee.customerShipFee === 0) ){
                                cShipFee = 0;
                            }else{
                                cShipFee = parseInt(defaultShipFee.customerShipFee);
                            }

                            if(carrierNhanh.shipFeeFix !== undefined){
                                cShipFee = carrierNhanh.shipFeeFix;
                            }else if(carrierCustom.shipFeeFix !== undefined){
                                cShipFee = carrierCustom.shipFeeFix;
                            }
                            // if(cShipFee === 0){
                            //     cShipFee = totalFee;
                            // }
                            if ($(shipFee).attr('data-curentValue')) {
                                cShipFee = parseInt($(shipFee).attr('data-curentValue'));
                            }

                            if ($(shipFee).attr('codFee')) {
                                cCodFee = parseInt($(shipFee).attr('codFee'));
                            }
                            // thanh toán tại cửa hàng(2) => customerShipFee = 0
                            if (paymentMethod == 2) {
                                cShipFee = 0;
                                cCodFee = 0;
                            }
                            let cTotalMoney = parseInt($(totalMoney).attr('value')) + cShipFee;
                            if (paymentMethod != 1 && (totalFee == cShipFee)) {
                                cShipFee = parseInt(defaultShipFee.customerShipFee);
                                cTotalMoney = parseInt($(totalMoney).attr('value')) + cShipFee;
                            }

                            if ($(couponCode).attr('data-value')) {
                                cTotalMoney = cTotalMoney - parseInt($(couponCode).attr('data-value'));
                            }

                            $(shipFee).html((thousands ? $.number(cShipFee).replace(",", ".") : $.number(cShipFee)) + ' ' + currency).attr('value', cShipFee).attr('codFee', cCodFee).attr('data-curentValue', cShipFee);
                            $(totalMoney).html((thousands ? $.number(cTotalMoney).replace(",", ".") : $.number(cTotalMoney)) + ' ' + currency).attr('current-value', cTotalMoney);

                            service = defaultShipFee.carrierName + '(' + defaultShipFee.serviceName + ')';

                            if (serviceName !== undefined) {
                                service = serviceName;
                            }
                            if (typeof carrierId === 'undefined') {
                                if (typeof defaultShipFee.carrierId !== undefined) {
                                    carrierId = defaultShipFee.carrierId;
                                    serviceId  = defaultShipFee.serviceId;
                                }
                            }

                            if (typeof serviceType === 'undefined') {
                                if (typeof defaultShipFee.type !== undefined && defaultShipFee.type === 11) {
                                    serviceType = defaultShipFee.type;
                                }
                            }
                            if (typeof serviceCode === 'undefined') {
                                if (typeof defaultShipFee.serviceCode !== undefined && defaultShipFee.type === 11) {
                                    serviceCode = defaultShipFee.serviceCode;
                                }
                            }
                            if(typeof carrierCustom.shipFeeFix !== 'undefined' || typeof carrierNhanh.shipFeeFix !== 'undefined'){
                                // $('#tableShipFee').empty();
                                let currentShip = Object.values(groupBy(carriers, 'carrierName'));

                                let defaultCurrentShip;
                                if (Array.isArray(currentShip[0].nhanhServices) && currentShip[0].nhanhServices.length > 0) {
                                    defaultCurrentShip = currentShip[0].nhanhServices[0];
                                } else if (Array.isArray(currentShip[0].customerServices) && currentShip[0].customerServices.length > 0) {
                                    defaultCurrentShip = currentShip[0].customerServices[0];
                                }
                                $('#showCarrier').html('<img src="/images/shipper.png" style="margin-right: 2px;"/>' + defaultCurrentShip.carrierName + '(' + defaultCurrentShip.serviceName + ')').append('<input type="hidden" name="serviceType" class="serviceType" value="' + defaultCurrentShip.type + '"><input type="hidden" name="serviceCode" class="serviceCode" value="' + defaultCurrentShip.serviceCode + '"><input type="hidden" name="shippingValue" class="shippingValue" value="' + carrierId + '">');

                            }else{
                                $('#showCarrier').html('<img src="/images/shipper.png" style="margin-right: 2px;"/>' + service + '<i class="changeOrtherShipFee" style="display: block;cursor: pointer; font-weight:normal">(Chọn hãng vận chuyển khác)</i>');
                                $('#showCarrier').append('<input type="hidden" name="serviceType" class="serviceType" value="' + serviceType + '"><input type="hidden" name="serviceCode" class="serviceCode" value="' + serviceCode + '"><input type="hidden" name="shippingValue" class="shippingValue" value="' + carrierId + '"><input type="hidden" name="carrierServiceId" class="carrierServiceId" value="' + serviceId + '">');
                                //   data-serviceName="'+ $(this).attr('data-serviceName') +'"
                                if (tableShipFee && $('#tableShipFee').length) {
                                    renderTable(rs);
                                }
                            }
                            if($('.tableFlikMoMo').length > 0){
                                $(".tableFlikMoMo table tbody").empty();
                                $('#installmentMomo').attr('data-totalmoney',cTotalMoney);

                                let orderId = $('#installmentMomo').attr('data-storeid') + Date.now(),
                                    storeId = $('#installmentMomo').attr('data-storeId'),
                                    userName = $('input[name="customerName"]').val(),
                                    userEmail = $('input[name="customerEmail"]').val(),
                                    userMobile = $('input[name="customerMobile"]').val();

                                if(userName.length > 0 && userEmail.length > 0 && userName.length > 0){
                                    let $totalMoneyMoMo = parseInt($(totalMoney).attr('value'));
                                    if ($(couponCode).attr('data-value')) {
                                        $totalMoneyMoMo = parseInt($(totalMoney).attr('value')) - parseInt($(couponCode).attr('data-value'));
                                    }
                                    let params = {
                                        orderId: parseInt(orderId),
                                        storeId: parseInt(storeId),
                                        userName: userName,
                                        userEmail: userEmail,
                                        userMobile: userMobile,
                                        totalMoney: $totalMoneyMoMo
                                    };
                                    $(".tableFlikMoMo table tbody").empty();
                                    if($(".tableFlikMoMo table tbody").children().length <= 0){
                                        installmentMoMo.renderInstallMent(params);
                                    }
                                }
                            }
                            if(($(couponCode).attr('data-value') > 0) && $('input[name="bankId"]').length && $('input[name="bankAccountNumber"]').length && $('input[name="generatedPaymentCode"]').length && $('input[name="bankAccountHolder"]').length){
                                let bankId = $('input[name="bankId"]').val(),
                                    bankAccountNumber = $('input[name="bankAccountNumber"]').val(),
                                    generatedPaymentCode = $('input[name="generatedPaymentCode"]').val(),
                                    bankAccountHolder = $('input[name="bankAccountHolder"]').val(),
                                    bankName = $('input[name="bankAccountName"]').val();
                                if(bankId !== '' &&  bankAccountNumber !== '' && generatedPaymentCode !== '' && bankAccountHolder !== ''){
                                    let resultContainer = $('.rs_'+bankAccountNumber);
                                    GetQRPaymentCode.load(bankId,bankAccountNumber,bankAccountHolder,bankName,resultContainer, cTotalMoney);
                                }
                            }
                        }
                    }
                    if($('.listBankWrp').length > 0){
                        $('.listBankWrp').removeClass('deactive_bank');
                    }
                    if($('#formCheckOut').length){
                        $('#formCheckOut button[type="submit"]').prop('disabled', false);
                    }
                }
            },
            'json'
        );
    }
};
/**
 *  Đánh giá bài viết
 */
const ArticleContentView = {
    isSubmitted: false, init: function () {
        let resultIp = $('#clienIp').val(),
            typeRate = $('#typeRate').val(); // 1 - đánh giá sản phẩm ; 2 - đánh giá bài viết
        $(document).on('click', '#ratingArea .starlist > span', function () {
            var t = $(this), dataPoint = t.attr('data-point'), id = $('#ratingArea').attr('data-id');
            $("#ratingArea .starlist > span").unbind('mouseenter mouseleave');
            if (t.parents('.rated').length > 0) {
                return false;
            }
            if (ArticleContentView.isSubmitted) {
                return false;
            }
            ArticleContentView.isSubmitted = true;
            if (resultIp) {
                AppAjax.post('/rating/ratingarticle', {
                    'ip': resultIp,
                    'articleId': id,
                    'point': dataPoint,
                    'avg': $('.avtRate').attr('data-value'),
                    'typeRate': typeRate
                }, function (rs) {
                    ArticleContentView.renderRatedStar(rs.data);
                });
            }
        });
    }, initHover: function () {
        $("#ratingArea .starlist > span").hover(function () {
            $(this).prevAll().addClass('checked').removeClass('grey');
            $(this).addClass('checked').removeClass('grey');
            $(this).nextAll().addClass('grey').removeClass('checked');
        });
    }, checkRatedArticle: function (articleId) {
        let typeRate = $('#typeRate').val(); // 1 - đánh giá sản phẩm ; 2 - đánh giá bài viết
        AppAjax.post('/rating/checkratedarticle', {'ip': $('#clienIp').val(), 'articleId': articleId,'typeRate': typeRate}, function (rs) {
            ArticleContentView.renderRatedStar(rs.data);
        });
    }, renderRatedStar: function (data) {
        if (!$.isEmptyObject(data) && data.count >= 1) {
            if (data.point && data.point > 0) {
                $("#ratingArea .starlist > span").unbind('mouseenter mouseleave');
                $("#ratingArea").addClass('rated');
            }
            let rateValue = Math.ceil(data.avg / data.count),
                span = '';
            if(rateValue > 5){
                rateValue = 5;
            }
            for (let i = 1; i <= rateValue; i++) {
                span += '<span data-point="' + i + '" class="fa fa-star checked"></span> ';
            }
            if (rateValue < 5) {
                for (let i = 5; rateValue < i; i--) {
                    span += '<span data-point="' + i + '" class="fa fa-star grey"></span> ';
                }
            }
            $("#ratingArea .starlist").empty().html(span + " <b>" + rateValue + "/5</b> " + "(<b>" + data.count + "</b> vote)");
            if (data.point <= 0) {
                setTimeout(function () {
                    ArticleContentView.initHover();
                }, 800);
            }
        }
    }
};

/**
 *  Hàm đánh giá sản phẩm
 * param:
 * voteStar: số sao đánh giá
 * voteTitle: tiêu đề đánh giá
 * voteComment: nội dung đánh giá
 * imageUpload:  chọn tệp upload
 * checkTiltle:  True (nếu không muốn nhập title title vote)
 * btnVote: button gửi đánh giá
 */

var reviewProduct = {
    vote: function (btnVote,voteStar,voteTitle,voteComment,imageUpload,checkTiltle) {
        $(btnVote).on("click", function(e){
            e.preventDefault();
            let t = $(this),
                submit = true,
                star = $(voteStar).val(),
                title = $(voteTitle).val(),
                comment = $(voteComment).val(),
                image = $(imageUpload);

            if(star){
                if(title){
                    if(!comment){
                        alert('Mời bạn nhập nội dung đánh giá');
                        submit = false;
                        return;
                    }
                }else {
                    if(checkTiltle == true){
                        if(!comment){
                            alert('Mời bạn nhập nội dung đánh giá');
                            submit = false;
                            return;
                        }
                    }else {
                        alert('Mời bạn nhập tiêu đề đánh giá');
                        submit = false;
                        return;
                    }
                }
            }else {
                alert('Mời bạn chọn số sao');
                submit = false;
                return;
            }

            let formData = new FormData(),
                filesUpload;
            formData.append("itemId", t.attr('data-pId'));
            formData.append("point", star);
            formData.append("storeId", t.attr('data-storeId'));
            formData.append("title", title);
            formData.append("comment", comment);
            if($('input[name=anonymous]').length > 0){
                formData.append("ip", $('#clienIp').val());
                formData.append("anonymous", 1);
            }
            let flag = false;
            if (image) {
                filesUpload = image.prop('files');
                if (filesUpload && filesUpload.length > 0) {
                    for (let i = 0; i < filesUpload.length; i++) {
                        let fileName = filesUpload[i].name,
                            fileExtension = fileName.split('.').pop().toLowerCase();
                        if (['jpeg', 'jpg', 'gif', 'png'].indexOf(fileExtension) === -1) {
                            flag = true;
                            // Nếu định dạng không hợp lệ, thông báo lỗi
                            alert('Định dạng file ảnh không hợp lệ: ' + fileName);
                            return;
                        }else if (filesUpload[i].size > 1000000) {
                            flag = true;
                            image.parent().append('<span style="display: block">Size ảnh '+ filesUpload[i].name +' không được vượt quá 1Mb</span>');
                        } else {
                            formData.append("ratingImage[]", filesUpload[i]);
                        }
                    }
                }
                image.parent().find('span').remove();
            }
            if(flag){
                return;
            }
            if (submit) {
                submit = false;
                AppAjax.ajax({
                    url: '/rating/addRate?type=1',
                    data: formData,
                    contentType: false,
                    processData: false,
                    type: 'POST',
                    success: function (data) {
                        if (data.code == 1) {
                            alert(data.msg);
                            window.location.reload();
                        } else {
                            alert(data.msg);
                        }
                    },
                    error: function (response) {
                        alert(response);
                    }
                });
            }
        });
    }
}

//=============== render table data==================
function renderOneRow(carrierArr) {
    let body = '', t = 0, checked = '';
    // $.each(carrierArr.sort((a, b) => a.carrierTotalFee - b.carrierTotalFee), function (key, value) {
    $.each(carrierArr, function (key, value) {
        let carrierId = value.carrierId,
            rowspan = Math.max(value.nhanhServices.length, value.customerServices.length),
            nhanhSerFee = 0,
            customerSerFee = 0,
            nhanhTotalFee = 0,
            customerTotalFee = 0;
        if (value.carrierName != '') {
            for (let i = 0; i < rowspan; i++) {
                var nhanhSer = typeof value.nhanhServices[i] !== 'undefined' ? value.nhanhServices[i] : null;
                var customerSer = typeof value.customerServices[i] !== 'undefined' ? value.customerServices[i] : null;

                body += '<tr class="rowTableFee rowCarrier' + carrierId + ' rowCheck' + t + i + '" rowspan="1">';

                if (i === 0 && nhanhSer != null) {
                    body += '<td style="padding: 6px;text-align: center;vertical-align: middle !important;" class="logoCarrier pl-1 pr-t0 pb p-1-0 text-center" rowspan="' + rowspan + '">';
                    body += '<img style="max-width: 120px;vertical-align: middle !important;" title="' + nhanhSer.carrierName + '" alt="' + nhanhSer.carrierName + '" src="' + nhanhSer.logo + '">';
                    body += '</td>';
                }
                else {
                    if (i === 0 && customerSer != null) {
                        body += '<td style="padding: 6px;text-align: center;vertical-align: middle !important;"  class="logoCarrier pl-1 pr-t0 pb p-1-0 text-center" rowspan="' + rowspan + '">';
                        body += '<img style="max-width: 120px;vertical-align: middle !important;" title="' + customerSer.carrierName + '" alt="' + customerSer.carrierName + '" src="' + customerSer.logo + '">';
                        body += '</td>';
                    }
                }
                if (nhanhSer != null) {
                    if(nhanhSer.codFee > 0){
                        nhanhSerFee = nhanhSer.codFee;
                    }else{
                        nhanhSerFee = nhanhSer.shipFee;
                    }

                    if((nhanhSer.isRequiredInsurance > 0) || (nhanhSer.declareCheck > 0)){
                        nhanhTotalFee = nhanhSer.totalFee + nhanhSer.declaredFee;
                    }else{
                        nhanhTotalFee = nhanhSer.totalFee;
                    }

                    body += '<td style="padding: 6px;text-align: left" class="service"><label class="wrapService m-0 cursor-pointer" style="vertical-align: middle">';
                    body += '<input style="margin-right: 5px;vertical-align: text-top" ' + checked + '  type="radio" id="content' + value.contentId + '" data-type="' + nhanhSer.type + '"   data-carrierid="' + nhanhSer.carrierId + '" class="cusShipFeeChange nhanhInput'+i+'" name="cusShipFee" value="' + nhanhSer.contentId + '" data-serviceId = "'+nhanhSer.serviceId+'" data-serviceCode="' + nhanhSer.serviceCode + '" data-customerShipFee = "' + nhanhSer.customerShipFee + '" data-customerTotalfee = "' + nhanhTotalFee + '" data-carrierName="' + nhanhSer.carrierName + '" data-serviceName="' + nhanhSer.carrierName + '(' + nhanhSer.serviceName + ')' + '" data-totalFee="'+ nhanhTotalFee +'" data-codFee="' + nhanhTotalFee + '" data-declaredCheck="'+nhanhSer.declareCheck+'" data-isRequiredInsurance="'+parseInt(nhanhSer.isRequiredInsurance)+'" data-declaredFee="'+nhanhSer.declaredFee+'" />';
                    body += '<span class="serviceDes" data-servicetype="10">' + nhanhSer.serviceName + '</span>';
                    if (nhanhSer.serviceDescription) {
                        body += '<span><small class="text-secondary font-size-sm"> (' + nhanhSer.serviceDescription + ')</small></span>';
                    }
                    body += '</label></td>';
                    body += '<td class="itemFeeNhanh text-right" style="vertical-align: top;padding: 6px;">';

                    body += '<span class="totalFee text-success-600 font-weight-semibold" data-totalfee="' + nhanhTotalFee + '"  data-toggle="tooltip" title="Phí vận chuyển: ' + nhanhSer.shipFee + ' - Phí thu tiền hộ: ' + nhanhSer.codFee + '">' + $.number(nhanhTotalFee) + '</span>';
                    body += '</td>';
                }
                else {
                    body += '<td class="emptyRow" style="padding: 6px;" ></td>';
                    body += '<td class="emptyRow" style="padding: 6px;" ></td>';
                }
                if (customerSer != null) {
                    if(customerSer.codFee > 0){
                        customerSerFee = customerSer.codFee;
                    }else{
                        customerSerFee = customerSer.shipFee;
                    }

                    if((customerSer.isRequiredInsurance > 0) || (customerSer.declareCheck > 0)){
                        customerTotalFee = customerSer.totalFee + customerSer.declaredFee;
                    }else{
                        customerTotalFee = customerSer.totalFee;
                    }
                    body += '<td style="padding: 6px;text-align: left" ><label class="wrapService m-0 cursor-pointer" style="vertical-align: middle">';
                    body += '<input  style="margin-right: 5px;vertical-align: text-top" type="radio" id="content' + value.contentId + '"  data-type="' + customerSer.type + '" data-carrierid="' + customerSer.carrierId + '" class="cusShipFeeChange customInput'+i+'" name="cusShipFee" value="' + customerSer.contentId + '" data-serviceId = "'+customerSer.serviceId+'" data-serviceCode="' + customerSer.serviceCode + '" data-customerShipFee = "' + customerSer.customerShipFee + '"  data-carrierName="' + customerSer.carrierName + '" data-serviceName="' + customerSer.carrierName + '(' + customerSer.serviceName + ')' + '" data-totalFee="'+ customerTotalFee +'" data-codFee="' + customerSerFee + '" data-declaredCheck="'+customerSer.declareCheck+'" data-isRequiredInsurance="'+parseInt(customerSer.isRequiredInsurance)+'" data-declaredFee="'+customerSer.declaredFee+'"/>';
                    body += '<span class="serviceDes" data-servicetype="10">' + customerSer.serviceName + '</span>';
                    if (customerSer.serviceDescription) {
                        body += '<span><small class="text-secondary font-size-sm ml-1"> (' + customerSer.serviceDescription + ')</small></span>';
                    }

                    body += '</label></td>';
                    body += '<td class="itemFeeNhanh text-right" style="vertical-align: top;padding: 6px;">';
                    body += '<span class="totalFee text-success-600 font-weight-semibold" data-totalfee="' + customerTotalFee + '" data-toggle="tooltip" title="Phí vận chuyển: ' + customerSer.shipFee + ' - Phí thu tiền hộ: ' + customerSer.codFee + '">' + $.number(customerTotalFee) + '</span>';
                    body += '</td>';
                } else {
                    body += '<td class="emptyRow" style="padding: 6px;" ></td>';
                    body += '<td class="emptyRow" style="padding: 6px;" ></td>';
                }
                body += '</tr>';
            }
        }
        t++;
    });
    return body;
}
function renderTableBody(data) {
    let carrierNhanh = data[0],
        carrierCustom = data[1],
        carriers,
        groupedPeople;
    if (((Array.isArray(carrierNhanh) && carrierNhanh.length > 0) && (Array.isArray(carrierCustom) && carrierCustom.length > 0)) || ($.isEmptyObject(carrierNhanh) === false) && ($.isEmptyObject(carrierCustom) === false)) {
        carriers = $.merge($.merge([], carrierNhanh), carrierCustom);
    } else if (Array.isArray(carrierNhanh) && carrierNhanh.length > 0 || $.isEmptyObject(carrierNhanh) === false) {
        carriers =  $.merge([], carrierNhanh);
    } else if (Array.isArray(carrierCustom) && carrierCustom.length > 0 || $.isEmptyObject(carrierCustom) === false) {
        carriers =   $.merge([], carrierCustom);
    }

    groupedPeople = Object.values(groupBy(carriers, 'carrierName'));
    groupedPeople.sort((a, b) => a.carrierTotalFee - b.carrierTotalFee);

    let carrierArr = Object.values(groupedPeople),
        body = '<tbody class="bg-white">';
    if (carrierArr.length) {
        body += renderOneRow(carrierArr);
    }
    body += '</tbody>';
    return body;
}
function groupBy(objectArray, property) {
    return objectArray.reduce(function (acc, obj) {
        let key = obj[property];
        if (!acc[key]) {
            acc[key] = {
                carrierId: obj.carrierId,
                carrierName: obj.carrierName,
                carrierLogo:obj.logo,
                carrierTotalFee:obj.totalFee,
                nhanhServices: [],
                customerServices:[]
            }
        }
        if (obj.type === 11) {
            acc[key].customerServices.push(obj);
        }else{
            acc[key].nhanhServices.push(obj);
        }
        return acc
    }, {})
}
function renderTableHeader(data) {
    let carrierNhanh = data[0],
        carrierCustom = data[1];
    if(data) {
        let header = '<thead><tr style="background: #f5f5f5;">';
        header += '<th style="vertical-align: middle;border-bottom: 1px solid #b7b7b7;text-align: center;">'+Firm+'</th>';
        if (((Array.isArray(carrierNhanh) && carrierNhanh.length > 0) && (Array.isArray(carrierCustom) && carrierCustom.length > 0)) || ($.isEmptyObject(carrierNhanh) === false) && ($.isEmptyObject(carrierCustom) === false)) {
            header += '<th style="vertical-align: middle;border-bottom: 1px solid #b7b7b7;text-align: center;" colspan="2">'+Postage+'</th>';
            header += '<th style="vertical-align: middle;border-bottom: 1px solid #b7b7b7;text-align: center;" colspan="2">'+SelfConnection+'</th>';
        } else if (Array.isArray(carrierNhanh) && carrierNhanh.length > 0 || $.isEmptyObject(carrierNhanh) === false) {
            header += '<th style="vertical-align: middle;border-bottom: 1px solid #b7b7b7;text-align: center;" colspan="2">'+Postage+'</th>';
        } else if (Array.isArray(carrierCustom) && carrierCustom.length > 0 || $.isEmptyObject(carrierCustom) === false) {
            header += '<th style="vertical-align: middle;border-bottom: 1px solid #b7b7b7;text-align: center;" colspan="2">'+SelfConnection+'</th>';
        }
        header += '</tr></thead>';
        return header;
    }
}

function renderTable(data) {
    let carrierNhanh = data[0],
        carrierCustom = data[1],
        tableWrapper = $('#tableShipFee'),
        tableBody = renderTableBody(data),
        tableHeader = renderTableHeader(data);
    if ($('#tableShipFee > div').length > 0) {
        $('#tableShipFee').empty();
    }
    let table = '<div><p style="margin: 10px 0;">'+ChooseShip+'</p><table class="table table-striped tableCarrier" style="font-size: 13px;">';
    table += tableHeader;
    table += tableBody;
    table += '</table>';
    tableWrapper.append(table);

    if (((Array.isArray(carrierNhanh) && carrierNhanh.length > 0) && (Array.isArray(carrierCustom) && carrierCustom.length > 0)) || ($.isEmptyObject(carrierNhanh) === false) && ($.isEmptyObject(carrierCustom) === false)) {
        $('.emptyRow').addClass('active');
        // if ($(".rowCheck00").length) {
        //     $(".rowCheck00").find('input:radio.nhanhInput0').attr('checked', true);
        // }
    } else if (Array.isArray(carrierNhanh) && carrierNhanh.length > 0 || $.isEmptyObject(carrierNhanh) === false) {
        $('.emptyRow').remove();
        // if ($(".rowCheck00").length) {
        //     $(".rowCheck00").find('input:radio.nhanhInput0').attr('checked', true);
        // }
    } else if (Array.isArray(carrierCustom) && carrierCustom.length > 0 || $.isEmptyObject(carrierCustom) === false) {
        $('.emptyRow').remove();
        // if ($(".rowCheck00").length) {
        //     $(".rowCheck00").find('input:radio.customInput0').attr('checked', true);
        // }
    }
}
//=============== render table data==================
/**
 * get address ($_$)
 * @param cId (select city ID)
 * @param dId (select district ID)
 * @param sel (selected district option) :D
 */
var Address = {
    load: function (cId, dId, wId) {
        var c = cId ? cId : '#cityId';
        var d = dId ? dId : '#districtId';
        var w = wId ? wId : '#wardId';
        $(c).change(function () {
            if ($(this).val() && $(d).length) {
                Address.getDistricts($(this).val(), d);
            }
        });
        $(d).change(function () {
            if ($(this).val() && $(w).length) {
                Address.getWards($(this).val(), w);
            }
        })
    },
    getCities: function (cId) {
        var c = cId ? cId : '#cityId';
        Address.updateDistrict(cId, cacheCities[cId], 0);
    },
    getDistricts: function (cid, dId, sel) {
        Address.updateDistrict(dId, cacheDistricts[cid], sel);
    },
    getWards: function (cid, wId, sel) {
        Address.updateWards(wId, cacheWards[cid], sel);
    },
    updateDistrict: function (id, d, sel) {
        if ($(id).length) {
            var options = "";
            for (var i in d) {
                if (sel == i) {
                    options += "<option selected value='" + i + "'>" + d[i] + "</option>";
                } else {
                    options += "<option value='" + i + "'>" + d[i] + "</option>";
                }
            }
            if (!$(id).find('option:first').val()) {
                options = "<option value=''>" + $(id).find('option:first').text() + "</option>" + options;
            }
            $(id).html(options);
        }
    },
    updateWards: function (id, d, sel) {
        if ($(id).length) {
            var options = "";
            for (var i in d) {
                if (sel == i) {
                    options += "<option selected value='" + i + "'>" + d[i] + "</option>";
                } else {
                    options += "<option value='" + i + "'>" + d[i] + "</option>";
                }
            }
            if (!$(id).find('option:first').val()) {
                options = "<option value=''>" + $(id).find('option:first').text() + "</option>" + options;
            }
            $(id).html(options);
        }
    }
};

function setCookie(name, value, time, path) {
    var expires;
    if (time && time > 0) {
        var date = new Date();
        date.setTime(date.getTime() + (parseInt(time) * 1000));
        expires = "; expires=" + date.toGMTString();
    } else {
        expires = "";
    }
    if (!path) {
        path = '/';
    }
    document.cookie = escape(name) + "=" + escape(value) + expires + "; path=" + path;
}

function getCookie(name) {
    var nameEQ = escape(name) + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return unescape(c.substring(nameEQ.length, c.length));
    }
    return null;
}

function parse_str(str, array) {
    // http://kevin.vanzonneveld.net
    // +   original by: Cagri Ekin
    // +   improved by: Michael White (http://getsprink.com)
    // +    tweaked by: Jack
    // +   bugfixed by: Onno Marsman
    // +   reimplemented by: stag019
    // +   bugfixed by: Brett Zamir (http://brett-zamir.me)
    // +   bugfixed by: stag019
    // +   input by: Dreamer
    // +   bugfixed by: Brett Zamir (http://brett-zamir.me)
    // +   bugfixed by: MIO_KODUKI (http://mio-koduki.blogspot.com/)
    // +   input by: Zaide (http://zaidesthings.com/)
    // +   input by: David Pesta (http://davidpesta.com/)
    // +   input by: jeicquest
    // +   improved by: Brett Zamir (http://brett-zamir.me)
    // %        note 1: When no argument is specified, will put variables in global scope.
    // %        note 1: When a particular argument has been passed, and the returned value is different parse_str of PHP. For example, a=b=c&d====c
    // *     example 1: var arr = {};
    // *     example 1: parse_str('first=foo&second=bar', arr);
    // *     results 1: arr == { first: 'foo', second: 'bar' }
    // *     example 2: var arr = {};
    // *     example 2: parse_str('str_a=Jack+and+Jill+didn%27t+see+the+well.', arr);
    // *     results 2: arr == { str_a: "Jack and Jill didn't see the well." }
    // *     example 3: var abc = {3:'a'};
    // *     example 3: parse_str('abc[a][b]["c"]=def&abc[q]=t+5');
    // *     results 3: JSON.stringify(abc) === '{"3":"a","a":{"b":{"c":"def"}},"q":"t 5"}';

    var strArr = String(str).replace(/^&/, '').replace(/&$/, '').split('&'),
        sal = strArr.length,
        i, j, ct, p, lastObj, obj, lastIter, undef, chr, tmp, key, value,
        postLeftBracketPos, keys, keysLen,
        fixStr = function (str) {
            return decodeURIComponent(str.replace(/\+/g, '%20'));
        };

    if (!array) {
        array = this.window;
    }

    for (i = 0; i < sal; i++) {
        tmp = strArr[i].split('=');
        key = fixStr(tmp[0]);
        value = (tmp.length < 2) ? '' : fixStr(tmp[1]);

        while (key.charAt(0) === ' ') {
            key = key.slice(1);
        }
        if (key.indexOf('\x00') > -1) {
            key = key.slice(0, key.indexOf('\x00'));
        }
        if (key && key.charAt(0) !== '[') {
            keys = [];
            postLeftBracketPos = 0;
            for (j = 0; j < key.length; j++) {
                if (key.charAt(j) === '[' && !postLeftBracketPos) {
                    postLeftBracketPos = j + 1;
                } else if (key.charAt(j) === ']') {
                    if (postLeftBracketPos) {
                        if (!keys.length) {
                            keys.push(key.slice(0, postLeftBracketPos - 1));
                        }
                        keys.push(key.substr(postLeftBracketPos, j - postLeftBracketPos));
                        postLeftBracketPos = 0;
                        if (key.charAt(j + 1) !== '[') {
                            break;
                        }
                    }
                }
            }
            if (!keys.length) {
                keys = [key];
            }
            for (j = 0; j < keys[0].length; j++) {
                chr = keys[0].charAt(j);
                if (chr === ' ' || chr === '.' || chr === '[') {
                    keys[0] = keys[0].substr(0, j) + '_' + keys[0].substr(j + 1);
                }
                if (chr === '[') {
                    break;
                }
            }

            obj = array;
            for (j = 0, keysLen = keys.length; j < keysLen; j++) {
                key = keys[j].replace(/^['"]/, '').replace(/['"]$/, '');
                lastIter = j !== keys.length - 1;
                lastObj = obj;
                if ((key !== '' && key !== ' ') || j === 0) {
                    if (obj[key] === undef) {
                        obj[key] = {};
                    }
                    obj = obj[key];
                } else { // To insert new dimension
                    ct = -1;
                    for (p in obj) {
                        if (obj.hasOwnProperty(p)) {
                            if (+p > ct && p.match(/^\d+$/g)) {
                                ct = +p;
                            }
                        }
                    }
                    key = ct + 1;
                }
            }
            lastObj[key] = value;
        }
    }
}

function isset() {
    var a = arguments, l = a.length, i = 0, undef;

    if (l === 0) {
        throw new Error('Empty isset');
    }

    while (i !== l) {
        if (a[i] === undef || a[i] === null) {
            return false;
        }
        i++;
    }
    return true;
}

function explode(delimiter, string, limit) {

    if (arguments.length < 2 || typeof delimiter === 'undefined' || typeof string === 'undefined') return null;
    if (delimiter === '' || delimiter === false || delimiter === null) return false;
    if (typeof delimiter === 'function' || typeof delimiter === 'object' || typeof string === 'function' || typeof string === 'object') {
        return {0: ''};
    }
    if (delimiter === true) delimiter = '1';

    // Here we go...
    delimiter += '';
    string += '';

    var s = string.split(delimiter);

    if (typeof limit === 'undefined') return s;

    // Support for limit
    if (limit === 0) limit = 1;

    // Positive limit
    if (limit > 0) {
        if (limit >= s.length) return s;
        return s.slice(0, limit - 1).concat([s.slice(limit - 1).join(delimiter)]);
    }

    // Negative limit
    if (-limit >= s.length) return [];

    s.splice(s.length + limit);
    return s;
}

function implode(glue, pieces) {
    // http://kevin.vanzonneveld.net
    // +   original by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // +   improved by: Waldo Malqui Silva
    // +   improved by: Itsacon (http://www.itsacon.net/)
    // +   bugfixed by: Brett Zamir (http://brett-zamir.me)
    // *     example 1: implode(' ', ['Kevin', 'van', 'Zonneveld']);
    // *     returns 1: 'Kevin van Zonneveld'
    // *     example 2: implode(' ', {first:'Kevin', last: 'van Zonneveld'});
    // *     returns 2: 'Kevin van Zonneveld'
    var i = '', retVal = '', tGlue = '';
    if (arguments.length === 1) {
        pieces = glue;
        glue = '';
    }
    if (typeof pieces === 'object') {
        if (Object.prototype.toString.call(pieces) === '[object Array]') {
            return pieces.join(glue);
        }
        for (i in pieces) {
            retVal += tGlue + pieces[i];
            tGlue = glue;
        }
        return retVal;
    }
    return pieces;
}

function in_array(needle, haystack, argStrict) {
    var key = '', strict = !!argStrict;

    if (strict) {
        for (key in haystack) {
            if (haystack[key] === needle) {
                return true;
            }
        }
    } else {
        for (key in haystack) {
            if (haystack[key] == needle) {
                return true;
            }
        }
    }

    return false;
}

function array_diff(arr1) {
    // http://kevin.vanzonneveld.net
    // +   original by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // +   improved by: Sanjoy Roy
    // +    revised by: Brett Zamir (http://brett-zamir.me)
    // *     example 1: array_diff(['Kevin', 'van', 'Zonneveld'], ['van', 'Zonneveld']);
    // *     returns 1: {0:'Kevin'}
    var retArr = {}, argl = arguments.length, k1 = '', i = 1, k = '', arr = {};

    arr1keys: for (k1 in arr1) {
        for (i = 1; i < argl; i++) {
            arr = arguments[i];
            for (k in arr) {
                if (arr[k] === arr1[k1]) {
                    // If it reaches here, it was found in at least one array, so try next value
                    continue arr1keys;
                }
            }
            retArr[k1] = arr1[k1];
        }
    }

    return retArr;
}

function json_encode(mixed_val) {
    //       discuss at: http://phpjs.org/functions/json_encode/
    //      original by: Public Domain (http://www.json.org/json2.js)
    // reimplemented by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    //      improved by: Michael White
    //         input by: felix
    //      bugfixed by: Brett Zamir (http://brett-zamir.me)
    //        example 1: json_encode('Kevin');
    //        returns 1: '"Kevin"'

    /*
     http://www.JSON.org/json2.js
     2008-11-19
     Public Domain.
     NO WARRANTY EXPRESSED OR IMPLIED. USE AT YOUR OWN RISK.
     See http://www.JSON.org/js.html
     */
    var retVal, json = this.window.JSON;
    try {
        if (typeof json === 'object' && typeof json.stringify === 'function') {
            retVal = json.stringify(mixed_val); // Errors will not be caught here if our own equivalent to resource
            //  (an instance of PHPJS_Resource) is used
            if (retVal === undefined) {
                throw new SyntaxError('json_encode');
            }
            return retVal;
        }

        var value = mixed_val;

        var quote = function (string) {
            var escapable =
                /[\\\"\u0000-\u001f\u007f-\u009f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g;
            var meta = { // table of character substitutions
                '\b': '\\b',
                '\t': '\\t',
                '\n': '\\n',
                '\f': '\\f',
                '\r': '\\r',
                '"': '\\"',
                '\\': '\\\\'
            };

            escapable.lastIndex = 0;
            return escapable.test(string) ? '"' + string.replace(escapable, function (a) {
                var c = meta[a];
                return typeof c === 'string' ? c : '\\u' + ('0000' + a.charCodeAt(0)
                    .toString(16))
                    .slice(-4);
            }) + '"' : '"' + string + '"';
        };

        var str = function (key, holder) {
            var gap = '';
            var indent = '    ';
            var i = 0; // The loop counter.
            var k = ''; // The member key.
            var v = ''; // The member value.
            var length = 0;
            var mind = gap;
            var partial = [];
            var value = holder[key];

            // If the value has a toJSON method, call it to obtain a replacement value.
            if (value && typeof value === 'object' && typeof value.toJSON === 'function') {
                value = value.toJSON(key);
            }

            // What happens next depends on the value's type.
            switch (typeof value) {
                case 'string':
                    return quote(value);

                case 'number':
                    // JSON numbers must be finite. Encode non-finite numbers as null.
                    return isFinite(value) ? String(value) : 'null';

                case 'boolean':
                case 'null':
                    // If the value is a boolean or null, convert it to a string. Note:
                    // typeof null does not produce 'null'. The case is included here in
                    // the remote chance that this gets fixed someday.
                    return String(value);

                case 'object':
                    // If the type is 'object', we might be dealing with an object or an array or
                    // null.
                    // Due to a specification blunder in ECMAScript, typeof null is 'object',
                    // so watch out for that case.
                    if (!value) {
                        return 'null';
                    }
                    if ((this.PHPJS_Resource && value instanceof this.PHPJS_Resource) || (window.PHPJS_Resource &&
                        value instanceof window.PHPJS_Resource)) {
                        throw new SyntaxError('json_encode');
                    }

                    // Make an array to hold the partial results of stringifying this object value.
                    gap += indent;
                    partial = [];

                    // Is the value an array?
                    if (Object.prototype.toString.apply(value) === '[object Array]') {
                        // The value is an array. Stringify every element. Use null as a placeholder
                        // for non-JSON values.
                        length = value.length;
                        for (i = 0; i < length; i += 1) {
                            partial[i] = str(i, value) || 'null';
                        }

                        // Join all of the elements together, separated with commas, and wrap them in
                        // brackets.
                        v = partial.length === 0 ? '[]' : gap ? '[\n' + gap + partial.join(',\n' + gap) + '\n' + mind +
                            ']' : '[' + partial.join(',') + ']';
                        gap = mind;
                        return v;
                    }

                    // Iterate through all of the keys in the object.
                    for (k in value) {
                        if (Object.hasOwnProperty.call(value, k)) {
                            v = str(k, value);
                            if (v) {
                                partial.push(quote(k) + (gap ? ': ' : ':') + v);
                            }
                        }
                    }

                    // Join all of the member texts together, separated with commas,
                    // and wrap them in braces.
                    v = partial.length === 0 ? '{}' : gap ? '{\n' + gap + partial.join(',\n' + gap) + '\n' + mind + '}' :
                        '{' + partial.join(',') + '}';
                    gap = mind;
                    return v;
                case 'undefined':
                // Fall-through
                case 'function':
                // Fall-through
                default:
                    throw new SyntaxError('json_encode');
            }
        };

        // Make a fake root object containing our value under the key of ''.
        // Return the result of stringifying the value.
        return str('', {
            '': value
        });

    } catch (err) { // Todo: ensure error handling above throws a SyntaxError in all cases where it could
        // (i.e., when the JSON global is not available and there is an error)
        if (!(err instanceof SyntaxError)) {
            throw new Error('Unexpected error type in json_encode()');
        }
        this.php_js = this.php_js || {};
        this.php_js.last_error_json = 4; // usable by json_last_error()
        return null;
    }
}

function json_decode(str_json) {
    //       discuss at: http://phpjs.org/functions/json_decode/
    //      original by: Public Domain (http://www.json.org/json2.js)
    // reimplemented by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    //      improved by: T.J. Leahy
    //      improved by: Michael White
    //        example 1: json_decode('[ 1 ]');
    //        returns 1: [1]

    /*
     http://www.JSON.org/json2.js
     2008-11-19
     Public Domain.
     NO WARRANTY EXPRESSED OR IMPLIED. USE AT YOUR OWN RISK.
     See http://www.JSON.org/js.html
     */

    var json = this.window.JSON;
    if (typeof json === 'object' && typeof json.parse === 'function') {
        try {
            return json.parse(str_json);
        } catch (err) {
            if (!(err instanceof SyntaxError)) {
                throw new Error('Unexpected error type in json_decode()');
            }
            this.php_js = this.php_js || {};
            this.php_js.last_error_json = 4; // usable by json_last_error()
            return null;
        }
    }

    var cx = /[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g;
    var j;
    var text = str_json;

    // Parsing happens in four stages. In the first stage, we replace certain
    // Unicode characters with escape sequences. JavaScript handles many characters
    // incorrectly, either silently deleting them, or treating them as line endings.
    cx.lastIndex = 0;
    if (cx.test(text)) {
        text = text.replace(cx, function (a) {
            return '\\u' + ('0000' + a.charCodeAt(0)
                .toString(16))
                .slice(-4);
        });
    }

    // In the second stage, we run the text against regular expressions that look
    // for non-JSON patterns. We are especially concerned with '()' and 'new'
    // because they can cause invocation, and '=' because it can cause mutation.
    // But just to be safe, we want to reject all unexpected forms.
    // We split the second stage into 4 regexp operations in order to work around
    // crippling inefficiencies in IE's and Safari's regexp engines. First we
    // replace the JSON backslash pairs with '@' (a non-JSON character). Second, we
    // replace all simple value tokens with ']' characters. Third, we delete all
    // open brackets that follow a colon or comma or that begin the text. Finally,
    // we look to see that the remaining characters are only whitespace or ']' or
    // ',' or ':' or '{' or '}'. If that is so, then the text is safe for eval.
    if ((/^[\],:{}\s]*$/)
        .test(text.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g, '@')
            .replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, ']')
            .replace(/(?:^|:|,)(?:\s*\[)+/g, ''))) {

        // In the third stage we use the eval function to compile the text into a
        // JavaScript structure. The '{' operator is subject to a syntactic ambiguity
        // in JavaScript: it can begin a block or an object literal. We wrap the text
        // in parens to eliminate the ambiguity.
        j = eval('(' + text + ')');

        return j;
    }

    this.php_js = this.php_js || {};
    this.php_js.last_error_json = 4; // usable by json_last_error()
    return null;
}

function base64_decode(data) {
    //  discuss at: http://phpjs.org/functions/base64_decode/
    // original by: Tyler Akins (http://rumkin.com)
    // improved by: Thunder.m
    // improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    //    input by: Aman Gupta
    //    input by: Brett Zamir (http://brett-zamir.me)
    // bugfixed by: Onno Marsman
    // bugfixed by: Pellentesque Malesuada
    // bugfixed by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    //   example 1: base64_decode('S2V2aW4gdmFuIFpvbm5ldmVsZA==');
    //   returns 1: 'Kevin van Zonneveld'
    //   example 2: base64_decode('YQ===');
    //   returns 2: 'a'

    var b64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
    var o1, o2, o3, h1, h2, h3, h4, bits, i = 0,
        ac = 0,
        dec = '',
        tmp_arr = [];

    if (!data) {
        return data;
    }

    data += '';

    do { // unpack four hexets into three octets using index points in b64
        h1 = b64.indexOf(data.charAt(i++));
        h2 = b64.indexOf(data.charAt(i++));
        h3 = b64.indexOf(data.charAt(i++));
        h4 = b64.indexOf(data.charAt(i++));

        bits = h1 << 18 | h2 << 12 | h3 << 6 | h4;

        o1 = bits >> 16 & 0xff;
        o2 = bits >> 8 & 0xff;
        o3 = bits & 0xff;

        if (h3 == 64) {
            tmp_arr[ac++] = String.fromCharCode(o1);
        } else if (h4 == 64) {
            tmp_arr[ac++] = String.fromCharCode(o1, o2);
        } else {
            tmp_arr[ac++] = String.fromCharCode(o1, o2, o3);
        }
    } while (i < data.length);

    dec = tmp_arr.join('');

    return dec.replace(/\0+$/, '');
}

function base64_encode(data) {
    //  discuss at: http://phpjs.org/functions/base64_encode/
    // original by: Tyler Akins (http://rumkin.com)
    // improved by: Bayron Guevara
    // improved by: Thunder.m
    // improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // improved by: Rafał Kukawski (http://kukawski.pl)
    // bugfixed by: Pellentesque Malesuada
    //   example 1: base64_encode('Kevin van Zonneveld');
    //   returns 1: 'S2V2aW4gdmFuIFpvbm5ldmVsZA=='
    //   example 2: base64_encode('a');
    //   returns 2: 'YQ=='

    var b64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
    var o1, o2, o3, h1, h2, h3, h4, bits, i = 0,
        ac = 0,
        enc = '',
        tmp_arr = [];

    if (!data) {
        return data;
    }

    do { // pack three octets into four hexets
        o1 = data.charCodeAt(i++);
        o2 = data.charCodeAt(i++);
        o3 = data.charCodeAt(i++);

        bits = o1 << 16 | o2 << 8 | o3;

        h1 = bits >> 18 & 0x3f;
        h2 = bits >> 12 & 0x3f;
        h3 = bits >> 6 & 0x3f;
        h4 = bits & 0x3f;

        // use hexets to index into b64, and append result to encoded string
        tmp_arr[ac++] = b64.charAt(h1) + b64.charAt(h2) + b64.charAt(h3) + b64.charAt(h4);
    } while (i < data.length);

    enc = tmp_arr.join('');

    var r = data.length % 3;

    return (r ? enc.slice(0, r - 3) : enc) + '==='.slice(r || 3);
}

function validateMobile(mobile) {
    mobile = mobile.replace(/\s/g, '');
    mobile = mobile.replace(/\./g, '');
    mobile = mobile.replace(/,/g, '');
    mobile = mobile.replace(/^(\+84|84|\(84\))/, '0');

    if (/^0/.exec(mobile) == null) {
        mobile = '0' + mobile;
    }
    if (isNaN(mobile) || mobile.length < 10 || mobile.length > 11) {
        return false;
    }

    return true;
}

function validateEmail(email) {
    var regexPattern = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (!regexPattern.test(email)) {
        return false;
    }
    return true;
}

/**
 *
 * @type {{load: CheckPromotionOrder.load, updateOrder: CheckPromotionOrder.updateOrder}}
 */
var CheckPromotionOrder = {
    load: function (totalDiscount, totalMoney, shipFee, currency) {
        var customerMobile = $('input[name=customerMobile]').val();
        if (!currency || currency === '') {
            currency = " đ";
        }
        if (customerMobile && validateMobile(customerMobile)) {
            CheckPromotionOrder.updateOrder(customerMobile, totalDiscount, totalMoney, shipFee, currency)
        }
        $('input[name=customerMobile]').on('change', function () {
            var t = $(this);
            if (validateMobile(t.val())) {
                CheckPromotionOrder.updateOrder(t.val(), totalDiscount, totalMoney, shipFee, currency)
            }
        });
    },
    updateOrder: function (customerMobile, totalDiscount, totalMoney, shipFee, currency) {
        $.post(
            '/promotion/checkpromotionorder',
            {
                customerMobile: customerMobile
            },
            function (rs) {
                var shipFeeVal = parseInt($(shipFee).attr('value')),
                    ttDisVal = 0,
                    ttMonVal = 0,
                    disVal = 0;
                if (rs.code == 1) {
                    disVal = parseInt(rs.moneyDiscount);
                    if((parseInt(rs.moneyDiscount) > 0) && (parseInt(rs.orderDiscount) > 0)){
                        disVal = parseInt(rs.moneyDiscount) - parseInt(rs.orderDiscount);
                    }
                    if ($(totalDiscount).attr('value')) {
                        ttDisVal = parseInt($(totalDiscount).attr('value')) + disVal;
                    } else {
                        ttDisVal = parseInt($(totalDiscount).attr('data-value')) + disVal;
                    }

                    ttMonVal = parseInt($(totalMoney).attr('data-beforediscount')) - disVal + shipFeeVal;

                    $(totalDiscount).html($.number(ttDisVal) + currency).attr('data-value', ttDisVal).attr('value', 0);
                    $(totalMoney).html($.number(ttMonVal) + currency).attr('current-value', ttMonVal);
                    //CustomerShipFee.updateCustomershipFee(toCity,toDistrict,shipFee, totalMoney, inputCoupon, currency, 1, ttMonVal- shipFeeVal,'');
                } else {
                    if ($(totalDiscount).attr('data-currentvalue')) {
                        ttDisVal = parseInt($(totalDiscount).attr('data-currentvalue')) - parseInt($(totalDiscount).attr('data-value'));
                    } else {
                        ttDisVal = parseInt($(totalDiscount).attr('data-value'));
                    }
                    if ($(totalMoney).attr('data-value')) {
                        ttMonVal = parseInt($(totalMoney).attr('data-value')) + shipFeeVal;
                    } else {
                        ttMonVal = parseInt($(totalMoney).attr('value')) + shipFeeVal;
                    }

                    $(totalDiscount).html($.number(ttDisVal) + currency).attr('data-currentvalue', ttDisVal).attr('data-value', ttDisVal);
                    $(totalMoney).html($.number(ttMonVal) + currency).attr('current-value', ttMonVal).attr('value', ttMonVal);
                }
            }
        )
    }
};

function checkCoupon() {
    var totalMoney = parseInt($('.totalCurentMoney').val());
    AppAjax.post(
        '/promotion/checkcoupon', {couponCode: $('#coupon').val()},
        function (rs) {
            if (rs.code == 1) {
                $('.showTotalCurentMoney').html($.number(totalMoney - parseInt(rs.value)) + ' đ');
                $('.messageCouponDefault').html('Mã giảm giá: ' + ' : - ' + $.number(rs.value) + ' đ');
                $('.totalCurentMoney').val(totalMoney - parseInt(rs.value));
                $('.messageCouponDefault').attr('data-valueTemp', rs.value);
            } else {
                alert(rs.msg);
                $('.showTotalCurentMoney').html($.number((totalMoney + parseInt($('.messageCouponDefault').attr('data-valueTemp')))) + ' đ');
                $('.totalCurentMoney').val(totalMoney + parseInt($('.messageCouponDefault').attr('data-valueTemp')));
                $('.messageCouponDefault').attr('data-valueTemp', 0);
                $('.messageCouponDefault').html('');
            }
        },
        'json'
    );
}

/*
* check tồn SP
* btnAddToCart: nút mua hàng
* quantity: input số lượng
* req: class đi với màu và size
* color: ô chưa foreach màu (VD: .req.color)
* colorItem: ô chọn màu
* colorActiveItem: ô màu được active
* size: ô chưa foreach size (VD: .req.size)
* sizeItem: ô chọn size
* sizeActiveItem: size được active
* mainPrice: class để đổi giá trong các trường hợp size, màu được active
* oldPPriceLib: class để đổi giá cũ trong các trường hợp size, màu được active
* discountPriceLib: class để đổi giá khuyến mại trong các trường hợp size, màu được active
* currency: đơn vị tiền tệ
* PercentLib: tham số truyền vào khi muốn hiển thị % khuyến mại (VD: true/false)
* extenDiscount: hậu tố thêm vào đằng sau giá khuyến mại, có thể điền hoặc không.
* */
function checkInvProduct(options) {
    if (typeof options == 'undefined') {
        options = {};
    }
    var attrs = {},
        atc = options.btnAddToCart ? options.btnAddToCart : $('body .btnAddToCart'),
        qtt = options.quantity ? options.quantity : $('body #pquantity'),
        req = options.req ? options.req.length : $('body .req').length,
        color = options.color ? options.color : $('body .req.color'),
        colorItem = options.colorItem ? options.colorItem : $('body .req.color a'),
        colorActiveItem = options.colorActiveItem ? options.colorActiveItem : $('body .req.color a.active'),
        size = options.size ? options.size : $('body .req.size'),
        sizeItem = options.sizeItem ? options.sizeItem : $('body .req.size a'),
        sizeActiveItem = options.sizeActiveItem ? options.sizeActiveItem : $('body .req.size a.active'),
        mainPrice = options.mainPrice ? options.mainPrice : $('body .main-price'),
        oldPPriceLib = options.oldPPriceLib ? options.oldPPriceLib : $('body .old-lib-price'),
        PercentLib = options.PercentLib ? options.PercentLib : false,
        discountPriceLib = options.discountPriceLib ? options.discountPriceLib : $('body .discount-lib-price'),
        currency = options.currency ? options.currency : '',
        extenDiscount = options.extenDiscount ? options.extenDiscount : '';
    if (req == 1) {
        if (color.length) {
            if (colorActiveItem.length) {
                attrs[color.attr('data-column')] = colorActiveItem.attr('data-value');
                $.post(
                    '/product/child?psId=' + atc.attr('data-psid'),
                    {'attrs': attrs},
                    function (rs) {
                        if (rs.code == 1 && rs.data.available > 0) {
                            qtt.attr('max', rs.data.available);
                            atc.attr({
                                'data-selId': rs.data.id,
                                'data-ck': 1
                            })
                                .removeAttr('data-original-title').removeClass('unsel');
                            atc.removeAttr('title');
                            // mainPrice.html($.number(rs.data.price) + currency);
                            if (oldPPriceLib.length){
                                if (rs.data.price <= 0){
                                    mainPrice.html('Liên hệ');
                                    oldPPriceLib.hide();
                                    discountPriceLib.hide();
                                }else {
                                    if(rs.data.moneyDiscount > 0){
                                        mainPrice.html($.number(rs.data.price) + currency);
                                        oldPPriceLib.html($.number(rs.data.price + rs.data.moneyDiscount) + currency);
                                        if (PercentLib == true){
                                            discountPriceLib.html($.number((rs.data.moneyDiscount/rs.data.price)*100) + '%' + extenDiscount);
                                        }else {
                                            discountPriceLib.html($.number(rs.data.moneyDiscount) + currency + extenDiscount);
                                        }
                                    }else {
                                        mainPrice.html($.number(rs.data.price) + currency);
                                        if(rs.data.oldPrice > 0){
                                            oldPPriceLib.html($.number(rs.data.oldPrice) + currency);
                                            if (PercentLib == true){
                                                discountPriceLib.html($.number((rs.data.oldPrice - rs.data.price)/rs.data.oldPrice*100) + '%' + extenDiscount);
                                            }else {
                                                discountPriceLib.html($.number((rs.data.oldPrice - rs.data.price)) + currency + extenDiscount);
                                            }
                                        }else {
                                            oldPPriceLib.hide();
                                            discountPriceLib.hide();
                                        }
                                    }
                                }
                            }else {
                                if (rs.data.price <= 0){
                                    mainPrice.html('Liên hệ');
                                }else {
                                    if(rs.data.moneyDiscount > 0){
                                        mainPrice.html($.number(rs.data.price) + currency);
                                        mainPrice.append('<span class="oldPrice">'+ $.number(rs.data.price + rs.data.moneyDiscount) + currency +'</span>');
                                        if (PercentLib == true){
                                            mainPrice.append('<span class="discountPercent">'+ $.number((rs.data.moneyDiscount/rs.data.price)*100) +'%'+ extenDiscount +'</span>');
                                        }else {
                                            mainPrice.append('<span class="discountPercent">'+ $.number(rs.data.moneyDiscount) + currency + extenDiscount +'</span>');
                                        }
                                    }else {
                                        mainPrice.html($.number(rs.data.price) + currency);
                                        if(rs.data.oldPrice > 0){
                                            mainPrice.append('<span class="oldPrice">'+ $.number(rs.data.oldPrice) + currency +'</span>');
                                            if (PercentLib == true){
                                                mainPrice.append('<span class="discountPercent">'+ $.number((rs.data.oldPrice - rs.data.price)/rs.data.oldPrice*100) +'%'+ extenDiscount +'</span>');
                                            }else {
                                                mainPrice.append('<span class="discountPercent">'+ $.number((rs.data.oldPrice - rs.data.price)) + currency + extenDiscount +'</span>');

                                            }
                                        }
                                    }
                                }
                            }
                        } else {
                            atc.attr('title', msgOutofStock);
                        }
                    },
                    'json'
                );
            } else {
                colorItem.each(function () {
                    var t = $(this);
                    attrs[color.attr('data-column')] = t.attr('data-value');
                    $.post(
                        '/product/child?psId=' + atc.attr('data-psid'),
                        {'attrs': attrs},
                        function (rs) {
                            if (rs.code == 1 && rs.data.available > 0) {
                                t.attr({
                                    'qtt': rs.data.available,
                                    'data-selId': rs.data.id,
                                    'data-price': rs.data.price,
                                    'data-oldPrice': rs.data.oldPrice,
                                    'data-moneyDiscount': rs.data.moneyDiscount,
                                });
                            } else {
                                t.addClass('deactive').attr('title', msgOutofStock);
                            }
                        },
                        'json'
                    );
                });
            }
        } else {
            if (sizeActiveItem.length) {
                attrs[size.attr('data-column')] = sizeActiveItem.attr('data-value');
                $.post(
                    '/product/child?psId=' + atc.attr('data-psid'),
                    {'attrs': attrs},
                    function (rs) {
                        if (rs.code == 1 && rs.data.available > 0) {
                            qtt.attr('max', rs.data.available);
                            atc.attr({
                                'data-selId': rs.data.id,
                                'data-ck': 1
                            }).removeAttr('data-original-title').removeClass('unsel');
                            atc.removeAttr('title');
                            if (oldPPriceLib.length){
                                if (rs.data.price <= 0){
                                    mainPrice.html('Liên hệ');
                                    oldPPriceLib.hide();
                                    discountPriceLib.hide();
                                }else {
                                    if(rs.data.moneyDiscount > 0){
                                        mainPrice.html($.number(rs.data.price) + currency);
                                        oldPPriceLib.html($.number(rs.data.price + rs.data.moneyDiscount) + currency);
                                        if (PercentLib == true){
                                            discountPriceLib.html($.number((rs.data.moneyDiscount/rs.data.price)*100) + '%' + extenDiscount);
                                        }else {
                                            discountPriceLib.html($.number(rs.data.moneyDiscount) + currency + extenDiscount);
                                        }
                                    }else {
                                        mainPrice.html($.number(rs.data.price) + currency);
                                        if(rs.data.oldPrice > 0){
                                            oldPPriceLib.html($.number(rs.data.oldPrice) + currency);
                                            if (PercentLib == true){
                                                discountPriceLib.html($.number((rs.data.oldPrice - rs.data.price)/rs.data.oldPrice*100) + '%' + extenDiscount);
                                            }else {
                                                discountPriceLib.html($.number((rs.data.oldPrice - rs.data.price)) + currency + extenDiscount);
                                            }
                                        }else {
                                            oldPPriceLib.hide();
                                            discountPriceLib.hide();
                                        }
                                    }
                                }
                            }else {
                                if (rs.data.price <= 0){
                                    mainPrice.html('Liên hệ');
                                }else {
                                    if(rs.data.moneyDiscount > 0){
                                        mainPrice.html($.number(rs.data.price) + currency);
                                        mainPrice.append('<span class="oldPrice">'+ $.number(rs.data.price + rs.data.moneyDiscount) + currency +'</span>');
                                        if (PercentLib == true){
                                            mainPrice.append('<span class="discountPercent">'+ $.number((rs.data.moneyDiscount/rs.data.price)*100) +'%'+ extenDiscount +'</span>');
                                        }else {
                                            mainPrice.append('<span class="discountPercent">'+ $.number(rs.data.moneyDiscount) + currency + extenDiscount +'</span>');
                                        }
                                    }else {
                                        mainPrice.html($.number(rs.data.price) + currency);
                                        if(rs.data.oldPrice > 0){
                                            mainPrice.append('<span class="oldPrice">'+ $.number(rs.data.oldPrice) + currency +'</span>');
                                            if (PercentLib == true){
                                                mainPrice.append('<span class="discountPercent">'+ $.number((rs.data.oldPrice - rs.data.price)/rs.data.oldPrice*100) +'%'+ extenDiscount +'</span>');
                                            }else {
                                                mainPrice.append('<span class="discountPercent">'+ $.number((rs.data.oldPrice - rs.data.price)) + currency + extenDiscount +'</span>');

                                            }
                                        }
                                    }
                                }
                            }
                        } else {
                            atc.attr('title', msgOutofStock);
                        }
                    },
                    'json'
                );
            } else {
                sizeItem.each(function () {
                    var t = $(this);
                    attrs[size.attr('data-column')] = t.attr('data-value');
                    $.post(
                        '/product/child?psId=' + atc.attr('data-psid'),
                        {'attrs': attrs},
                        function (rs) {
                            if (rs.code == 1 && rs.data.available > 0) {
                                t.attr({
                                    'qtt': rs.data.available,
                                    'data-selId': rs.data.id,
                                    'data-price': rs.data.price,
                                    'data-oldPrice': rs.data.oldPrice,
                                    'data-moneyDiscount': rs.data.moneyDiscount,
                                });
                            } else {
                                t.addClass('deactive').attr('title', msgOutofStock);
                            }
                        },
                        'json'
                    );
                });
            }
        }
        return false;
    }
    if (req > 1) {
        if (colorActiveItem.length && sizeActiveItem.length) {
            attrs[color.attr('data-column')] = colorActiveItem.attr('data-value');
            attrs[size.attr('data-column')] = sizeActiveItem.attr('data-value');
            $.post(
                '/product/child?psId=' + atc.attr('data-psid'),
                {'attrs': attrs},
                function (rs) {
                    if (rs.code == 1 && rs.data.available > 0) {
                        qtt.attr('max', rs.data.available);
                        atc.removeAttr('data-original-title')
                            .removeClass('unsel')
                            .attr({
                                'data-selId': rs.data.id,
                                'data-ck': 1
                            });
                        atc.removeAttr('title');
                        // mainPrice.html($.number(rs.data.price) + currency);
                        if (oldPPriceLib.length){
                            if (rs.data.price <= 0){
                                mainPrice.html('Liên hệ');
                                oldPPriceLib.hide();
                                discountPriceLib.hide();
                            }else {
                                if(rs.data.moneyDiscount > 0){
                                    mainPrice.html($.number(rs.data.price) + currency);
                                    oldPPriceLib.html($.number(rs.data.price + rs.data.moneyDiscount) + currency);
                                    if (PercentLib == true){
                                        discountPriceLib.html($.number((rs.data.moneyDiscount/rs.data.price)*100) + '%' + extenDiscount);
                                    }else {
                                        discountPriceLib.html($.number(rs.data.moneyDiscount) + currency + extenDiscount);
                                    }
                                }else {
                                    mainPrice.html($.number(rs.data.price) + currency);
                                    if(rs.data.oldPrice > 0){
                                        oldPPriceLib.html($.number(rs.data.oldPrice) + currency);
                                        if (PercentLib == true){
                                            discountPriceLib.html($.number((rs.data.oldPrice - rs.data.price)/rs.data.oldPrice*100) + '%' + extenDiscount);
                                        }else {
                                            discountPriceLib.html($.number((rs.data.oldPrice - rs.data.price)) + currency + extenDiscount);
                                        }
                                    }else {
                                        oldPPriceLib.hide();
                                        discountPriceLib.hide();
                                    }
                                }
                            }
                        }else {
                            if (rs.data.price <= 0){
                                mainPrice.html('Liên hệ');
                            }else {
                                if(rs.data.moneyDiscount > 0){
                                    mainPrice.html($.number(rs.data.price) + currency);
                                    mainPrice.append('<span class="oldPrice">'+ $.number(rs.data.price + rs.data.moneyDiscount) + currency +'</span>');
                                    if (PercentLib == true){
                                        mainPrice.append('<span class="discountPercent">'+ $.number((rs.data.moneyDiscount/rs.data.price)*100) +'%'+ extenDiscount +'</span>');
                                    }else {
                                        mainPrice.append('<span class="discountPercent">'+ $.number(rs.data.moneyDiscount) + currency + extenDiscount +'</span>');
                                    }
                                }else {
                                    mainPrice.html($.number(rs.data.price) + currency);
                                    if(rs.data.oldPrice > 0){
                                        mainPrice.append('<span class="oldPrice">'+ $.number(rs.data.oldPrice) + currency +'</span>');
                                        if (PercentLib == true){
                                            mainPrice.append('<span class="discountPercent">'+ $.number((rs.data.oldPrice - rs.data.price)/rs.data.oldPrice*100) +'%'+ extenDiscount +'</span>');
                                        }else {
                                            mainPrice.append('<span class="discountPercent">'+ $.number((rs.data.oldPrice - rs.data.price)) + currency + extenDiscount +'</span>');

                                        }
                                    }
                                }
                            }
                        }
                    } else {
                        sizeActiveItem.addClass('deactive').attr('title', msgOutofStock);
                        atc.attr('title', msgOutofStock);
                    }
                },
                'json'
            );
            return false;
        }
        if (colorActiveItem.length && !sizeActiveItem.length) {
            attrs[color.attr('data-column')] = colorActiveItem.attr('data-value');
            sizeItem.each(function () {
                var t = $(this);
                attrs[size.attr('data-column')] = t.attr('data-value');
                $.post(
                    '/product/child?psId=' + atc.attr('data-psid'),
                    {'attrs': attrs},
                    function (rs) {
                        if (rs.code == 1 && rs.data.available > 0) {
                            t.attr({
                                'qtt': rs.data.available,
                                'data-selId': rs.data.id,
                                'data-price': rs.data.price,
                                'data-oldPrice': rs.data.oldPrice,
                                'data-moneyDiscount': rs.data.moneyDiscount,
                            });
                        } else {
                            t.addClass('deactive').attr('title', msgOutofStock);
                        }
                    },
                    'json'
                );
            });
            return false;
        }
        if (!colorActiveItem.length && sizeActiveItem.length) {
            attrs[size.attr('data-column')] = sizeActiveItem.attr('data-value');
            colorItem.each(function () {
                var t = $(this);
                attrs[color.attr('data-column')] = t.attr('data-value');
                $.post(
                    '/product/child?psId=' + atc.attr('data-psid'),
                    {'attrs': attrs},
                    function (rs) {
                        if (rs.code == 1 && rs.data.available > 0) {
                            t.attr({
                                'qtt': rs.data.available,
                                'data-selId': rs.data.id,
                                'data-price': rs.data.price,
                                'data-oldPrice': rs.data.oldPrice,
                                'data-moneyDiscount': rs.data.moneyDiscount,
                            });
                        } else {
                            t.addClass('deactive').attr('title', msgOutofStock);
                        }
                    },
                    'json'
                );
            });
            return false;
        }
    }
}