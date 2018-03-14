var page_size = 20;
var group_id = "0";

var getMsgList = function (page) {
    var url = "/get_msg/?id=" + page + "&page_size=" + page_size + "&group_id=" + group_id;
    getData(url, function (data) {
        if (data !== null && data.code === "0000") {
            msg_list = data.msg_list;
            html = "";
            for (var i = 0; i < msg_list.length; i++) {
                html += "<tr><td>" + msg_list[i].id + "</td>";
                if (msg_list[i].is_group) {
                    html += "<td>群组</td>" +
                        "<td>" + msg_list[i].group_name + "</td>";
                } else {
                    html += "<td>个人</td>" +
                        "<td>-</td>";
                }
                html += "<td>" + msg_list[i].user_name + "</td>";
                html += "<td>" + msg_list[i].msg_content + "</td>";
                html += "<td>" + msg_list[i].created_at + "</td></tr>";
            }
            $("#message-list").html(html);
        }
        setPage(page, data.size);
    })
};

var setPage = function (index, size) {
    var options = {
        bootstrapMajorVersion: 3, //对应的bootstrap版本
        currentPage: index, //当前页数，这里是用的EL表达式，获取从后台传过来的值
        numberOfPages: page_size, //每页页数
        totalPages: size, //总页数，这里是用的EL表达式，获取从后台传过来的值
        numberOfPages: 5,
        itemTexts: function (type, page, current) {//设置显示的样式，默认是箭头
            switch (type) {
                case "first":
                    return "首页";
                case "prev":
                    return "上一页";
                case "next":
                    return "下一页";
                case "last":
                    return "末页";
                case "page":
                    return page;
            }
        },
        //点击事件
        onPageClicked: function (event, originalEvent, type, page) {
            getMsgList(page, group_id);
        }

    };
    $("#page").bootstrapPaginator(options);
};

var getGroupList = function () {
    getData("/get_group_list/", function (data) {
        console.log(data);
        if (data !== null && data.code === "0000") {
            group_list = data.group_list;
            html = "<option value='0'>全部</option>";
            for (var i = 0; i < group_list.length; i++) {
                html += "<option value='" + group_list[i].group_id + "'>" + group_list[i].group_name + "</option>";
            }
            $('#group-list').html(html);
        }
    })
};

var changeGroup = function (values) {
    group_id = values;
    getMsgList(1);
};

getMsgList(1);
getGroupList();