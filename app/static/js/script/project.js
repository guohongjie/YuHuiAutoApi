$("#btn2").click(function () {
    $.ajax({
        url: "/projectSearch",
        type: "get",
        data: {
            project: $("#project").find("option:selected").val(),
            test_group: $("#test_group").find("option:selected").val(),
            pro_status: $("#pro_status").find("option:selected").val(),
        }
    }).done(function (result) {
        if (result.status == "200")
        {
            var _temo = [];
            // alert(result['datas']);
            for (var i = 0; i < result['datas'].length; i++) {
                _temo.push(result['datas'][i]);
            }
            var tableHTML = "";
            // alert(_temo);
            // alert(_temo);
            for (var i = 0; i < _temo.length; i++) {
                var j = i + 1;
                tableHTML = tableHTML +
                '<tr><td style="display:none">' + j +
                '</td><td style="text-align:center">' + _temo[i][0] +
                '</td><td style="text-align:center">' + _temo[i][1] +
                '</td><td style="text-align:center">' + _temo[i][2] +
                '</td><td style="text-align:center">' + _temo[i][3] +
                '</td><td style="text-align:center">' + _temo[i][4] + '</td>'+
                 '<td><a data-pid="' + _temo[i][0] + '" class="btn btn-primary btn-large project_update">修改</a>'+ '</td>'+
                '</tr>';
            }//case_name+description+case_url+method+parameter+assert
            $("#casetb").html(tableHTML);
            // alert(tableHTML);
        }
        else{
            alert(result.error);
        }
    })
});

$(document).ready(function () {
//    $.ajax({
//        url: "http://uwsgi.sys.bandubanxie.com/projectSearch",
//        type: "get",
//        data: {
//            project: $("#project").find("option:selected").val()
//        }
//    }).done(function (result) {
//        if (result.status == "200") {
//            var _temo = [];
//            // alert(result['datas']);
//            for (var i = 0; i < result['datas'].length; i++) {
//                _temo.push(result['datas'][i]);
//            }
//            var tableHTML = "";
//            // alert(_temo);
//            // alert(_temo);
//            for (var i = 0; i < _temo.length; i++) {
//                var j = i + 1;
//                tableHTML = tableHTML + '<tr><td style="display:none">' + j + '</td><td >' + _temo[i][0] + '</td><td>' + _temo[i][1] + '</td><td>' + _temo[i][2] + '</td><td>' + _temo[i][3] + '</td></tr>';
//            }//case_name+description+case_url+method+parameter+assert
//            $("#casetb").html(tableHTML);
//            // alert(tableHTML);
//        }
//        else{
//            alert(result.error);
//        }
//    });

    $('.theme-login').click(function () {
        $('.theme-popover-mask').fadeIn(100);
        $("#project_name").val("");
        $("#project_domain").val("");
        $("#RC").val("");
        $("#targetId").val("");
        $("#startDate").val("");
        $("#endDate").val("");
        $('.theme-popover').slideDown(200);
    });
    $('.theme-poptit .close').click(function () {
        $('.theme-popover-mask').fadeOut(100);
        $('.theme-popover').slideUp(200, function () {
        });
    });

    $("#btn1").click(function () {
        var _case = []
        $("#tbdata tr").each(function () {
            var tr = $(this)
            var svn_url_str;
            _case.push({
                project: $("#project_name").val(),
                domain: $("#project_domain").val(),
                description:$("#RC").val()
            });
        });
        //alert(_case[0]);
        if ($("#targetId").val()!="") {
            //数据更新
            $.ajax({
                url: "/projectUpdate",
                type: "get",
                data: {
                    pid: $("#targetId").val(),
                    project: $("#project_name").val(),
                    project_en: $("#project_en").val(),
                    domain: $("#project_domain").val(),
                    description:$("#RC").val(),
                    startDate:$("#startDate").val(),
                    endDate:$("#endDate").val(),
                    project_status:$("#project_status").find("option:selected").val(),
                },
                success: function () {
                    alert("保存成功")
                    $.cookie('feature', _case[0].feature);
                    $.cookie('scene', _case[0].scene);
                    $("#feature").text($.cookie('feature'))
                    $("#scene").text($.cookie('scene'))
                    location.reload()
                }
            })
        } else {
            //数据新增
            $.ajax({
                url: "/projectInsert",
                type: "get",
                data: {
                    project: $("#project_name").val(),
                    project_en: $("#project_en").val(),
                    domain: $("#project_domain").val(),
                    description:$("#RC").val(),
                    startDate:$("#startDate").val(),
                    endDate:$("#endDate").val(),
                    project_status:$("#project_status").find("option:selected").val(),
                }}).done(function (result) {
                if (result.status == "200")
                    {
                    alert("保存成功");
                    $.ajax({
                        url: "/projectSearch",
                        type: "get",
                        data: {
                            project: $("#project").find("option:selected").val(),
                            test_group: $("#test_group").find("option:selected").val()
                        }
                    }).done(function (result) {
                        var _temo = [];
                        // alert(result['datas']);
                        for (var i = 0; i < result['datas'].length; i++) {
                            _temo.push(result['datas'][i]);
                        }
                        var tableHTML = "";
                        // alert(_temo);
                        for (var i = 0; i < _temo.length; i++) {
                            var j = i + 1;
                            tableHTML = tableHTML +
                            '<tr><td style="display:none">' + j +
                            '</td><td style="text-align:center" >' + _temo[i][0] +
                            '</td><td style="text-align:center">' + _temo[i][1] +
                            '</td><td style="text-align:center">' + _temo[i][2] +
                            '</td><td style="text-align:center">' + _temo[i][3] +
                            '</td><td style="text-align:center">' + _temo[i][4] +
                            '</td></tr>';
                        }//case_name+description+case_url+method+parameter+assert
                        $("#casetb").html(tableHTML);
                        $('.theme-popover-mask').fadeOut(100);
                        $('.theme-popover').slideUp(200);}
                        )
                    }
                    else{
                        alert("保存失败");
                        alert(result.result)
                        }
                    })
            }
    });
});
$("body").delegate(".project_update", "click",function(){
    pid = $(this).data("pid");
    $.ajax({
        url: "/projectSingleDatas",
        type: "get",
        data: {
            pid: pid,
        }
    }).done(function (result) {
    if (result["code"]=="400"){
        alert(result["datas"]);
    }
    else{
    $('.theme-popover').toggle();
    $("#project_name").val(result["datas"]["project_name"]);
    $("#project_en").val(result["datas"]["project_en"]);
    $("#project_domain").val(result["datas"]["project_domain"]);
    $("#project_status").val(result["datas"]["project_status"]);
    $("#startDate").val(result["datas"]["startDate"]);
    $("#endDate").val(result["datas"]["endDate"]);
    $("#RC").val(result["datas"]["RC"]);
    $("#targetId").val(result["datas"]["id"]);
    }
    })
});

$("#flow_btn_search").click(function () {
    $.ajax({
        url: "/flowSearch",
        type: "get",
        data: {
            test_group: $("#test_group").find("option:selected").val(),
        }
    }).done(function (result) {
        if (result.status == "200")
        {
            var _temo = [];
            var tableHTML = "";
            for (var i = 0; i < result['datas'].length; i++) {
                tableHTML = tableHTML +
                '<tr><td style="display:none">' + result["datas"][i]["id"] +
                '</td><td style="text-align:center">' + result["datas"][i]["domain"] +
                '</td><td style="text-align:center">' + result["datas"][i]["name"] +
                '</td><td style="text-align:center">' + result["datas"][i]["desc"] +
                '</td><td style="text-align:center">' + result["datas"][i]["statu"] +
                '</td><td style="text-align:center">' + result["datas"][i]["test_group"] + '</td>'+
                '</td><td style="text-align: center;vertical-align:middle">' +
                    '<a data-pid="' + result["datas"][i]["id"] + '" class="btn btn-primary btn-large update">修改</a>'+
                    '<a data-pid="' + result["datas"][i]["id"] + '" class="btn btn-primary btn-large delete">删除</a>'+
                '</tr>';
            }
            $("#casetb").html(tableHTML);
        }
        else{
            alert(result.error);
        }
    })
});
$("body").delegate(".update", "click",function(){
    flow_id = $(this).data("pid");
    $.ajax({
        url: "/flowSingleDatas",
        type: "get",
        data: {
            flow_id: flow_id,
        }
    }).done(function (result) {
    if (result["code"]=="400"){
        alert(result["datas"]);
    }
    else{
    $('.theme-popover').toggle();
    $("#flow_id").val(result["datas"]["id"]);
    $("#flow_group").val(result["datas"]["test_group"]);
    $("#flow_name").val(result["datas"]["name"]);
    $("#flow_domain").val(result["datas"]["domain"]);
    $("#flow_desc").val(result["datas"]["desc"]);
    $("#flow_user").val(result["datas"]["user"]);
    }
    })
});
$("body").delegate(".delete","click",function(){
    flow_id = $(this).data("pid");
    $.ajax({
        url:"/flowDelete",
        type:"get",
        data:{
            flow_id:flow_id,
        }
    }).done(function (result) {
        alert(result["datas"]);
    })
})
$("#flow_btn_save").click(function (){
    var domains=[];
    $("#flow_domain option:selected").each(function() {
        domains.push($(this).val());
    });
    if (domains.length==0){
        alert("请选择功能域!");
        return;
    }
    var flow_statu=$('#flow_status option:selected').val();
    if (flow_statu=="None"){
        alert("请选择工作流状态!");
        return;
    }
    var flow_name=$("#flow_name").val();
    if (flow_name=="None"||flow_name==""){
        alert("工作流名称不能为空!");
        return;
    }
    var tester=$("#flow_user").val();
    if (tester=="None"||tester==""){
        alert("创建人员不能为空!");
        return;
    }
    flow_domain=domains.join(",");
    console.log(flow_domain);
    $.ajax({
        url: "/flowSaveUpdate",
        type: "get",
        data: {
            flow_id: $("#flow_id").val(),
            flow_name:flow_name,
            flow_domain:flow_domain,
            flow_statu:flow_statu,
            flow_desc:$("#flow_desc").val(),
            tester:tester,
        }
    }).done(function (result) {
        if (result["code"]==200){
        alert(result["datas"]);}
        else{
        alert("更新失败");
        }
    });
});