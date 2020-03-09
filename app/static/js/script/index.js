$(function(){
    //获取用户信息
    // 左侧点击展开收起
    $(".article-list-tit").on("click",function(){
        $(this).toggleClass("down").parents(".article-list").siblings().find(".article-list-tit").removeClass("down");
        $(this).siblings("ul").toggle();
        $(this).parents(".article-list").siblings().find("ul").hide();
    })
    // 日期插件
    $("#datepicker1").datepicker({
            numberOfMonths: 1,
            changeMonth: true,
            changeYear: true,
            minDate: '',
            dateFormat:"yy-mm-dd"
    });
    $("#datepicker2").datepicker({
            numberOfMonths: 1,
            changeMonth: true,
            changeYear: true,
            minDate: '',
            dateFormat:"yy-mm-dd"
    });

      $("#datepickerOnL").datepicker({
            numberOfMonths: 1,
            changeMonth: true,
            changeYear: true,
            minDate: '',
            dateFormat:"yy-mm-dd"
      });

      $("#datepickerOnL2").datepicker({
            numberOfMonths: 1,
            changeMonth: true,
            changeYear: true,
            minDate: '',
            dateFormat:"yy-mm-dd"
      });
    var _time=new Date().getTime();
    var verify=function(){};
    verify.prototype={
        //获取数据
        getData:function(table,startdata,enddata,type){
            var _time=new Date().getTime();
            var _this=this;
            $.ajax({
                url:"/report_datas",
                type:"get",
                data:{
                    table:table,
                    startdata:startdata,
                    startdata:startdata,
                    enddata:enddata,
                    type:type
                },
                crossDomain: true,
                dataType:"jsonp",
                jsonpCallback:"resp"
            }).done(function(result){
                if(result.status_code==200&&result.result.length>0){
                    _this.alasyData(result);
                    var hre="/Report?type="+type+"&table="+table;
                    $(".seepage").attr("href",hre).show();
                }else{
                    $("#canvasDiv1").html("当前时间段没有返回数据！");
                    $("#canvasDiv2").html("");
                    $(".seepage").hide();
                    $(".charts").hide();
                    return false;
                }
            }).fail(function(){
                console.log("接口不通");
            })
        },
        //分析数据  绘制折线图
        alasyData:function(value){
            var usetime=[],t;
            var labels = [];//鼠标移入usetime显示数据
            var label=[];//横坐标
            var passArr=[];
            var data=value.result;
            var max=parseInt(value.Max),min=parseInt(value.Min);
            var scale=Math.ceil((max-min)/5);
            for(var i=0;i<data.length;i++){
                var time=data[i].data;
                var pointtime=time.substring(0,4)+"年"+time.substring(4,6)+"月"+time.substring(6,8)+"日 "+time.substring(8,10)+":"+time.substring(10,12)+":"+time.substring(12,14);
                var xtime=time.substring(0,4)+"/"+time.substring(4,6)+"/"+time.substring(6,8);
                usetime.push(Number(data[i].useTime).toFixed(2));
                labels.push(pointtime);
                label.push(xtime);
                passArr.push(data[i].passRate*100);
            }
            for(var i=0;i<label.length;i++){
                if(i>0&&i<label.length-1){
                    label[i]="";
                }
            }
            var data1 = [
                {
                    name : '耗时',
                    value:usetime,
                    color:'#aad0db',
                    line_width:2
                }
            ]; 
            var data2 = [
                {
                    name : '通过率',
                    value:passArr,
                    color:'#ff4c4c',
                    line_width:2
                }
            ]; 
            this.drawLine(data1,label,'canvasDiv1','自动化测试场景耗时','自动化测试场景耗时(s)',labels,'s',scale,min);
            this.drawLine(data2,label,'canvasDiv2','自动化测试通过率','自动化测试通过率(%)',labels,'%',40,0);
        },
        drawLine:function(data,xValue,renderDiv,title,subtitle,hoverValue,dw,scaleSize,startD){
            var chart = new iChart.LineBasic2D({
                render : renderDiv,
                data: data,
                align:'center',
                title : title,
                subtitle : subtitle,
                footnote : '',
                width : 1500,
                height : 500,
                background_color:'#FEFEFE',
                tip:{
                    enable:true,
                    shadow:true,
                    move_duration:400,
                    border:{
                         enable:true,
                         radius : 5,
                         width:2,
                         color:data[0].color
                    },
                    listeners:{
                         //tip:提示框对象、name:数据名称、value:数据值、text:当前文本、i:数据点的索引
                        parseText:function(tip,name,value,text,i){
                            return name+":"+value+dw;
                        }
                    }
                },
                tipMocker:function(tips,i){
                    return "<div style='font-weight:600'>"+
                            hoverValue[i]+" "+//日期
                            "</div>"+tips.join("<br/>");
                },
                legend : {
                    enable : true,
                    row:1,//设置在一行上显示，与column配合使用
                    column : 'max',
                    valign:'top',
                    sign:'bar',
                    background_color:null,//设置透明背景
                    offsetx:-80,//设置x轴偏移，满足位置需要
                    border : true
                },
                crosshair:{
                    enable:true,
                    line_color:data[0].color//十字线的颜色
                },
                sub_option : {
                    label:false,
                    point_size:10 //小圆点
                },
                coordinate:{
                    width:640,
                    height:240,
                    axis:{
                        color:'#dcdcdc',
                        width:1
                    },
                    scale:[{
                         position:'left',   
                         start_scale:startD,
                         end_scale:1,
                         scale_space:scaleSize,
                         scale_size:2,
                         scale_color:'#9f9f9f'
                    },{
                         position:'bottom', 
                         labels:xValue
                    }]
                }
            });

            //开始画图
            chart.draw();
        }
        
    }
    var verifyFn = new verify();  
        $(".subNavBox .ssBox li").on("click",function(){
        //$(".sub-title").removeClass("cur")
        var $parents = $(this).parents(".subNavBox")
        $parents.find("li").removeClass("active")
        $(this).addClass("active");
        })
    $(".subNavBox .sBox li").on("click",function(){
        //$(".sub-title").removeClass("cur")
        var $parents = $(this).parents(".subNavBox")
        $parents.find("li").removeClass("active")
        $(this).addClass("active");
        var table=$(this).data("table");
        var type=$(this).data("type");
        var beginTimeArr=$("#datepicker1").val().split("-");
        var endTimeArr=$("#datepicker2").val().split("-");
        var beginTime = new Date(parseInt(beginTimeArr[0]),parseInt(beginTimeArr[1])-1,parseInt(beginTimeArr[2]));
        var endTime = new Date(parseInt(endTimeArr[0]),parseInt(endTimeArr[1])-1,parseInt(endTimeArr[2]));
        if(!$("#datepicker1").val()){
            alert("请选择开始时间！");
            return false;
        }else if(!$("#datepicker2").val()){
            alert("请选择结束时间！");
            return false;
        }else if(beginTime.getTime() > endTime.getTime()){
            alert("开始时间不能大于结束时间！");
            return false;
        }else{ 
            verifyFn.getData(table,beginTimeArr.join(""),endTimeArr.join(""),type);
        }
        $(".gantte").hide();
        $(".online").hide();
        $(".charts").hide();
        $(".section-content").show();
    })

    $(".online").hide();
    $(".gant").on("click",function(){
        $(".section-content").hide();
        $(".online").hide();
        $(".charts").hide();
        $(".gantte").show();
    })
    $(".onl").on("click",function(){
        $(".section-content").hide();
        $(".gantte").hide();
        $(".charts").hide();
        $(".online").show();
    })

    $(".dialog-box").on("click",".buildbtn",function(){
        if($(this).attr("name")=="tabconsole"){
            $("#tabconsole").remove();
            var html='<iframe id="tabconsole" src="/job/Public_ScanLink/lastBuild/console" width="1350" height="800" scrolling="yes" style="border:none; z-index:8;display:none"></iframe>';
            $("#build").append(html);
        }    
        $("#"+$(this).attr("name")).show().siblings("iframe").hide();
    })

    // 弹出层
    var dialog_with = 1000;  
    var dialog_height = 800;  
    var _move=false;//移动标记  
    var _x,_y;//鼠标离控件左上角的相对位置  
    $(".dialog_show").click(function(){  
        var isclick=$(this).attr("isclick");
        $("#"+isclick).show().siblings().hide();
        $(".mask").css("opacity","0.6").show();//body加蒙板            
        var window_width = $(window).width();  
        var window_height = $(window).height();  
        /*var widd = $(this).width();  
        var heii = $(this).height();*/  
        var left = (window_width - dialog_with)/2+"px";//距左边位置  
        var top = (window_height - dialog_height)/2+"px";//距顶边位置  
      
        $("#dialog").css({//设置弹出框样式   
            "position":"absolute", 
            "z-index":"5",  
            "display":"block",  
            "width":"1000px",  
            "height":"600px",  
            "left":left,  
            "top":"20%",  
            "background":"#fff",  
            "border":"1px solid #999999",  
        });  
    });  
      
    $("#dialog_close").click(function(event){//关闭  
        /*$("#dialog").css({  
        "display":"none",  
        "speed":"600"  
        });*/  
        $("#dialog").hide(); 
        $(".mask").hide();  
    });  
  
   $("#dialog_title").click(function(){  
       //alert("click");//点击（松开后触发）  
       }).mousedown(function(e){  
       _move=true;  
       _x=e.pageX-parseInt($("#dialog").css("left"));  
       _y=e.pageY-parseInt($("#dialog").css("top"));  
       $("#dialog").fadeTo(20, 0.55);//点击后开始拖动并透明显示  
   });  
  
    $("#dialog").mouseup(function(){  
        _move=false;  
        $("#dialog").fadeTo("fast", 1);//松开鼠标后停止移动并恢复成不透明  
    });  
  
   $("#dialog_title").mousemove(function(e){  
       if(_move){  
           var x=e.pageX-_x;//移动时根据鼠标位置计算控件左上角的绝对位置  
           var y=e.pageY-_y;  
           $("#dialog").css({top:y,left:x});//控件新位置  
       }  
   }).mouseup(function(){  
        _move=false;  
        $("#dialog").fadeTo("fast", 1);//松开鼠标后停止移动并恢复成不透明  
    });               

})
//品牌旗舰店搜索条件框清空
