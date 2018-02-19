var get_admin_list = function () {
    getData('admin_list/', function (data) {
        if (data != null) {
            html = "";
            for (var i = 0; i < data.length; i++) {
                html += "<tr><td>" + data[i].id + "</td>" +
                    "<td>" + data[i].name + "</td>";
                if (data[i].right_level === 0) {
                    html += "<td>全局</td>" +
                    "<td>-</td>";
                } else {
                    html += "<td>单群</td>" +
                    "<td>" + data[i].group_name + "</td>";
                }
                status = data[i].status === 0 ? "可用" : "不可用";
                html += "<td>" + status + "</td>";
                html += "<td><botton id='edit-" + data[i].id + "' class='btn btn-primary'>" +
                    "<i class='glyphicon glyphicon-edit'></i>修改</botton></td></tr>";
            }
            $('#admin-list').html(html);
        }
    })
};

var add_admin = function () {
    var name = $('#name').val();
    var level = $('#level').val();
    var group_name = $('#group-name').val();
    var status = $('#status').val();

    var params = {
        "name": name,
        "right_level": parseInt(level),
        "group_name": group_name,
        "status": parseInt(status)
    };
    postData('add_admin/', JSON.stringify(params), function (data) {
        if (data.code === '0000') {
            alert('添加管理员成功')
        }
        location.reload();
    });
};

var change_level = function () {
    var level = $('#level').val();
    if (level === '0') {
        $('#group-name').attr("disabled",true)
    } else {
        $('#group-name').attr("disabled",false)
    }
};

get_admin_list();