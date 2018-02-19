var postData = function (url, obj, callBack) {
    $.ajax({
        url: url,
        type: "POST",
        header: {
            type: "Access-Control-Allow-Origin:*"
        },
        dataType: "json",
        data: obj,
        success: function (result) {
            if (typeof callBack === 'function') {
                callBack(result);
            }
        },
        error: function (response) {
            var error_message = (response.status === 403) ? response.responseText : "程序处理异常，请稍后重试";
            alert(error_message);
        }
    });
};

var getData = function (url, callBack) {
    $.ajax({
        url: url,
        type: "GET",
        header: {
            type: "Access-Control-Allow-Origin:*"
        },
        success: function (result) {
            if (typeof callBack === 'function') {
                callBack(result);
            }
        },
        error: function (response) {
            var error_message = (response.status === 403) ? response.responseText : "程序处理异常，请稍后重试";
            alert(error_message);
        }
    });
};