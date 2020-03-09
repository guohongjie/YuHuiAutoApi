$(function () {

            var is_save=true;
            $(document).click(function(e){
                is_save=true;
                e.stopPropagation();  //防止冒泡
            });
            //查询事件
            $("#searchSuite").click(function(e){
                var flowName = $("#file").find("option:selected")
                var suiteName = flowName.attr("text");
                var suiteId = flowName.val();
                var newSuiteDatas;
                if (suiteId=="None"){
                    return;
                 }
                $.ajax({
                    url: "/getSuiteName",
                    type: "post",
                    data: {
                        suiteName: suiteName,
                        suiteId: suiteId
                        },
                    success: function (returndata) {
                          newSuiteDatas = "";
                          newSuiteDatas =  JSON.parse(returndata);
                          console.log(newSuiteDatas);
                            $('#myflow').myflow(
                            {
                                restore:
                               eval("("+newSuiteDatas+")"),
//                                {states:{rect1:{type:'start',text:{text:'开始'}, attr:{ x:427, y:214, width:48, height:48}, props:{show:{value:'开始'}}},rect2:{type:'task',text:{text:' 洪琛专属-退款申请'}, attr:{ x:498, y:355, width:100, height:50}, props:{text:{value:' 洪琛专属-退款申请'},rolename:{value:'789'}}},rect3:{type:'end',text:{text:'结束'}, attr:{ x:625, y:552, width:48, height:48}, props:{show:{value:'结束'}}}},paths:{path4:{from:'rect1',to:'rect2', dots:[],text:{text:'TO  洪琛专属-退款申请'},textPos:{x:0,y:-10}, props:{show:{value:''},xpath:{value:''}}},path5:{from:'rect2',to:'rect3', dots:[],text:{text:'TO 结束'},textPos:{x:0,y:-10}, props:{show:{value:''},xpath:{value:''}}}},props:{props:{}}},
                            });
                            $("#searchSuite").css("display","none");
                            return;
                                },
                    error: function (returndata) {
                            alert("操作失败！");
                            return;
                        }
                 });

                    });
            $('#myflow').myflow(
                    {
                        restore:
                        "",
//                        {"states":{"rect1":{"type":"start","text":{"text":"开始"},"attr":{"x":566,"y":196,"width":48,"height":48},"props":{"show":{"value":"开始"}}},"rect2":{"type":"task","text":{"text":" queryMyOpusComment.htm"},"attr":{"x":568,"y":380,"width":100,"height":50},"props":{"text":{"value":" queryMyOpusComment.htm"},"rolename":{"value":"11"}}},"rect3":{"type":"end","text":{"text":"结束"},"attr":{"x":731,"y":591,"width":48,"height":48},"props":{"show":{"value":"结束"}}}},"paths":{"path4":{"from":"rect1","to":"rect2","dots":[],"text":{"text":"TO  queryMyOpusComment.htm"},"textPos":{"x":0,"y":-10},"props":{"show":{"value":""},"xpath":{"value":""}}},"path5":{"from":"rect2","to":"rect3","dots":[],"text":{"text":"TO 结束"},"textPos":{"x":0,"y":-10},"props":{"show":{"value":""},"xpath":{"value":""}}}},"props":{"props":{}}},
                    });
            $("#delete").bind("click", function () {    //删除功能
                $(document).trigger("keydown", true);
            });

            if (true) {
                $(".readonly").hide();  //可编辑状态
            } else {
                $(".readonly").show();  //只读状态
                readonly = true            //禁止删除
            }

        });
function wctv(cur) {
        var wc = $("#getApd").find("option:selected");
        project_id = wc.val();
        projectName = wc.attr("text");
        $.ajax({
            url: "/getProjectApi",
            type: "get",
            data: {
                project_id: project_id,
                projectName: projectName,
                curPage: cur,
                },
            success: function (returndata) {
            if (returndata["total"]=="0") {
             $("#prePageApi").css("display","none");
             $("#nextPageApi").css("display","none");
            }
            else{
                    for (var i = 0; i < 10; i++) {
                              var apiId = i+1;
                              if (typeof(returndata['datas'][i])!="undefined"){
                                    $("#api_"+apiId+"").css("display","block");
                                    $("#api_"+apiId+" span").text(returndata['datas'][i][1]);
                                    $("#api_"+apiId).attr("value",returndata['datas'][i][0]);
                                    $("#api_"+apiId+" p").text(returndata['datas'][i][2]);
                                    var has_next = returndata['has_next']    //判断是否存在下一页
                                    var has_prev = returndata['has_prev']    //判断是否存在上一页
                                    if (has_next==true)
                                    {
                                    $("#nextPageApi").css("display","block");
                                    }
                                    else {
                                    $("#nextPageApi").css("display","none");
                                    }
                                    if (has_prev==true) {
                                    $("#prePageApi").css("display","block");
                                    }
                                    else
                                    {
                                    $("#prePageApi").css("display","none");
                                    }
                                    }
                               else{
                                    $("#api_"+apiId+"").css("display","none");

                                    }
                        }
                 }
                        },
            error: function (returndata) {
                    alert("操作失败！");
                    return;
                }
         })
};
function displayDescription(obj){
    var api_id=obj.attributes.value.value;
    $.ajax({
                    url: "/getApiDesc",
                    type: "get",
                    data: {
                        api_id: api_id,
                        },
                    success: function (returndata) {
                        $("#api_discript").css("display","block");
                        $("#api_discriptLook p").text(returndata["datas"]);
                        },
                    error: function (returndata) {
                            alert("查询失败");
                        }
                 });
}
function displayClose() {
  $('#testDiv').css("display","none");
  $("#testResult").text("");
  $("#helpDiv").css("display","none");
  $("#get_params").css("display","none");
    $("#resp_value").text("");
    $("#api_discript").css("display","none");
    $("#api_discriptLook p").text("");
}
function displaySearchFlow(){
//    $("#searchSuite").css("display","block");
    window.location.reload();
}
function newSuiteName(){
    $(".newSuitName").toggle();
    $(".file").toggle();
    $("#searchSuite").toggle();
}
function selectProject(){
    window.location.reload();
    $("#searchSuite").css("display","block");
}
function getPassValue(){
    var key = $("#get_key").val();
     $.ajax({
                    url: "/getRedisValue",
                    type: "get",
                    data: {
                        key: key,
                        },
                    success: function (returndata) {
                        $("#resp_value").html(returndata["datas"]);
                        },
                    error: function (returndata) {
                            alert("查询失败");
                        }
                 });
}
function displayHelp(){

    $("#helpDiv").toggle();
}
function displayGetParams(){

    $("#get_params").toggle();
}
function deleteSuite(){
    var name= window.confirm("确定要删除当前流程吗?")
  if (name)
  {
    var flowName = $("#file").find("option:selected")
    var suiteId = flowName.val();
    $.ajax({
                    url: "/deleteSuite",
                    type: "get",
                    data: {
                        suiteId: suiteId,
                        },
                    success: function (returndata) {
                        alert("删除成功");
                        window.location.reload();
                        },
                    error: function (returndata) {
                            alert("删除失败");
                        }
                 });
    }

}
function nextPage(){
    var curPageIndex = parseInt($("#curPageApi").text())+1;
    $("#curPageApi").text(curPageIndex);
    wctv(curPageIndex);
}
function prePage(){
    var curPageIndex = parseInt($("#curPageApi").text())-1;
     $("#curPageApi").text(curPageIndex);
    wctv(curPageIndex);
}
function closeDesc(){
    $("#api_discript").css("display","none");
}
