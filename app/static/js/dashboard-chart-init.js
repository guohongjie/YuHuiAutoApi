// Use Morris.Area instead of Morris.Line
var val1 = 0;
var val2 = 0;
var val3 = 0;
var val4 = 0;
$.ajax({
    type: 'get',
    url: "/dataRing",
    dataType: "json",
    success: function (data) {
        val1 = data.plan;
        val2 = data.doing;
        val3 = data.done;
        val4 = data.delay;
        Morris.Donut({
            element: 'graph-donut',
            data: [
                {value: val2, label: '进行中项目', formatted: '占比:' + val2 + '%'},
                {value: val3, label: '已结束项目', formatted: '占比:' + val3 + '%'},
                {value: val1, label: '未开始项目', formatted: '占比:' + val1 + '%'},
                {value: val4, label: '已延期项目', formatted: '占比:' + val4 + '%'}
            ],
            backgroundColor: false,
            labelColor: '#fff',
            colors: [
                '#4acacb', '#6a8bc0', '#5ab6df', '#fe8676'
            ],
            formatter: function (x, data) {
                return data.formatted;
            }
        });
    },
    error: function () {
        alert("环形数据获取失败！")
    }
});

function rdj(){
  $.ajax({
        type: 'get',
        url: "/rdj",
        dataType: "json",
        data:{
            env: $("#choiceEnv").find("option:selected").val(),
            startDate: $("#startDate").val(),
            endDate: $("#endDate").val(),
        },
        success: function (data1) {
            var d1 = data1["d1"];
            var d2 = data1["d2"];
            var data = ([{
                label: "成功",
                data: d1,
                lines: {
                    show: true,
                    fill: true,
                    fillColor: {
                        colors: ["rgba(255,255,255,.4)", "rgba(183,236,240,.4)"]
                    }
                }
            },
                {
                    label: "失败",
                    data: d2,
                    lines: {
                        show: true,
                        fill: true,
                        fillColor: {
                            colors: ["rgba(255,255,255,.0)", "rgba(253,96,91,.7)"]
                        }
                    }
                }
            ]);

            var options = {
                grid: {
                    backgroundColor:
                        {
                            colors: ["#ffffff", "#f4f4f6"]
                        },
                    hoverable: true,
                    clickable: true,
                    tickColor: "#eeeeee",
                    borderWidth: 1,
                    borderColor: "#eeeeee"
                },
                // Tooltip
                tooltip: true,
                tooltipOpts: {
                    content: "任务排序: %x 数量:%y ",
                    shifts: {
                        x: -60,
                        y: 25
                    },
                    defaultTheme: false
                },
                legend: {
                    labelBoxBorderColor: "#000000",
                    container: $("#main-chart-legend"), //remove to show in the chart
                    noColumns: 0
                },
                series: {
                    stack: true,
                    shadowSize: 0,
                    highlightColor: 'rgba(000,000,000,.2)'
                },
//        lines: {
//            show: true,
//            fill: true
//
//        },
                points: {
                    show: true,
                    radius: 3,
                    symbol: "circle"
                },
                colors: ["#5abcdf", "#ff8673"]
            };
            var plot = $.plot($("#main-chart #main-chart-container"), data, options);
        },
        error: function () {
            alert("燃尽图数据获取失败！")
        }
    });
}
$(function () {
    rdj();
    // var d1 = [
    //     [0, 501],
    //     [1, 620],
    //     [2, 437],
    //     [3, 361],
    //     [4, 549],
    //     [5, 618],
    //     [6, 570],
    //     [7, 758],
    //     [8, 658],
    //     [9, 538],
    //     [10, 488],
    //     [11, 620],
    //     [12, 437],
    //     [13, 361],
    //     [14, 549],
    //     [15, 618],
    //     [16, 570],
    //     [17, 758],
    //     [18, 658],
    //     [19, 538],
    //     [20, 488],
    //     [21, 620],
    //     [22, 437],
    //     [23, 361],
    //     [24, 549],
    //     [25, 618],
    //     [26, 570],
    //     [27, 758],
    //     [28, 658],
    //     [29, 538],
    //     [30, 488],
    //     [31, 488]
    //
    // ];
    // var d2 = [
    //     [0, 401],
    //     [1, 520],
    //     [2, 337],
    //     [3, 261],
    //     [4, 449],
    //     [5, 518],
    //     [6, 470],
    //     [7, 658],
    //     [8, 558],
    //     [9, 438],
    //     [10, 388],
    //     [11, 520],
    //     [12, 337],
    //     [13, 261],
    //     [14, 449],
    //     [15, 518],
    //     [16, 470],
    //     [17, 658],
    //     [18, 558],
    //     [19, 438],
    //     [20, 388],
    //     [21, 520],
    //     [22, 337],
    //     [23, 261],
    //     [24, 449],
    //     [25, 518],
    //     [26, 470],
    //     [27, 658],
    //     [28, 558],
    //     [29, 438],
    //     [30, 388],
    //     [31, 388]
    // ];
});
$("#endDate").blur(function(){rdj()})