$("#msg_select_btn").click(function () {
    var curPageIndex = 1;
    $(".pagination").css("display","inline-block");
    searchApi(curPageIndex);
     $(".theme-schedule").css("display","block");
    });
$("body").delegate(".review","click", function () {
            $td = $(this).parents("tr").find("td");
             $.ajax({
                url: "/msgReviews",
                type: "get",
                data: {
                    pid:  $td.eq(1).text(),
                }
            }).done(function(result){
                    if (result.code == "200"){
                        alert(result.datas);
                        searchApi(1);}
                    else{
                        alert(result.datas);
                       }
                });
    });

$("body").delegate(".reject","click", function () {
                     $td = $(this).parents("tr").find("td");
             $.ajax({
                url: "/msgReject",
                type: "get",
                data: {
                    pid:  $td.eq(1).text(),
                }
            }).done(function(result){
                    if (result.code == "200"){
                        alert(result.datas);
                        searchApi(1);}
                    else{
                        alert(result.datas);
                       }
                });
    });

$("body").delegate(".reread","click", function () {
                     $td = $(this).parents("tr").find("td");
             $.ajax({
                url: "/msgRead",
                type: "get",
                data: {
                    pid:  $td.eq(1).text(),
                }
            }).done(function(result){
                    if (result.code == "200"){
                        alert(result.datas);
                        searchApi(1);}
                    else{
                        alert(result.datas);
                       }
                });
    });
$("#prePageApi").click(function () {
    var curPageIndex = parseInt($("#curPageApi").text())-1;
    searchApi(curPageIndex);
    });
$("#nextPageApi").click(function () {
    var curPageIndex = parseInt($("#curPageApi").text())+1;
    searchApi(curPageIndex);
    });

function searchApi(curPageIndex) {
    $.ajax({
            url: "/msgSearch",
            type: "get",
            data: {
                msg_tester: $("#msg_tester").find("option:selected").val(),
                msg_review: $("#msg_review").find("option:selected").val(),
                curPageIndex: curPageIndex
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
                if (_temo[i][5]==true){ //判断管理员
                        if (_temo[i][4]=="0"){    //判断为　未审核　＝０　
                        tableHTML = tableHTML +
                         '<tr><td class="check_box"><input type="checkbox" class="check_box" ></td>' +
                            '<td id="pid" style="display:none">' + _temo[i][0] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][1] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][2] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][3] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">未审核</td>' +
                        '<td style="text-align: center;vertical-align:middle">' +
                         '<a data-pid="' + _temo[i][0] + '" class="btn btn-primary btn-large review">审核</a>'+
                         '<a data-pid="' + _temo[i][0] + '" class="btn btn-primary btn-large reject">拒绝</a>'+'</td>'+
                        '</tr>'}
                        else if(_temo[i][4]=="1"){
                                          tableHTML = tableHTML +
                         '<tr><td class="check_box"><input type="checkbox" class="check_box" ></td>' +
                            '<td id="pid" style="display:none">' + _temo[i][0] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][1] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][2] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][3] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">已审核</td>' +
                        '<td style="text-align: center;vertical-align:middle">' +
                         '<a data-pid="' + _temo[i][0] + '" class="btn btn-primary btn-large">已审核</a>'+'</td>'+
                        '</tr>'}
                        else if(_temo[i][4]=="2"){
                                          tableHTML = tableHTML +
                         '<tr><td class="check_box"><input type="checkbox" class="check_box" ></td>' +
                            '<td id="pid" style="display:none">' + _temo[i][0] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][1] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][2] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][3] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">已拒绝</td>' +
                        '<td style="text-align: center;vertical-align:middle">' +
                         '<a data-pid="' + _temo[i][0] + '" class="btn btn-primary btn-large">已拒绝</a>'+'</td>'+
                        '</tr>'}
                        else {
                                          tableHTML = tableHTML +
                         '<tr><td class="check_box"><input type="checkbox" class="check_box" ></td>' +
                            '<td id="pid" style="display:none">' + _temo[i][0] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][1] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][2] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][3] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">用户已阅</td>' +
                        '<td style="text-align: center;vertical-align:middle">' +
                         '<a data-pid="' + _temo[i][0] + '" class="btn btn-primary btn-large">已阅</a>'+'</td>'+
                        '</tr>'}
                        }
                else {
                      if (_temo[i][4]=="0"){    //判断为　未审核　＝０　
                        tableHTML = tableHTML +
                         '<tr><td class="check_box"><input type="checkbox" class="check_box" ></td>' +
                            '<td id="pid" style="display:none">' + _temo[i][0] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][1] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][2] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][3] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">未审核</td>' +
                        '<td style="text-align: center;vertical-align:middle">' +
                        '<a data-pid="' + _temo[i][0] + '" class="btn btn-primary btn-large reread">已阅</a>'+
                        '</tr>'}
                        else if(_temo[i][4]=="1"){
                                          tableHTML = tableHTML +
                         '<tr><td class="check_box"><input type="checkbox" class="check_box" ></td>' +
                            '<td id="pid" style="display:none">' + _temo[i][0] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][1] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][2] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][3] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">已审核</td>' +
                        '<td style="text-align: center;vertical-align:middle">' +
                             '<a data-pid="' + _temo[i][0] + '" class="btn btn-primary btn-large reread">已阅</a>'+
                        '</tr>'}
                        else if(_temo[i][4]=="2"){
                                          tableHTML = tableHTML +
                         '<tr><td class="check_box"><input type="checkbox" class="check_box" ></td>' +
                            '<td id="pid" style="display:none">' + _temo[i][0] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][1] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][2] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">' + _temo[i][3] + '</td>' +
                        '<td style="text-align: center;vertical-align:middle">已拒绝</td>' +
                        '<td style="text-align: center;vertical-align:middle">' +
                             '<a data-pid="' + _temo[i][0] + '" class="btn btn-primary btn-large reread">已阅</a>'+
                        '</tr>'}
                        else {
                              tableHTML = tableHTML +
                             '<tr><td class="check_box"><input type="checkbox" class="check_box" ></td>' +
                                '<td id="pid" style="display:none">' + _temo[i][0] + '</td>' +
                            '<td style="text-align: center;vertical-align:middle">' + _temo[i][1] + '</td>' +
                            '<td style="text-align: center;vertical-align:middle">' + _temo[i][2] + '</td>' +
                            '<td style="text-align: center;vertical-align:middle">' + _temo[i][3] + '</td>' +
                            '<td style="text-align: center;vertical-align:middle">已阅</td>' +
                            '<td style="text-align: center;vertical-align:middle">' +
                             '<a data-pid="' + _temo[i][0] + '" class="btn btn-primary btn-large reread">已阅</a>'+
                            '</tr>'}
                    }
                }
              $("#casetb").html(tableHTML);
        });
};