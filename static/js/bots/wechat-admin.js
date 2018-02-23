var adminList;
var id;

var get_admin_list = function () {
    getData('admin_list/', function (data) {
        if (data != null) {
            adminList = data;
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
                html += "<td><botton id='edit-" + data[i].id + "' onclick='init_edit(" + i + ")' class='btn btn-primary' data-toggle='modal' data-target='#editAdmin'>" +
                    "<i class='glyphicon glyphicon-edit'></i>修改</botton>" +
                    "<button class='btn btn-info' onclick='remove_admin(" + data[i].id +")'";
                if (data[i].status === -1){
                    html += "disabled";
                }
                html += "><i class='glyphicon glyphicon-stop'></i>暂停</button>" +
                    "<button onclick='delete_admin(" + data[i].id + ")' class='btn btn-danger'><i class='glyphicon glyphicon-remove'></i>删除</button>" +
                    "</td></tr>";
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
        } else {
            alert('添加管理员失败,请确认昵称与群名')
        }
        location.reload();
    });
};

var edit_admin = function () {
    var name = $('#editName').val();
    var level = $('#editLevel').val();
    var group_name = $('#editGroupName').val();
    var status = $('#editStatus').val();
    var params = {
        "id": id,
        "name": name,
        "right_level": parseInt(level),
        "group_name": group_name,
        "status": parseInt(status)
    };
    console.log(params);
    postData('edit_admin/', JSON.stringify(params), function (data) {
        if (data.code === '0000') {
            alert('修改管理员信息成功')
        }
        location.reload();
    });
};

var remove_admin = function (id) {
    getData('remove_admin/?id=' + id, function (data) {
        if (data.code === '0000') {
            alert('禁停成功')
        }
        location.reload();
    });
};

var delete_admin = function (id) {
    getData('delete_admin/?id=' + id, function (data) {
        if (data.code === '0000') {
            alert('删除成功')
        }
        location.reload();
    });
};

var init_edit = function (index) {
    $('#editName').val(adminList[index].name);
    $('#editLevel').val(adminList[index].right_level === 0 ? '0' : '1');
    $('#editGroupName').val(adminList[index].group_name);
    $('#editStatus').val(adminList[index].status === 0 ? '0' : '-1');
    id = adminList[index].id;
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