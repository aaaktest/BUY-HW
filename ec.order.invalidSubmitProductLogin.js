ec.order.invalidSubmitProductLogin = function() {
  $("#checkoutSubmit").addClass("disabled");
  var orderType = $("#orderType").val();
  if (document.getElementsByName("orderType").length > 1) orderType = 0;
  var UIDesignID = $("input[name\x3d'UIDesignID']").val();
  var sbs = $("input[name\x3d'sbs']").val();
  var css = $("input[name\x3d'css']").val();
  var qtys = $("input[name\x3d'qtys']").val();
  var ess = $("input[name\x3d'ess']").val();
  var ass = $("input[name\x3d'ass']").val();
  var addressId = $("input[name\x3d'consigneeAddressId']").val();
  var couponCode = $("input[name\x3d'couponCode']").val();
  var orderReq = $("input[name\x3d'orderReq']").val();
  var iMeiCode = $("input[name\x3d'imeiCode']").val();
  if (orderType == "25") data = {
    "UIDesignID": UIDesignID,
    "sbs": sbs,
    "css": css,
    "qtys": qtys,
    "ess": ess,
    "ass": ass,
    "orderType": orderType,
    "addressId": addressId,
    "couponCode": couponCode
  };
  else data = {
    "orderReq": orderReq,
    "orderType": orderType,
    "addressId": addressId,
    "couponCode": couponCode,
    "imeiCode": iMeiCode
  };
  $("#checkoutSubmit").addClass("disabled");
  $.ajax({
    url: "/order/validateOrder.json",
    timeout: 1E4,
    type: "POST",
    data: data,
    success: function(json) {
      var json = ec.lang.json.parse(json);
      // if (!json.success) if (json.errorCode == "noProduct") {
      //   ec.order.noProduct();
      //   $("#checkoutSubmit").removeClass("disabled");
      //   return
      // } else if (json.errorCode == "addressError") {
      if (json.errorCode == "addressError") {
        if (json.msg != "" && json.msg != undefined && json.msg != null) ec.order.ecboxOpen(json.msg);
        else ec.order.ecboxOpen("\u60a8\u7684\u6536\u8d27\u5730\u5740\u6709\u8bef,\u8bf7\u4fee\u6539\u6536\u8d27\u5730\u5740\u518d\u8bd5\uff01");
        $("#checkoutSubmit").removeClass("disabled");
        return
      } else if (json.errorCode == "errorMsg") {
        ec.order.ecboxOpen(json.msg);
        $("#checkoutSubmit").removeClass("disabled");
        return
      } else {
        var input = "";
        input += '\x3cinput name\x3d"errorCode" type\x3d"text" value\x3d\'' + json.errorCode + "'\x3e";
        input += '\x3cinput name\x3d"errorMsg" type\x3d"text" value\x3d"' + json.msg + '"\x3e';
        var $form = $("#validateForward");
        $form.append(input);
        $("body").append($form);
        $form.submit()
      }
      if (ec.lang.json.parse(json.invalidProductList.transHtmlAttribute()).length > 0) {
        var r = ec.lang.json.parse(json.invalidProductList.transHtmlAttribute());
        ec.encryptJSON(r);
        ec.order.invalidProduct(r)
      } else ec.order.splitOrder()
    },
    error: function() {
      ec.order.ecboxOpen("\u64cd\u4f5c\u8d85\u65f6\uff0c\u8bf7\u91cd\u8bd5\uff01");
      $("#checkoutSubmit").removeClass("disabled")
    }
  })
};