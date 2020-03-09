!function () {
    var canvass = document.getElementsByClassName("canvass")[0];
    var ctx = canvass.getContext("2d");

    var border = {
        width: 40 //头像边框厚度
        ,
        color: "rgba(247, 248, 250, .9)" //头像边框颜色
    }

    var minImgRect = {
        width: null,
        height: null
    }; //图像的最小高度与宽度
    var currLoc = {
        x: null,
        y: null
    }; //保存当前图片在canvas里的位置
    var imgRect = {
        width: null,
        height: null
    }; //保存当前图像的宽度与高度（缩放后）
    var midpoint = null; //保存当前图片的居中比例，拖动时清空，缩放时重新计算
    //    居中比例：以canvas中轴线为基准将图片切成两部分，左侧部分占总宽度的比例，y方向同理。

    var rangeInput = document.getElementsByClassName("rangeInput")[0]; //滑块对象
    var uploadButton = document.getElementsByClassName("uploadButton")[0]; //图像上传按钮对象
    var fileInput = uploadButton.getElementsByClassName("fileInput")[0]; //图像上传控件
    var image = new Image(); //图像文件

    //<div>元素模拟图片上传按钮
    uploadButton.onclick = function (event) {
        return fileInput.click();
    }

    //图片上传处理代码
    fileInput.addEventListener('change', function (event) {
        var file = fileInput.files[0];
        image.src = URL.createObjectURL(file);
        image.onload = function (event) {
            //缩放图片到刚好填满中框
            if (image.width < image.height) {
                minImgRect.width = canvass.width - border.width * 2;
                minImgRect.height = parseInt(minImgRect.width / image.width * image.height);
            } else {
                minImgRect.height = canvass.height - border.width * 2;
                minImgRect.width = parseInt(minImgRect.height / image.height * image.width);
            }
            //绘制初始图片
            imgRect.width = minImgRect.width;
            imgRect.height = minImgRect.height;
            drawing(centerImg({
                x: 0.5,
                y: 0.5
            }));
        };
    }, false);

    //根据居中比例及图像大小，计算放置图片的坐标
    //    参数: {x: <0-1>, y: <0-1>}
    //    结果: {x: <coordinate_X>, y: <coordinate_Y>}
    function centerImg(ratio) {
        return { // 居中时应满足如下条件，借此计算出偏移量 x 和 y
            x: canvass.width / 2 - imgRect.width * ratio.x, // 横坐标偏移(x) + 图像宽度*横向居中比例 应等于 canvas 宽度的一半（中点横坐标）
            y: canvass.height / 2 - imgRect.height * ratio.y // 纵坐标偏移(y) + 图像高度*纵向居中比例 应等于 canvas 高度的一半（中点纵坐标）
        };
    }

    //绘制图片到canvas
    function drawing(loc) {
        ctx.clearRect(0, 0, canvass.width, canvass.height);
        ctx.drawImage(image, loc.x, loc.y, imgRect.width, imgRect.height); //指定坐标输出图像
        ctx.strokeStyle = border.color; // \
        ctx.lineWidth = border.width; // | 绘制半透明边框
        ctx.strokeRect(border.width / 2, border.width / 2, canvass.width - border.width, canvass.height - border.width); // /
        currLoc = {
            x: loc.x,
            y: loc.y
        };
    }

    //缩放相关代码
    rangeInput.oninput = function (event) {
        //检查缩放前是否发生过拖动(midpoint是否被清除)，如果是则重新计算居中比例
        if (midpoint == null) {
            midpoint = {
                x: (canvass.width * 0.5 - currLoc.x) / imgRect.width,
                y: (canvass.height * 0.5 - currLoc.y) / imgRect.height
            }
        }

        imgRect.width = minImgRect.width * parseFloat(this.value);
        imgRect.height = minImgRect.height * parseFloat(this.value);
        loc = centerImg(midpoint);
        //检查计算出的位置是否存在脱离中框的情况
        if (loc.x > 40) {
            midpoint = null; //由于发生位移，需要情况居中比例，重新计算
            loc.x = 40;
        }
        if (loc.x + imgRect.width < canvass.width - 40) {
            midpoint = null;
            loc.x = canvass.width - 40 - imgRect.width;
        }
        if (loc.y > 40) {
            midpoint = null;
            loc.y = 40;
        }
        if (loc.y + imgRect.height < canvass.height - 40) {
            midpoint = null;
            loc.y = canvass.height - 40 - imgRect.height;
        }
        drawing(loc);
    }

    //拖动相关代码
    canvass.onmousedown = function (event) {
        var lastMouseLoc = {
            x: event.clientX,
            y: event.clientY
        };

        document.onmousemove = function dragging(event) {
            midpoint = null; //由于位置改变，居中比例需要清空，以便在缩放时重新计算。
            var mouseMove = {
                x: event.clientX - lastMouseLoc.x,
                y: event.clientY - lastMouseLoc.y
            };
            lastMouseLoc = {
                x: lastMouseLoc.x + mouseMove.x,
                y: lastMouseLoc.y + mouseMove.y
            };

            if (currLoc.x + mouseMove.x > 40) { //禁止图像向左拖出中框
                mouseMove.x = 40 - currLoc.x;
            }
            if (currLoc.x + mouseMove.x + imgRect.width < canvass.width - 40) { //禁止图像向右拖出中框
                mouseMove.x = canvass.width - 40 - currLoc.x - imgRect.width;
            }
            if (currLoc.y + mouseMove.y > 40) { //禁止图像向下拖出中框
                mouseMove.y = 40 - currLoc.y;
            }
            if (currLoc.y + mouseMove.y + imgRect.height < canvass.height - 40) { //禁止图像向上拖出中框
                mouseMove.y = canvass.height - 40 - currLoc.y - imgRect.height;
            }

            drawing({
                x: currLoc.x + mouseMove.x,
                y: currLoc.y + mouseMove.y
            });
        }

        document.onmouseup = function (event) {
            document.onmousemove = null;
        }
    };


    //保存画板
    $('#img_submit').click(
        function canvasSaveToServer() {
                        const tmp=document.createElement('canvas');
            tmp.width=160;
            tmp.height=160;
            const tmpCtx=tmp.getContext('2d');
            tmpCtx.drawImage(canvass,40,40,160,160,0,0,160,160);
            var imgUrl = tmp.toDataURL("image/png");
            var imageDataB64 = imgUrl.substring(22);
            // alert("savePic" + imageDataB64);
            imgData = {uploadImg: imageDataB64};
            var senddata = JSON.stringify(imgData);
            var deptName = $("#test_group").find("option:selected").val();
            if (deptName=="None"){
                alert("请选择测试组别!");
                return;
            }
           //方法二：通过ajax 传送到后台
            $.ajax({
                url: "/uploadImg",
                type: "POST",
                //data: { "uploadImg": imageDataB64},
                data:senddata,
                async: true,
                cashe: false,
                contentType: false,
                processData: false}).done(function (result) {
                if (result['code']=="200"){
                        //发送数据
                    $.ajax({
                        url: "/uploadDept",
                        type: "POST",
                        data:{
                            deptName:deptName,
                        }
                        }).done(function (result) {
                         if (result['code']=="200") {
                            alert(result['msg']);
                            }
                         else{
                            alert(result["msg"]);
                         }
                        }); }
                   else{
                   alert(result["msg"]);
                   }
                })
        })

}()

