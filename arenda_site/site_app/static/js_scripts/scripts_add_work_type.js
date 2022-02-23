function addWork() {
  var nameid = "div[hidden]";
//  $( nameid ).first().removeAttr('hidden').fadeIn(2000)
  $( nameid ).each(function( i ) {
    alert($(this))
    $(this).fadeIn().removeAttr('hidden');
    return false
    });
  }


function removeWork() {
  var id="div[id^='rf_']";
  var del_name = id + ' :visible';
  $( del_name ).last().hide(2000);
  alert(del_name)
  };

$(document).ready(function  () {
    $("#add_work").click(function () {
        addWork();
    });

//    $("#remove_work").click(function () {
//        removeWork();
////        location.reload();
//    });

});