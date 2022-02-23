function list_forms() {
  list=$(id="div[id^='forms_']");
  list.hide();
//  list.show(2000)
  return list;
};


$(document).(function() {
  list_forms();
});

<html>
<head>
<title>Try jQuery Online</title>
<script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
<script>
$(document).ready(function() {
   $("div[hidden]").first().removeAttr("hidden");
    alert($(this))




   $("div[hidden]").first().removeAttr("hidden");




});

