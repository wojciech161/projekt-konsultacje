function submitform(arg)
{
   $('#infobord').val($('#area_infobord').val());
   arg.submit();
}

$(document).ready(function(){
    $('#area_infobord').val($('#infobord').val());
});