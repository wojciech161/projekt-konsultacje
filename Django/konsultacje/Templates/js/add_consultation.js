//function
function button_off(){
        $('#button').removeAttr('class');
        $('#button').attr('disabled','disabled');
        $('#button').attr('style','color:#777777;');
        $('#button').attr('class','button_disabled');
}
function button_on(){
    if($('#building').val()!='' && $('#room').val()!='' && $('#day').val()!=0 && $('#week').val()!=0 && $('#start_hour').val()!=0 && $('#start_minutes').val()!=1 && $('#date').val()!=''){
        $('#button').removeAttr('class');
        $('#button').removeAttr('disabled');
        $('#button').removeAttr('style');
        $('#button').attr('class','button3');
    }
}
//----------------------------------

$(document).ready(function(){
  
 if($('#day').val()!=0){
    $('#day_check_yes').html('<img src="/static/images/change.png"/>');
    button_on();  
 }
 if($('#week').val()!=0){
    $('#week_check_yes').html('<img src="/static/images/change.png"/>');
    button_on();  
 }
 if($('#date')!=''){
    var date=$('#date').val();
    var reg = /^([0-9]{1,2})+\/([0-9]{1,2})+\/([0-9]{1,4})$/;
    if(reg.test(date) == true){
    button_on();
    $('#expiry_massage_status').html('<img src="/static/images/change.png"/>');
    } else {
            button_off();
            $('#expiry_massage_status').html('');
           }
 }
 if($('#start_hour').val()!=0){
    var list_value = $('#start_hour').val();
    list_value = parseFloat(list_value);
    if($('#start_hour').val()!=0){
    button_on();
    $('#start_minutes').removeAttr('disabled');
    var select_end_hour = '<select class="selectt" name="end_hour" id="end_hour">\n';
    for(i=list_value+1;i<23;i++)
    {
        select_end_hour=select_end_hour+'<option value="'+i+'">'+i+'</option>';
    }
    select_end_hour=select_end_hour+'</select>';
    $('#end_hour_span').html(select_end_hour);
    if($('#start_minutes').val()!=1){
        $('#start_hour_check_yes').html('<img src="/static/images/change.png"/>');
        $('#end_hour_check_yes').html('<img src="/static/images/change.png"/>');
    }
    } else {
             $('#start_minutes').attr('disabled','disabled');
             $('#end_hour').attr('disabled','disabled');
             $('#start_hour_check_yes').html('');
             $('#end_hour_check_yes').html('');
             button_off();   
           }  
 }  
 
 if($('#building').val()!=0){
    $('#building_massage_status').html('<img src="/static/images/change.png"/>');
 }
  if($('#room').val()!=0){
    $('#room_massage_status').html('<img src="/static/images/change.png"/>');
 }
 
 if(1){
 var students_limit=$('#students_limit').val();
    button_on();
    var reg = /^([0-9]{0,3})$/;
    if(reg.test(students_limit) == false) {
    $('#students_limit_massage_status').text('Podano złą liczbę '); 
    button_off();}
    else $('#students_limit_massage_status').html('<img src="/static/images/change.png"/>');
 }
 
 
 
 
 
 
 
 
 
 
 
$('#day').change(function(){
    if($('#day').val()!=0){
    $('#day_check_yes').html('<img src="/static/images/change.png"/>');
    button_on();
    }else {
            $('#day_check_yes').html(''); 
            button_off();
          }
});

$('#week').change(function(){
    if($('#week').val()!=0){
    $('#week_check_yes').html('<img src="/static/images/change.png"/>');
    button_on();
    } else {
            $('#week_check_yes').html(''); 
            button_off();
           }
});

$('#start_hour').change(function(){
    var list_value = $('#start_hour').val();
    list_value = parseFloat(list_value);
    if($('#start_hour').val()!=0){
    button_on();
    $('#start_minutes').removeAttr('disabled');
    var select_end_hour = '<select class="selectt" name="end_hour" id="end_hour">\n';
    for(i=list_value+1;i<23;i++)
    {
        select_end_hour=select_end_hour+'<option value="'+i+'">'+i+'</option>';
    }
    select_end_hour=select_end_hour+'</select>';
    $('#end_hour_span').html(select_end_hour);
    if($('#start_minutes').val()!=1){
        $('#start_hour_check_yes').html('<img src="/static/images/change.png"/>');
        $('#end_hour_check_yes').html('<img src="/static/images/change.png"/>');
    }
    } else {
             $('#start_minutes').attr('disabled','disabled');
             $('#end_hour').attr('disabled','disabled');
             $('#start_hour_check_yes').html('');
             $('#end_hour_check_yes').html('');
             button_off();   
           }
    
});

$('#start_minutes').change(function(){
    if($('#start_minutes').val()!=1){
    button_on(); 
    var list_value = $('#start_minutes').val();
    $('#start_hour_check_yes').html('<img src="/static/images/change.png"/>');
    var temp='<input type="hidden" name="end_minutes" id="end_minutes" value="'+list_value+'" />'+list_value;
    $('#end_minutes').html(temp);
    $('#end_hour_check_yes').html('<img src="/static/images/change.png"/>');
    } else {
            $('#end_minutes').html('00');
            $('#start_hour_check_yes').html('');
            $('#end_hour_check_yes').html('');
            button_off();   
           }
    
});

//start---------------------------------------
// sprawdzenie poprawnosci nazwiska
$('#building').keyup(function(){
    var building=$('#building').val();
    button_on();
    var reg = /^([A-ZACESZZL]{1,1})+\-([0-9]{1,4})$/;
    if(reg.test(building) == false) {
    $('#building_massage_status').text('Nazwa budynku jest niepoprawna'); 
    button_off();}
    else $('#building_massage_status').html('<img src="/static/images/change.png"/>');
});

$('#building').focusin(function(){
   $('#building_massage_example').text(' wzór: C-1');
}).blur(function(){
    $('#building_massage_example').text('');
    var building=$('#building').val();
    button_on();
    var reg = /^([A-ZACESZZL]{1,1})+\-([0-9]{1,4})$/;
    if(reg.test(building) == false) {
    $('#building_massage_status').text('Nazwa budynku jest niepoprawna'); 
    button_off();}
    else $('#building_massage_status').html('<img src="/static/images/change.png"/>');
    
});
//end----------------------------------------------

// start------------------------------------------
// sprawdzenie poprawnosci nazwiska
$('#room').keyup(function(){
    var room=$('#room').val();
    button_on();
    var reg = /^([0-9]{1,4})$/;
    if(reg.test(room) == false) {
    $('#room_massage_status').text('Wpisany nieporawny pokoj'); 
    button_off();}
    else $('#room_massage_status').html('<img src="/static/images/change.png"/>');
});

$('#room').focusin(function(){
   $('#room_massage_example').text(' wzor: 123');
}).blur(function(){
    $('#room_massage_example').text('');
    var room=$('#room').val();
    button_on();
    var reg = /^([0-9]{1,4})$/;
    if(reg.test(room) == false) {
    $('#room_massage_status').text('Wpisany nieporawny pokoj'); 
    button_off();}
    else $('#room_massage_status').html('<img src="/static/images/change.png"/>');
});

//end----------------------------------------------


// start------------------------------------------
// sprawdzenie poprawnosci nazwiska
$('#students_limit').keyup(function(){
    var students_limit=$('#students_limit').val();
    button_on();
    var reg = /^([0-9]{0,3})$/;
    if(reg.test(students_limit) == false) {
    $('#students_limit_massage_status').text('Podano zla liczbe '); 
    button_off();}
    else $('#students_limit_massage_status').html('<img src="/static/images/change.png"/>');
});

$('#students_limit').focusin(function(){
   $('#students_limit_massage_example').text(' wzor: 10 lub nic, jezeli niechcesz ustaic limitu');
}).blur(function(){
    $('#students_limit_massage_example').text('');
    var students_limit=$('#students_limit').val();
    button_on();
    var reg = /^([0-9]{0,3})$/;
    if(reg.test(students_limit) == false) {
    $('#students_limit_massage_status').text('Podano zla liczbe '); 
    button_off();}
    else $('#students_limit_massage_status').html('<img src="/static/images/change.png"/>');
});


$('#jeden').keyup(function(){
    var test = $('#jeden').val();
    test=test.length();
    $('#dwa').attr('value',test);
});
//end----------------------------------------------


$('#date').datepicker({ minDate: '0d', dateFormat: 'dd/mm/yy' })
});
$('#date').focusout(function(){
    var date=$('#date').val();
    var reg = /^([0-9]{1,2})+\/([0-9]{1,2})+\/([0-9]{1,4})$/;
    if(reg.test(date) == true){
    button_on();
    $('#expiry_massage_status').html('<img src="/static/images/change.png"/>');
    } else {
            button_off();
            $('#expiry_massage_status').html('');
           }
});
$('#date').keyup(function(){
    var date=$('#date').val();
    var reg = /^([0-9]{1,2})+\/([0-9]{1,2})+\/([0-9]{1,4})$/;
    if(reg.test(date) == true){
    button_on();
    $('#expiry_massage_status').html('<img src="/static/images/change.png"/>');
    } else {
            button_off();
            $('#expiry_massage_status').html('');
           }
});
