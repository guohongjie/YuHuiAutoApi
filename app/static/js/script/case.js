var get_title="<tr height=\"36px\"> \n" +
    "       <th colspan=\"3\" width=\"20%\" class=\"wctv\">Params(参数）</th>\n" +
    "       <th colspan=\"3\" width=\"20%\" class=\"wctv\">Headers(标头)</th>\n" +
    "       <th colspan=\"2\" width=\"20%\" class=\"wctv\">Cookies(缓存)</th>\n" +
    "      </tr>";
var get_data="<tr height=\"36px\">\n" +
    "<td colspan=\"3\" class=\"wctv\"><input maxlength=\"900000000\" style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"get_params\" placeholder=\"测试数据\" \n" +
    "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='测试数据'\"></td>\n" +
    "<td colspan=\"3\" class=\"wctv\"><input maxlength=\"900000000\" style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"get_headers\" placeholder=\"Headers\" \n" +
    "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='Headers'\"></td>\n" +
    "<td colspan=\"2\" class=\"wctv\"><input maxlength=\"900000000\" style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"get_cookies\" placeholder=\"Cookies\" \n" +
    "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='Cookies'\"></td>\n" +
    "</tr>"


var post_title="<tr height=\"36px\"> \n" +
    "       <th colspan=\"3\" width=\"20%\" style=\"text-align:center;\"  class=\"wctv\">Data(参数）</th>\n" +
    "       <th colspan=\"3\" width=\"20%\" style=\"text-align:center;\" class=\"wctv\">Headers(标头)</th>\n" +
    "       <th colspan=\"2\" width=\"15%\" style=\"text-align:center;\" class=\"wctv\">Cookies(缓存)</th>\n" +
    "      </tr>";

var post_data="<tr height=\"36px\">\n" +
    "<td colspan=\"3\" class=\"wctv\"><input maxlength=\"900000000\" style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"post_params\" placeholder=\"测试数据\" \n" +
        "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='测试数据'\"></td>\n" +
    "<td colspan=\"3\" class=\"wctv\"><input maxlength=\"900000000\" style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"post_headers\" placeholder=\"Headers\" \n" +
        "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='Headers'\"></td>\n" +
    "<td colspan=\"2\" class=\"wctv\"><input maxlength=\"900000000\" style=\"width: 100%; height: 100%\" type=\"text\" value=\"None\" id=\"post_cookies\" placeholder=\"Cookies\" \n" +
        "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='Cookies'\"/></td>\n" +
    "</tr>"

var file_data ="<tr height=\"36px\"> \n" +
    "       <th colspan=\"3\" style=\"text-align:center;\">file_desc(备注）</th>\n" +
    "       <th colspan=\"5\" style=\"text-align:center;\" >上传文件</th>\n" +
        "<tr height=\"36px\">\n" +
    "<td colspan=\"3\" class=\"wctv\"><input maxlength=\"900000000\" style=\"width: 100%; height: 100%\" type=\"text\" value=\"file\" id=\"file_desc\" placeholder=\"file_desc\" \n" +
        "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='file_desc'\"></td>\n" +
        "<td colspan=\"2\" class=\"wctv\"><input style=\"width: 100%; height: 100%\" type=\"file\" id=\"FileUpload\" placeholder=\"FileUpload\" name=\"FileUpload\" \n" +
        "onfocus=\"this.placeholder=''\" onblur=\"this.placeholder='FileUpload'\"></td>\n" +
        "<td colspan=\"2\" class=\"wctv\"><button class=\"btn btn-default\" onclick=\"btn_upload()\">上传</button><button class=\"btn btn-default\" onclick=\"btn_clear()\">清空</button></td>\n" +
    "</tr>"



$("#btn2").click(function () {
    if ($("#casetb").html()!=""){
        $(".schedule").css("display","none");
    };
    var curPageIndex = 1;
    $(".pagination").css("display","inline-block");
//    var isSelfGroup=$("#project").attr("name") //获取选中的项
//    if (isSelfGroup=="测试项目_1"){
//        searchApi(curPageIndex);}
//    else{
//        var option=$("#project option:selected").val();
//        if(option=="None"){
//            alert("请至少选择一项测试项目");
//        }else{
            searchApi(curPageIndex);
//        }
//    }
     $(".theme-schedule").css("display","block");
    });
$("#btn_schedule_save").click(function () {
    var api_pid = $("#schedule_targetId").val();
    var case_api = $("#schedule_case_api").val();
    var params = $("#schedule_params").val();
    var status = $("#schedule_status").val();
    var assertValue = $("#schedule_assertValue").val();
    $.ajax({
            url: "/saveHttpSchedule",
            type: "get",
            data: {
                api_pid: api_pid,
                case_api: case_api,
                status: status,
                params: params,
                assertValue: assertValue
            }
        }).done(function (result) {
            alert(result);
        })
});
$("#button_schedule").click(function() {
    var checkbox = $('input[class="check_box"]:checked');
    if (checkbox.length==0){
        alert("请勾选调度用例");}
    else{
        start_long_task();
//        checkSchedule();
    }
});
$('.theme-popover-runScheduleTest .close').click(function () {

        $('.theme-popover-runScheduleTest').fadeOut(100);
        $("#progressing").html("");
        });
$("#prePageApi").click(function () {
    if ($("#casetb").html()!=""){
        $(".schedule").css("display","none");
    };
    var curPageIndex = parseInt($("#curPageApi").text())-1;
    searchApi(curPageIndex);
    });
$("#nextPageApi").click(function () {
    if ($("#casetb").html()!=""){
        $(".schedule").css("display","none");
    };
    var curPageIndex = parseInt($("#curPageApi").text())+1;
    searchApi(curPageIndex);
    });
$("#CheckAll").bind("click",function(){
   if (this.checked){
      $("input[class='check_box']").each(function(){
            this.checked = true;
            })
              }
      else {
      $("input[class='check_box']").each(function(){
            this.checked = false;
            })
            }
 });
//获取 select=使用 的option
var func = function () {
        $.ajax({
        url: "/condition",
        type: "get",
        data: {
            project: $("#project option:selected").text()
        }
    }).done(function (result) {
        var selectHTML = ""
        for (var i = 0; i < result.condition.length; i++) {
            selectHTML = selectHTML + '<option value="">' + result.condition[i] + '</option>'
        }
        $("#api_name").html(selectHTML);
    })
}
jQuery(document).ready(function ($) {
    $('.theme-login').click(function () {
        $('.theme-popover-mask').fadeIn(100);
        $("#RS").html("");
        $("#RC").html("");
        $("#project_choice").val("");
        $("#targetId").val(999999999)
        $("#case_api").val("");
        $("#case_desc").val("");
        $("#case_url").val("");
        $("#method").val("");
        $("#key").val("");
        $("#except_result").val("");
        //$("#btn4").css("display","none");
        $("#actual_result").val("");
        $("#actual_result").attr("readOnly","true");
        $("#actual_result").removeAttr("style");
        $('.theme-popover').slideDown(200);
        $("#btn4").bind("click",http_test);
    });
    $('.theme-poptit .close').click(function () {
        $('.theme-popover-mask').fadeOut(100);
        $('.theme-popover').slideUp(200, function () {
            var _td = $("#tbdata").find("td");
            $("#btn4").unbind("click");
            $("#btn6").unbind("click");
            $("#btn7").unbind("click");
        });
    });
    $('.theme-poptit-schedule .close').click(function () {

    $('.theme-popover-schedule').fadeOut(100);
    });
    $(".theme-popover-apiCopy .close").click(function() {
        $(".theme-popover-apiCopy").fadeOut(100);
    });
    $("body").delegate(".update", "click", function () {
    $("#btn4").bind("click",http_test);
                $td = $(this).parents("tr").find("td");
                // alert("===" + $(this).data("pid"));
                var api_pid = $td.eq(1).text();  //获取用例id
                $('.theme-popover-mask').fadeIn(100);
                $('.theme-popover').slideDown(200, function () {
                var project=$td.eq(2).text();
                var case_api=$td.eq(3).text();
                httpUnionSearch(project,case_api,api_pid);
                });
        });//打开新增数据弹层
    $("body").delegate(".ci_schedule","click", function () {
        $('.theme-popover-schedule').fadeIn(100);
        $td = $(this).parents("tr").find("td");
        var api_pid = $td.eq(1).text();
        var case_api = $td.eq(3).text();
        $("#schedule_targetId").val(api_pid);
        $("#schedule_case_api").val(case_api);
         $.ajax({
            url: "/searchHttpSchedule",
            type: "get",
            data: {
                api_pid: api_pid,
                case_api: case_api
            }
        }).done(function (result) {
        if (result['count']=="0") {
            alert("接口未创建集成调度!");
            }
        else {
            $("#schedule_params").val(result['data']['params']);
            $("#schedule_params").val(result['data']['status']);
            $("#schedule_assertValue").val(result['data']['assertValue']);
            };
        })
    });
    $("#btn1").bind("click",save_http_data);
    $('.theme-schedule').click(function () {
        $(".schedule").toggle(100);
        $(".check_box").toggle(100);
    });
    $("body").delegate(".api_copy","click",function () {
    $(".theme-popover-apiCopy").fadeIn(100);
    $td = $(this).parents("tr").find("td");
    var api_pid = $td.eq(1).text();
    $("#copy_chedule_targetId").val(api_pid);
    var case_name = $td.eq(3).text();
    $("#copy_api_name").val(case_name);
    });
    $(function () {

        displayScheduleButton();
    });
});

$("#btn5").click(function () {
    var case_host=$("#case_host").val();
    var case_url=$("#case_url").val();
    var method=$("#method").find("option:selected").val();
    var pid=$("#targetId").val();
    //alert(pid);
    var api_data=$("#get_params").val();
    var api_headers=$("#get_headers").val();
    var api_cookies=$("#get_cookies").val();
    var except_result=$("#except_result").val();
    if (pid==""||pid=="999999999"){
        //alert("/mock"+case_url);
        $.ajax({
            url: "/mock"+case_url,
            type: "post",
            data: {
                method: method,
                params: api_data,
                headers: api_headers,
                cookies: api_cookies,
            }
        }).done(function (result) {
                  alert(except_result);
               // $("#RS").html("");
                $("#RS").html(except_result);
                })
                }
    else{
        //alert(api_redirects)
        $.ajax({
            url: "/mock"+case_url,
            type: "post",
            data: {
                method: method,
                params: api_data,
                headers: api_headers,
                cookies: api_cookies,
                id: pid,
            }
        }).done(function (result) {
                alert(result);
               // $("#RS").html("");
                $("#RS").html(result);
                }
       );}
});
$("#copy_btn").click(function () {
    var api_pid = $("#copy_chedule_targetId").val();
    var case_api = $("#copy_api_name").val();
    var copy_project_choice = $("#copy_project_choice").find("option:selected").val();
    var copy_test_env = $("#copy_test_env").find("option:selected").val();
    if (copy_project_choice=="None" ||copy_test_env=="None") {
        alert("项目或环境不能为默认值!");
    }
    else{
        $.ajax({
            url: "/httpCopy",
            type: "get",
            data: {
            pid: api_pid,
            case_api: case_api,
            copy_project_choice: copy_project_choice,
            copy_test_env: copy_test_env
                    }
        }).done(function (result){
                alert(result.datas);
        });
        }
});
$("body").delegate(".delet","click", function(){
    $td = $(this).parents("tr").find("td");
    var api_pid = $td.eq(1).text();
    var status = $td.eq(6).text();
    if (status=="通过"){
        case_status = 1;
        $.ajax({
        url: "/httpStatus",
        type: "get",
        data:{
            pid: api_pid,
            status:case_status
            }}).done(function(result){
                    if (result.code == "200"){
                        alert(result.datas);
                        $td.eq(6).html('<a data-pid="0" class="delet" style="background-color:red">失败</a>');
                        }
                    else{
                        alert(result.datas);
                       }
                });
    }
    else{
        case_status = 0;
        $.ajax({
        url: "/httpStatus",
        type: "get",
        data:{
            pid: api_pid,
            status:case_status
            }}).done(function(result){
                    if (result.code == "200"){
                        alert(result.datas);
                        $td.eq(6).html('<a data-pid="0" class="delet" style="background-color:green">通过</a>');
                        }
                    else{
                        alert(result.datas);
                       }
                });
    }
    //alert(status);
});
$("body").delegate(".delete","click", function(){
    $td = $(this).parents("tr").find("td");
    var api_pid = $td.eq(1).text();
    var project = $td.eq(2).text();
    var case_api = $td.eq(3).text();
        $.ajax({
        url: "/httpDelete",
        type: "get",
        data:{
            pid: api_pid,
            project:project,
            case_api:case_api
            }}).done(function(result){
                    if (result.code == "200"){
                        alert(result.datas);
                        var curPageIndex = 1;
                        searchApi(curPageIndex);
                        }
                    else{
                        alert(result.datas);
                       }
                });
});
$("#check1").change(function(){
 var scheduling=$("#check1").is(':checked');
 if (scheduling==true){
  $("#assert").attr('disabled',false);
 // $("#test_suite").attr('disabled',false);
 }
 else{
  $("#assert").attr('disabled',true);
 // $("#test_suite").attr('disabled',true);
 };
});
$("#check2").change(function(){
 var scheduling=$("#check2").is(':checked');
 if (scheduling==true){
  $("#account_project").attr('disabled',false);
  $("#account_username").attr('disabled',false);
  $("#account_passwd").attr('disabled',false);
 }else{
  $("#account_project").attr('disabled',true);
  $("#account_username").attr('disabled',true);
  $("#account_passwd").attr('disabled',true);
//   $("#account_project").val("None");
  $("#account_project").find("option[value='']").prop("selected",true);
  $("#account_username").val("None");
  $("#account_passwd").val("None");
 };});
$("#check3").change(function(){
var upload_file=$("#check3").is(":checked");
if (upload_file==true){
    $("#btn4").unbind("click");  //取消btn4 运行测试点击事件
    $("#btn4").attr("id","btn6");　　//更改id=btn6(运行测试按钮)
    $("#btn6").bind("click",http_upload_test);  //btn6添加http_upload_test运行测试功能事件
    $("#apt_others").append(file_data);  //添加上传文件input 框

    $("#btn1").unbind("click");  //取消btn1 保存数据点击事件
    $("#btn1").attr("id","btn7");
    $("#btn7").bind("click",save_file_data);
}
else{
$("#btn6").unbind("click");　　//取消btn6绑定事件
$("#btn6").attr("id","btn4");　　//更改id=btn4(运行测试按钮)
$("#btn4").bind("click",http_test);  //btn4添加http_test运行测试功能事件
$("#apt_others").html("");  //清空上传文件input 框

$("#btn7").unbind("click");  //保存按钮解除保存文件事件
$("#btn7").attr("id","btn1");　　//id=btn1
$("#btn1").bind("click",save_http_data);  //btn1添加保存数据事件
};
});
$("#check_assert").change(function(){
    var scheduling=$("#check_assert").is(':checked');
 if (scheduling==true){
  $("#assert_value").attr('disabled',false);
 }else{
  $("#assert_value").attr('disabled',true);
   $("#assert_value").val("None");
 };});
$(document).ready(changeAPIparams ());
function changeAPIparams(){
  $("#method").bind("change",function(){
    var _ad = $("#apt_datas").find("td");
        var params = _ad.eq(0).find("input").val();
        var headers = _ad.eq(1).find("input").val();
        var cookies = _ad.eq(2).find("input").val();
    if($(this).val()=="GET"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append(get_title);
        $("#apt_datas").append(get_data);
            $("#get_params").val(params);
            $("#get_headers").val(headers);
            $("#get_cookies").val(cookies);
    }
    else if($(this).val()=="POST"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
            $("#apt_title").append(post_title);
            $("#apt_datas").append(post_data);
            $("#post_params").val(params);
            $("#post_headers").val(headers);
            $("#post_cookies").val(cookies);
    }
    else if ($(this).val()=="HEAD"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第HEAD行</td></tr>");
        $("#apt_datas").append("<tr><td>第HEAD行</td></tr>");
    }
    else if ($(this).val()=="PUT"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第PUT行</td></tr>");
        $("#apt_datas").append("<tr><td>第PUT行</td></tr>");
     }
    else if ($(this).val()=="DELETE"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第DELETE行</td></tr>");
        $("#apt_datas").append("<tr><td>第DELETE行</td></tr>");
     }
    else if ($(this).val()=="OPTIONS"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第OPTIONS行</td></tr>");
        $("#apt_datas").append("<tr><td>第OPTIONS行</td></tr>");
     }
    else if ($(this).val()=="PATCH"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第PATCH行</td></tr>");
        $("#apt_datas").append("<tr><td>第PATCH行</td></tr>");
      }
    else {
        $("#apt_title").html("");
        $("#apt_datas").html("");
    }
  });
};
function initAPIparams(params,method){
    if(method=="GET"){
    $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append(get_title);
        $("#apt_datas").append(get_data);
        $("#get_params").val(params);
    }
    else if(method=="POST"){
        $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append(post_title);
        $("#apt_datas").append(post_data);
        $("#post_params").val(params);
    }
    else if (method=="HEAD"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第HEAD行</td></tr>");
        $("#apt_datas").append("<tr><td>第HEAD行</td></tr>");
    }
    else if (method=="PUT"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第PUT行</td></tr>");
        $("#apt_datas").append("<tr><td>第PUT行</td></tr>");
     }
    else if (method=="DELETE"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第DELETE行</td></tr>");
        $("#apt_datas").append("<tr><td>第DELETE行</td></tr>");
     }
    else if (method=="OPTIONS"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第OPTIONS行</td></tr>");
        $("#apt_datas").append("<tr><td>第OPTIONS行</td></tr>");
     }
    else if (method=="PATCH"){
         $("#apt_title").html("");
         $("#apt_datas").html("");
        $("#apt_title").append("<tr><td>第PATCH行</td></tr>");
        $("#apt_datas").append("<tr><td>第PATCH行</td></tr>");
      }
    else {
        $("#apt_title").html("");
        $("#apt_datas").html("");
    }
};
function addThreeTheam(theamClass){
var classProprety = theamClass;
 var cookies_html = "<div class=\"useBtnSaveParams add-"+classProprety+" cform\"><table id=\""+ classProprety +"Title\" border=\"5\" width=\"100%\"\n" +
                    "class=\"CSSearchTbl\" cellpadding=\"0\" cellspacing=\"0\">\n" +
                    "<tbody><tr><th style=\"width: 50%; height: 50%\">KEY</th>\n" +
                    "<th style=\"width: 50%; height: 50%\">VALUE</th></tr>\n" +
                    "</tbody><tbody id=\""+classProprety+"Value\"></tbody></table></div>\n" +
                    "<div class=\"btnDivBtn\">\n" +
                    "<button class=\"btn btn-default btnParamsSaveAdd "+classProprety+"Add\" onclick=\"addProprety('precondition')\">+</button>\n"+
                    "<button class=\"btn btn-default btnParamsSaveSub "+classProprety+"Sub\" onclick=\"subProprety('precondition')\">-</button>\n"+
                    "<button class=\"btn btn-default btnParamsSaveSave "+classProprety+"Save\" onclick=\"saveValues('"+classProprety+"Value','"+classProprety+"')\">Save</button></div>"
 $("."+classProprety).append(cookies_html);
 $("."+classProprety).css('display','block');
};
function saveValues(id,saveId){
  var datadict = new Object;
  var tb = document.getElementById(id);
  var rows = tb.rows;
  for (var i=0;i<rows.length;i++){
      datadict[rows[i].cells[0].childNodes[0].value]=rows[i].cells[1].childNodes[0].value;}
    //console.log(datadict);
  var date = JSON.stringify(datadict);
  console.log(date);
  $("#"+saveId).val(date);
  alert('数据保存成功');
  $(".theme-cookies").remove();
  //$(".theme-cookies").css('display','none');
};
function addProprety(classProprety) {
        $("#"+classProprety+"Value"
        ).append("<tr><td><input value=\"\" style=\"width: 100%; height: 100%\"></td><td><input value=\"\" style=\"width: 100%; height: 100%\"/></td></tr>");
};
function subProprety(classProprety) {
        $("#"+classProprety+"Value tr"
        ).eq(-1).remove();
};
function http_test () {
    var case_host=$("#case_host").val();
    var case_url=$("#case_url").val();
    var method=$("#method").find("option:selected").val();
    var islogin=$("#check2").is(':checked');
    var account_project=$("#account_project").find("option:selected").val();
    var account_username=$("#account_username").val();
    var account_passwd=$("#account_passwd").val();
    var project_cn=$("#project_choice").val();
    if (method=="GET"){
        var api_data=$("#get_params").val();
        var api_headers=$("#get_headers").val();
        var api_cookies=$("#get_cookies").val();
        $.ajax({
            url: "/case_http_test",
            type: "post",
            data: {
                case_host: case_host,
                case_url: case_url,
                method: method,
                params: api_data,
                headers: api_headers,
                cookies: api_cookies,
                islogin: islogin,
                account_project:account_project,
                account_username:account_username,
                account_passwd: account_passwd,
                project_cn:project_cn
            }
        }).done(function (result) {
            if (result.code == "200")
            {
                if (islogin){
                    alert("登录信息:"+result.login_msg+"\n"+result.test_datas);
                    var text = "登录信息:\n      登录项目:"+account_project+'\n'+"      登录账号:"+account_username+
                            "\n"+"      登录状态:"+result.login_msg+
                            '\n'+"接口测试信息:"+"\n"+ "      请求返回:"+"\n"+result.test_datas;
                    $("#RS").html(text);
                }
                else{
                    alert(result.test_datas);
                    var text = "接口测试信息:"+"\n"+ "      请求返回:"+"\n"+result.test_datas;
                    $("#RS").html(text);
                }

              }
            else{
                if (islogin){
                    alert("登录信息:"+result.login_msg+"\n"+result.test_datas);
                    var text = "登录信息:\n      登录项目:"+account_project+'\n'+"      登录账号:"+account_username+
                            "\n"+"      登录状态:"+result.login_msg+
                            '\n'+"接口测试信息:"+"\n"+ "      请求返回:"+"\n"+result.test_datas;
                    $("#RS").html(text);
                }
                else{
                    alert(result.test_datas);
                    var text = "接口测试信息:"+"\n"+ "      请求返回:"+"\n"+result.test_datas;
                    $("#RS").html(text);
                }
                }
        });}
    else if (method=="POST") {
        var api_data = $("#post_params").val();
        var api_headers = $("#post_headers").val();
        var api_cookies = $("#post_cookies").val();
        $.ajax({
            url: "/case_http_test",
            type: "post",
            data: {
                case_host: case_host,
                case_url: case_url,
                method: method,
                params: api_data,
                headers: api_headers,
                cookies: api_cookies,
                islogin: islogin,
                account_project:account_project,
                account_username:account_username,
                account_passwd: account_passwd,
                project_cn:project_cn
            }
        }).done(function (result) {
            if (result.code == "200")
            {
                if (islogin){
                    alert("登录信息:"+result.login_msg+"\n"+result.test_datas);
                    var text = "登录信息:\n      登录项目:"+account_project+'\n'+"      登录账号:"+account_username+
                            "\n"+"      登录状态:"+result.login_msg+
                            '\n'+"接口测试信息:"+"\n"+ "      请求返回:"+"\n"+result.test_datas;
                    $("#RS").html(text);
                }
                else{
                    alert(result.test_datas);
                    var text = "接口测试信息:"+"\n"+ "      请求返回:"+"\n"+result.test_datas;
                    $("#RS").html(text);
                }
              }
            else{
                if (islogin){
                    alert("登录信息:"+result.login_msg+"\n"+result.test_datas);
                    var text = "登录信息:\n      登录项目:"+account_project+'\n'+"      登录账号:"+account_username+
                            "\n"+"      登录状态:"+result.login_msg+
                            '\n'+"接口测试信息:"+"\n"+ "      请求返回:"+"\n"+result.test_datas;
                    $("#RS").html(text);
                }
                else{
                    alert(result.test_datas);
                    var text = "接口测试信息:"+"\n"+ "      请求返回:"+"\n"+result.test_datas;
                    $("#RS").html(text);
                }
                }
        });}
};
function http_upload_test() {
               var fileObj = document.getElementById("FileUpload").files[0]; // js 获取文件对象
               if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
                   alert("请选择文件");
                   return;
               }
               var formFile = new FormData();
               var file_desc = $("#file_desc").val()
               formFile.append("action", "UploadVMKImagePath");
               formFile.append("file", fileObj); //加入文件对象
               var data_flie = formFile;

               var case_host=$("#case_host").val();
                var case_url=$("#case_url").val();
                var method=$("#method").find("option:selected").val();
            if (method=="GET"){
                var api_data=$("#get_params").val();
                var api_headers=$("#get_headers").val();
                var api_cookies=$("#get_cookies").val();
                var project_cn=$("#project_choice").val();
                var islogin=$("#check2").is(':checked');
                var account=$("#account").val();
                   data_flie.append("project_cn",project_cn);
                    data_flie.append("case_host",case_host);
                    data_flie.append("case_url",case_url);
                    data_flie.append("method",method);
                    data_flie.append("params",api_data);
                    data_flie.append("headers",api_headers);
                    data_flie.append("cookies",api_cookies);
                    data_flie.append("islogin",islogin);
                    data_flie.append("account",account);
                    data_flie.append("file_desc",file_desc);
               $.ajax({
                        url: "/test_upload",
                        type: "post",
                        data: data_flie,
                        dataType: "json",
                        cache: false,//上传文件无需缓存
                        processData: false,//用于对data参数进行序列化处理 这里必须false
                        contentType: false, //必须
                    }).done(function (result) {
                    if (result.code == "200")
                    {var wc = result.datas;
                        alert(wc);
                       // $("#RS").html("");
                        $("#RS").html(wc);
                      }
                    else{alert(result.code,result.datas);}
                });}
            else if (method=="POST") {
                    var api_data = $("#post_params").val();
                    var api_headers = $("#post_headers").val();
                    var api_cookies = $("#post_cookies").val();
                    var project_cn=$("#project_choice").val();
                    var islogin=$("#check2").is(':checked');
                    var account=$("#account").val();
                    //alert(api_redirects)
                    data_flie.append("params",api_data);
                    data_flie.append("project_cn",project_cn);
                    data_flie.append("case_host",case_host);
                    data_flie.append("case_url",case_url);
                    data_flie.append("method",method);
                    data_flie.append("params",api_data);
                    data_flie.append("headers",api_headers);
                    data_flie.append("cookies",api_cookies);
                    data_flie.append("islogin",islogin);
                    data_flie.append("account",account);
                    data_flie.append("file_desc",file_desc);
                    $.ajax({
                        url: "/test_upload",
                        type: "post",
                        data: data_flie,
                        dataType: "json",
                        cache: false,//上传文件无需缓存
                        processData: false,//用于对data参数进行序列化处理 这里必须false
                        contentType: false, //必须
                    }).done(function (result) {
                        if (result.code == "200")
                        {var wc = result.datas;
                            alert(wc);
                           // $("#RS").html("");
                            $("#RS").html(wc);
                        }
                        else{alert(result.code,result.datas);}
                    });}
               };
function save_http_data () {
        var _case = [];
        var islogin=$("#check2").is(":checked");
        var account_project=$("#account_project").find("option:selected").val();;
        var check_assert=$("#check_assert").is(":checked");
        var assert_value=$("#assert_value").val();
        if (islogin==true && (account_project==''||account_project=='None')){
            alert("勾选登录状态后请填写登录程序");
        }
        else{
            $("#tbdata tr").each(function () {
            var tr = $(this);
            _case.push({
                project: $("#project_choice").find("option:selected").val(),
                case_api: $("#case_api").val(),
                case_desc: $("#case_desc").val(),
                case_host: $("#case_host").val(),
                case_url: $("#case_url").val(),
                method: $("#method").find("option:selected").val(),
                except_result: $("#except_result").val(),
                scheduling: $("#check1").is(':checked'),
                islogin: $("#check2").is(':checked'),
                assert: $("#assert").val(),
                account: $("#account").val(),
                //test_suite: $("#test_suite").val(),

            });
        });
        if ($("#targetId").val()!= "999999999" ) {
            //数据更新
            //alert(_case[0].method);
            if (_case[0].method=="GET"){
            $.ajax({
                url: "/httpUpdate",
                type: "post",
                data: {
                    pid: $("#targetId").val(),
                    project: _case[0].project,
                    case_api: _case[0].case_api,
                    description: _case[0].case_desc,
                    case_host: _case[0].case_host,
                    case_url: _case[0].case_url,
                    method: _case[0].method,
                    response: _case[0].except_result,
                    params: $("#get_params").val(),
                    headers: $("#get_headers").val(),
                    cookies: $("#get_cookies").val(),
                    islogin: $("#check2").is(':checked'),
                    account_project: $("#account_project").find("option:selected").val(),
                    account_username: $("#account_username").val(),
                    account_passwd: $("#account_passwd").val(),
                    check_assert: check_assert,
                    assert_value: assert_value,
                }}).done(function (result){
                    if (result.code == "200"){
                        alert(result.datas);
                        var curPageIndex = 1;
                        searchApi(curPageIndex);
                        }
                    else{
                        alert(result.datas);
                       }
                });
                }
            else if (_case[0].method=="POST"){
                $.ajax({
                url: "/httpUpdate",
                type: "post",
                data: {
                    pid: $("#targetId").val(),
                    project: _case[0].project,
                    case_api: _case[0].case_api,
                    description: _case[0].case_desc,
                    case_host: _case[0].case_host,
                    case_url: _case[0].case_url,
                    method: _case[0].method,
                    response: _case[0].except_result,
                    params: $("#post_params").val(),
                    headers: $("#post_headers").val(),
                    cookies: $("#post_cookies").val(),
                    islogin: $("#check2").is(':checked'),
                    account_project: $("#account_project").find("option:selected").val(),
                    account_username: $("#account_username").val(),
                    account_passwd: $("#account_passwd").val(),
                    check_assert: check_assert,
                    assert_value: assert_value,
                }
            }).done(function(result){
                    if (result.code == "200"){
                        alert(result.datas);
                        var curPageIndex = 1;
                        searchApi(curPageIndex);
                        }
                    else{
                        alert(result.datas);
                       }
                });
            }
        } else {
            //数据新增
            if (_case[0].method=="GET"){
            $.ajax({
                url: "/httpInsert",
                type: "post",
                data: {
                    pid: $("#targetId").val(),
                    project: _case[0].project,
                    case_api: _case[0].case_api,
                    description: _case[0].case_desc,
                    case_host: _case[0].case_host,
                    case_url: _case[0].case_url,
                    method: _case[0].method,
                    response: _case[0].except_result,
                    params: $("#get_params").val(),
                    headers: $("#get_headers").val(),
                    cookies: $("#get_cookies").val(),
                    islogin: $("#check2").is(':checked'),
                    account_project: $("#account_project").find("option:selected").val(),
                    account_username: $("#account_username").val(),
                    account_passwd: $("#account_passwd").val(),
                    check_assert: check_assert,
                    assert_value: assert_value,
                               }
            }).done(function(result){
                    if (result.code == "200"){
                        alert(result.datas);
                        var curPageIndex = 1;
                        searchApi(curPageIndex);
                        }
                    else{
                        alert(result.datas);
                       }
                });;
                }
            else if (_case[0].method=="POST"){
                $.ajax({
                url: "/httpInsert",
                type: "post",
                data: {
                    pid: $("#targetId").val(),
                    project: _case[0].project,
                    case_api: _case[0].case_api,
                    description: _case[0].case_desc,
                    case_host: _case[0].case_host,
                    case_url: _case[0].case_url,
                    method: _case[0].method,
                    response: _case[0].except_result,
                    params: $("#post_params").val(),
                    headers: $("#post_headers").val(),
                    cookies: $("#post_cookies").val(),
                    islogin: $("#check2").is(':checked'),
                    account_project: $("#account_project").find("option:selected").val(),
                    account_username: $("#account_username").val(),
                    account_passwd: $("#account_passwd").val(),
                    check_assert: check_assert,
                    assert_value: assert_value,
                }
            }).done(function(result){
                    if (result.code == "200"){
                        alert(result.datas);
                        var curPageIndex = 1;
                        searchApi(curPageIndex);
                        }
                    else{
                        alert(result.datas);
                       }
                });
            };}
            }
        };
function save_file_data () {
    save_http_data();  //保存接口测试数据
    var project=$("#project_choice").find("option:selected").val();
    var case_api=$("#case_api").val();
    var case_desc=$("#case_desc").val();
    var case_host=$("#case_host").val();
    var case_url=$("#case_url").val();
    var method=$("#method").find("option:selected").val();
    var file_desc=$("#file_desc").val();
    var targetId=$("#targetId").val();
    var fileObj = document.getElementById("FileUpload").files[0]; // js 获取文件对象
    if (typeof (fileObj) == "undefined" || fileObj.size <= 0) {
        alert("请选择文件");
        return;}
    var formFile = new FormData();
    var file_desc = $("#file_desc").val()
    formFile.append("action", "UploadVMKImagePath");
    formFile.append("file", fileObj); //加入文件对象
    formFile.append("project",project);
    formFile.append("case_api",case_api);
    formFile.append("case_desc",case_desc);
    formFile.append("case_host",case_host);
    formFile.append("case_url",case_url);
    formFile.append("method",method);
    formFile.append("file_desc",file_desc);
    formFile.append("targetId",targetId);
               var data_flie = formFile;
               $.ajax({
                        url: "/save_upload_data",
                        type: "post",
                        data: data_flie,
                        dataType: "json",
                        cache: false,//上传文件无需缓存
                        processData: false,//用于对data参数进行序列化处理 这里必须false
                        contentType: false, //必须
                    }).done(function (result) {
                        if (result.code == "200")
                        {var wc = result.datas;
                            alert(wc);
                           // $("#RS").html("");
                            $("#RS").html(wc);}
                        else{alert(result.code,result.datas);}
                    });
};
function btn_clear(){
   var file = document.getElementById("FileUpload");
     // for IE, Opera, Safari, Chrome
     if (file.outerHTML) {
         file.outerHTML = file.outerHTML;
     } else { // FF(包括3.5)
         file.value = "";
     }
   };
function searchApi(curPageIndex) {
    $.ajax({
            url: "/httpSearch",
            type: "get",
            data: {
                case_name: $("#case_name").val(),
                case_url_name: $("#case_url_name").val(),
                project: $("#project").find("option:selected").val(),
                state: $("#state").find("option:selected").val(),
                test_env: $("#test_env").find("option:selected").val(),
                test_group: $("#test_group").find("option:selected").val(),
                test_project: $("#test_project").find("option:selected").val(),
                pageDisplayCount: $("#pageDisplayCount").find("option:selected").val(),
                curPageApi: curPageIndex,
                isSelfGroup: $("#project").attr("name")
            }
        }).done(function (result)
        {
            var apiCount = result['total'] ;   //查询数量总计
            var curPageIndex = result['curPage'];    //当前页面数
            var pagesCount = result['pages']    //总页面数
            $("#curPageApi").text(curPageIndex);
            $("#totalApi").text(apiCount);
            var has_next = result['has_next']    //判断是否存在下一页
            var has_prev = result['has_prev']    //判断是否存在上一页
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
            var _temo = [];
            for (var i = 0; i < result['datas'].length; i++) {
                _temo.push(result['datas'][i]);
            }
            var tableHTML = "";
            for (var i = 0; i < _temo.length; i++) {
                var j = i + 1;
                //alert(_temo[i]);
                if (_temo[i][5]==false){    //判断为　测试通过　＝０　
                tableHTML = tableHTML +
                '<tr><td class="check_box"><input type="checkbox" class="check_box" ></td>' +
                '<td id="pid" style="display:none">' + _temo[i][0] + '</td>' +
                '<td style="text-align: center;vertical-align:middle" >' + _temo[i][1] + '</td>' +
                '<td style="text-align: center;vertical-align:middle">' + _temo[i][2] + '</td>' +
                '<td style="text-align: center;vertical-align:middle">' + _temo[i][3] + '</td>' +
                '<td style="text-align: center;vertical-align:middle">' + _temo[i][4] + '</td>' +
                '<td style="text-align:center;vertical-align:middle">' +
                    '<a data-pid="0"class="delet" style="background-color:green">通过</a></td>' +
                '<td style="text-align: center;vertical-align:middle">' +
                    '<a data-pid="' + _temo[i][0] + '" class="btn btn-primary btn-large update">修改</a>'+
                    '<a data-pid="' + _temo[i][0] + '" class="btn btn-primary btn-large delete">删除</a>'+
                    '<a data-pid="' + _temo[i][0] + '" class="btn btn-primary btn-large api_copy">复制</a>' +
                '<td style="display:none">' + _temo[i][7] + '</td>' +
                '<td style="display:none">' + _temo[i][6] + '</td>' +
                '</tr>'}
                else{
                    tableHTML = tableHTML +
                    '<tr><td class="check_box"><input type="checkbox" class="check_box" ></td>' +
                    '<td id="pid" style="display:none">' + _temo[i][0] + '</td>' +
                    '<td style="text-align: center;vertical-align:middle" >' + _temo[i][1] + '</td><td>' + _temo[i][2] + '</td>' +
                    '<td style="text-align: center;vertical-align:middle">' + _temo[i][3] + '</td><td>' + _temo[i][4] + '</td>' +
                    '<td style="text-align: center;vertical-align:middle">' +
                        '<a data-pid="1"class="delet"  style="background-color:red">失败</a></td>' +
                    '<td style="text-align: center;vertical-align:middle">' +
                        '<a data-pid="' + _temo[i][0] + '" class="btn btn-primary btn-large update">修改</a>' +
                        '<a data-pid="' + _temo[i][0] + '" class="btn btn-primary btn-large delete">删除</a>' +
                        '<a data-pid="' + _temo[i][0] + '" class="btn btn-primary btn-large api_copy">复制</a>' +
                                          '<td style="display:none">' + _temo[i][7] + '</td>' +
                    '<td style="display:none">' + _temo[i][6] + '</td>' +
                    '</tr>'
                }}//case_name+description+case_url+method+parameter+assert
            $("#casetb").html(tableHTML);
        });
};
function httpUnionSearch(project,case_api,api_pid) {
  $.ajax({
                        url: "/httpUnionSearch",
                        type: "get",
                        data:{
                            project: project,
                            case_api: case_api,
                            pid: api_pid
                        }
                    }).done(function (result){
                        var _temo = []
                        for (var i = 0; i < result['datas'].length; i++) {
                            _temo.push(result['datas'][i]);
                        }

                        changeTheme(_temo,api_pid);
                      //  initAPIparams()
                    });
};
function changeTheme(data,api_pid) {
        $("#RS").html("");
        $("#RC").html("");
        $("#actual_result").val("");
        $("#actual_result").removeAttr("style");
        $("#btn4").removeAttr("style");
        var _td = $("#tbdata").find("td");
        var _td_1 =  $("#tbdata_1").find("td");
       // alert(api_pid);
        $("#targetId").val(api_pid);
        //alert(_td.eq(0));
        _td.eq(1).find("option").attr("selected",false);    //测试项目
        _td.eq(1).find("option[value="+data[0]+"]").prop("selected",true);    //测试项目
        _td.eq(2).find("input").val(data[1]);    //接口名称
        _td.eq(3).find("input").val(data[2]);    //用例描述
        _td.eq(4).find("input").val(data[3]);    //请求Host
        _td.eq(5).find("input").val(data[4]);    //请求url
        _td.eq(6).find("option").attr("selected",false);    //method
        _td.eq(6).find("option[value="+data[5]+"]").prop("selected",true);     //method
        _td.eq(7).find("input").val(data[6]);    //预期结果
        document.getElementById("check2").checked=data[10];    //是否登录
        if (data[11]){
            $("#account_project").find("option").attr("selected",false);
            $("#account_project").find("option[value="+data[11]+"]").prop("selected",true);
        }
        else{
            $("#account_project").find("option").attr("selected",false);
            $("#account_project").find("option[value=None]").prop("selected",true);
          }//登录环境
        $("#account_username").val(data[12]);    //登录账号
        $("#account_passwd").val(data[13]);    //登录密码
        document.getElementById("check_assert").checked=data[14];
        $("#assert_value").val(data[15]);    //登录环境
        if (data[10]){
        $("#account_project").attr('disabled',false);
        $("#account_username").attr('disabled',false);
        $("#account_passwd").attr('disabled',false);
        }
        else{
        $("#account_project").attr('disabled',true);
        $("#account_username").attr('disabled',true);
        $("#account_passwd").attr('disabled',true);
        }
        if (data[15]) {
         $("#assert_value").attr('disabled',false);
        }
        else{
         $("#assert_value").attr('disabled',true);
        }
       // document.getElementById("account").value=data[13];  //account
        //alert(data[0]);
        if (data[5]=='GET'){
            //alert(_ad.eq(0));
             $("#apt_title").html(get_title);
             $("#apt_datas").html(get_data);
            var _ad = $("#apt_datas").find("td");
            _ad.eq(0).find("input").val(data[7]);
            _ad.eq(1).find("input").val(data[8]);
            _ad.eq(2).find("input").val(data[9]);
        }
        else if(data[5]=='POST'){
            //alert(_ad.eq(0));
             $("#apt_title").html(post_title);
             $("#apt_datas").html(post_data);
             var _ad = $("#apt_datas").find("td");
            _ad.eq(0).find("input").val(data[7]);
            _ad.eq(1).find("input").val(data[8]);
            _ad.eq(2).find("input").val(data[9]);
        }
        else{
            alert('wc');
        }

        $("#btn1").data("targetId", pid);
    };
function caseRun(urldata){
        var brow = $("#casefeature td").eq(2).find("option:selected").text()
        var step = [];
        var run_case = [];
        $("#casetb tr").each(function () {
            var tr = $(this);
            step.push([
                tr.find("td").eq(1).text(),
                tr.find("td").eq(2).text(),
                tr.find("td").eq(3).text(),
                tr.find("td").eq(4).text()
            ]);
            for (var i = 0; i < step.length; i++) {
                run_case[i] = step[i]
            }
        });
        var email = "";
        var emailmatch = "";
        if ($("#emailadrr").val() !== "") {
            emailmatch = $("#emailadrr").val(); 
            if(!emailmatch.match(/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/))
              {
                alert("格式不正确！请重新输入");
                $("#emailadrr").focus();
                return;
              }else{
                email = $("#emailadrr").val();
              }
        }
        $.ajax({
            url: urldata + "/case_run",
            type: "post",
            data: {
                brow: brow,
                case: JSON.stringify(run_case),
                url: urldata,
                email: email
            }
        });
        var loopfn = function () {
            $.ajax({
                url: urldata + "/re_status",
                type: "get",
                success: function (data) {
                    if (data.result == "end_step") {
                        var msg = "是否自动刷新页面？";
                        if (confirm(msg) == true) {
                            window.location.reload();
                        }
                    } else {
                        $('.theme-popover-mask').fadeIn(100);
                        $('.theme-popover').html("");
                        $('.theme-popover').attr("style", "width:80%");
                        //$('.theme-popover').attr("style","left:20%");
                        var imgli = '<img src="'+urldata+'/re_images/' + data.images + '" style="margin-top: -8%;margin-left: 0%;width: 100%;height: 900px;"></img>'
                        $('.theme-popover').append($(imgli));
                        $('.theme-popover').slideDown(200);
                        setTimeout(loopfn, 1000);
                    }
                }
            })
        }
        loopfn()
    };

function displayScheduleButton() {
    var booltext = $('#casetb').html();
    if (booltext==""){
        $(".theme-schedule").css("display","none");
    }
    else {
        $(".theme-schedule").css("display","block");
    }
};
function clearForm() {

    location.reload();
}



var count_progressing=0;
function start_long_task() {
            // add task status elements
            $("#progressing").html();
            $(".theme-popover-runScheduleTest").fadeIn(10);
            count_progressing+=1;
            var progressing_count="progressing_"+count_progressing
            var casetb="casetb_"+count_progressing
            div = $('<div class="progressing"><div></div><div class="ProgressBar" style="position:absolute;width:100%;height:40px;z-index:9999;top:10%;font-size:40px;font-weight:bold">0%</div><div class="status"  style="position:absolute;width:100%;height:40px;z-index:9999;top:40%;font-size:25px;font-weight:bold">...</div></div><hr>');
            var exists_progress=$('.progressing');
            if (exists_progress.length){
            $('#progressing').remove(div);
            $('#progressing').append(div);
            }
            else{
            $('#progressing').append(div);
            };
            // create a progress bar
            var nanobar = new Nanobar({
                bg: '#44f',
                target: div[0].childNodes[0]
            });
            // send ajax POST request to start background job
            var api_json = {};
            var schedule_env = $("#schedule_env").find("option:selected").val();
            var schedule_num = $("#schedule_num").find("option:selected").val();
           $('input[class="check_box"]:checked').each(function(k) {
               var api_detail = {};
               var api_pid = $(this).parents('tr').find('td').eq(1).text();     //获取页面API 对应的id
               var project = $(this).parents('tr').find('td').eq(2).text();     //接口对应的项目
               var case_api = $(this).parents('tr').find('td').eq(3).text();    //接口对应的名称
               api_detail.project = project;
               api_detail.case_api = case_api;
               api_detail.api_pid = api_pid;
               api_json[api_pid] = JSON.stringify(api_detail);
            });
            console.log(api_json);
            $.ajax({
                type: 'post',
                url: '/doSelfSchedule',
                dataType: 'json',
                data: {
                    api_json:JSON.stringify(api_json),
                    schedule_env: schedule_env,
                    schedule_num: schedule_num,
                    timer: 1
                },
                success: function(data, status, request) {
                    console.log(data);
                    if (data["reason"]){
                    alert(data["msg"]+"\n"+data["reason"]);
                    }else{
                    alert(data["msg"]);
                    }
                    status_url = request.getResponseHeader('Location');
                    var project = 'test';
                   // var table_html='<table id="' +progressing_count+'" class="table table-striped table-bordered table-hover"><tbody><tr><th width="10%" class="btn-info">接口名称</th><th width="20%" class="btn-info">URL</th><th width="5%" class="btn-info">请求方式</th><th width="30%" class="btn-info">返回结果</th><th width="30%" class="btn-info">预期结果</th><th width="5%" class="btn-info">测试结果</th></tr></tbody><tbody id="'+casetb+'"></tbody></table>'
                   // $('.page-content-report').append(table_html);
                    update_progress(status_url, nanobar, div[0],casetb);
                },
                error: function() {
                    alert("系统错误,请检查输入数据后重新提交");
                }
            });
        };
function update_progress(status_url, nanobar, status_div,casetb) {
            // send GET request to status URL
            $.getJSON(status_url, function(data) {
                // update UI
                percent = parseInt(data['current'] * 100 / data['total']);
                nanobar.go(percent);
                $(status_div.childNodes[1]).text(percent + '%');
                $(status_div.childNodes[2]).text(data['status']);
                console.log(data["datas"]);
                if (data["datas"]){
                var tableHTML='<tr><td id="api_name">' + data["datas"]["case_api"] + '</td><td id="api_url">' + data["datas"]["case_host"] +'/'+data["datas"]["case_url"] +'</td><td id="api_method">' + data["datas"]["method"] + '</td><td id="api_resp">' + data["resp"] + '</td><td id="api_expect">'+ data["datas"]["assertValue"] + '</td><td id="api_status">' + data["pass_status"] +'</td></tr>'};
                $("#"+casetb).append(tableHTML);
                if (data['state'] != 'PENDING' && data['state'] != 'PROGRESS') {
                    if ('result' in data) {
                        // show result
                        $(status_div.childNodes[3]).text('Result: ' + data['result']);
                    }
                    else {
                        // something unexpected happened
                        $(status_div.childNodes[3]).text('Result: ' + data['state']);
                    }
                }
                else {
                    // rerun in 2 seconds
                    setTimeout(function() {
                        update_progress(status_url, nanobar, status_div,casetb);
                    }, 10000);
                }
            });
        };