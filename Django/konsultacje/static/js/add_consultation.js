//function
function button_off(){
        $('#button').removeAttr('class');
        $('#button').attr('disabled','disabled');
        $('#button').attr('style','color:#777777;');
        $('#button').attr('class','button_disabled');
}
function button_on(){
    if($('#expiry_massage_status').html()=='<img src="/static/images/change.png">' && $('#students_limit_massage_status').html()=='<img src="/static/images/change.png">' && $('#room_massage_status').html()=='<img src="/static/images/change.png">'  && $('#building_massage_status').html()=='<img src="/static/images/change.png">' && $('#building').val()!='' && $('#room').val()!='' && $('#day').val()!=0 && $('#week').val()!=0 && $('#start_hour').val()!=0 && $('#start_minutes').val()!=1 && $('#date').val()!=''){
        $('#button').removeAttr('class');
        $('#button').removeAttr('disabled');
        $('#button').removeAttr('style');
        $('#button').attr('class','button3');
    }
}
//----------------------------------

$(document).ready(function(){
  
if($('#date1').val()=='\n') $('#date1').hide();
if($('#date2').val()=='\n') $('#date2').hide();
if($('#date3').val()=='\n') $('#date3').hide();

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
    button_on();
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
    $('#students_limit_massage_status').text('Podano zla liczbe '); 
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
        select_end_hour=select_end_hour+'<option';
        if($('#end_hour').val()==i) select_end_hour=select_end_hour+' selected="selected"';
        select_end_hour=select_end_hour+' value="'+i+'">'+i+'</option>';
    }
     select_end_hour=select_end_hour+'</select>';
    $('#end_hour_span').html(select_end_hour);
    if($('#start_minutes').val()!=1){
        $('#start_hour_check_yes').html('<img src="/static/images/change.png"/>');
        $('#end_hour_check_yes').html('<img src="/static/images/change.png"/>');
        button_on();
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
    var add_selected=' selected="selected"';
    var list_value = $('#start_minutes').val();
    list_value = parseFloat(list_value);
    if($('#start_hour_check_yes').html()!='')
    {
       list_value = $('#end_minutess').val();
       list_value = parseFloat(list_value);    
    }
    $('#start_hour_check_yes').html('<img src="/static/images/change.png"/>');                
    var temp='<select id="end_minutess" name="end_minutes"><option';
    if(list_value==0) temp=temp+add_selected;
    temp=temp+' value="00">00</option><option';
    if(list_value==15) temp=temp+add_selected;
    temp=temp+' value="15">15</option><option';
    if(list_value==30) temp=temp+add_selected;
    temp=temp+' value="30">30</option><option';
    if(list_value==45) temp=temp+add_selected;
    temp=temp+' value="45">45</option>';
    temp=temp+'</select>';
    $('#end_minutes').html(temp);
    $('#end_hour_check_yes').html('<img src="/static/images/change.png"/>');
    } else {
    var temp='<select disabled="disabled"><option>00</option></select>';
            $('#end_minutes').html(temp);
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
    var reg = /^([A-ZĄĆĘŚŻŹŁŃÓŁ]{1,1})+\-([0-9]{1,4})$/;
    if(reg.test(building) == false) {
    $('#building_massage_status').text('Nazwa budynku jest niepoprawna'); 
    button_off();}
    else {$('#building_massage_status').html('<img src="/static/images/change.png"/>'); button_on();}
});

$('#building').focusin(function(){
   $('#building_massage_example').text(' wzor: C-1');
}).blur(function(){
    $('#building_massage_example').text('');
    var building=$('#building').val();
    button_on();
    var reg = /^([A-ZĄĆĘŚŻŹŁŃÓŁ]{1,1})+\-([0-9]{1,4})$/;
    if(reg.test(building) == false) {
    $('#building_massage_status').text('Nazwa budynku jest niepoprawna'); 
    button_off();}
    else {$('#building_massage_status').html('<img src="/static/images/change.png"/>'); button_on();}
    
});
//end----------------------------------------------

// start------------------------------------------
// sprawdzenie poprawnosci nazwiska
$('#room').keyup(function(){
    var room=$('#room').val();
    button_on();
    var reg = /^([0-9]{1,4})$/;
    if(reg.test(room) == false) {
    $('#room_massage_status').text('Wpisany niepoprawny pokoj'); 
    button_off();}
    else {$('#room_massage_status').html('<img src="/static/images/change.png"/>');button_on();}
});

$('#room').focusin(function(){
   $('#room_massage_example').text(' wzor: 123');
}).blur(function(){
    $('#room_massage_example').text('');
    var room=$('#room').val();
    button_on();
    var reg = /^([0-9]{1,4})$/;
    if(reg.test(room) == false) {
    $('#room_massage_status').text('Wpisany niepoprawny pokoj'); 
    button_off();}
    else {$('#room_massage_status').html('<img src="/static/images/change.png"/>');button_on();}
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
    else {$('#students_limit_massage_status').html('<img src="/static/images/change.png"/>');button_on();}
});

$('#students_limit').focusin(function(){
   $('#students_limit_massage_example').text(' wzor: 10 lub nic, jezeli nie chcesz ustalic limitu');
}).blur(function(){
    $('#students_limit_massage_example').text('');
    var students_limit=$('#students_limit').val();
    button_on();
    var reg = /^([0-9]{0,3})$/;
    if(reg.test(students_limit) == false) {
    $('#students_limit_massage_status').text('Podano zla liczbe '); 
    button_off();}
    else {$('#students_limit_massage_status').html('<img src="/static/images/change.png"/>');button_on();}
});

//end----------------------------------------------


$('#date').datepicker({ minDate: '0d', dateFormat: 'dd/mm/yy',
    showOn: 'button',
    buttonImage: '/static/images/kalendarz.jpg', 
    buttonImageOnly: true,
    onClose: function(){
    
    var date=$('#date').val();
    var reg = /^([0-9]{1,2})+\/([0-9]{1,2})+\/([0-9]{1,4})$/;
    if(reg.test(date) == true){
    button_on();
    $('#expiry_massage_status').html('<img src="/static/images/change.png"/>');
    button_on();
    } else {
            button_off();
            $('#expiry_massage_status').html('');
           };
                                     } })
    });


$('#date').keyup(function(){
    var date=$('#date').val();
    var reg = /^([0-9]{1,2})+\/([0-9]{1,2})+\/([0-9]{1,4})$/;
    if(reg.test(date) == true){
    button_on();
    $('#expiry_massage_status').html('<img src="/static/images/change.png"/>');
    button_on();
    } else {
            button_off();
            $('#expiry_massage_status').html('');
           }
});

$('#date').focusin(function(){
   $('#expiry_massage_example').text('wzor: dd/mm/rrrr (30/12/2012)');
}).blur(function(){
    $('#expiry_massage_example').text('');
    var expiry=$('#date').val();
    button_on();
    var reg = /^([0-9]{1,2})+\/([0-9]{1,2})+\/([0-9]{1,4})$/;
    if(reg.test(expiry) == false) {
    $('#expiry_massage_status').text('wpisano złą datę '); 
    button_off();}
    else {$('#expiry_massage_status').html('<img src="/static/images/change.png"/>');button_on();}
});

$('#date1').click(function(){
 $('#date').val($('#date1b').val());
 button_on();
 $('#expiry_massage_status').html('<img src="/static/images/change.png"/>');
 button_on();
});

$('#date2').click(function(){
 $('#date').val($('#date2b').val());
 button_on();
 $('#expiry_massage_status').html('<img src="/static/images/change.png"/>');
 button_on();
});

$('#date3').click(function(){
 $('#date').val($('#date3b').val());
 button_on();
 $('#expiry_massage_status').html('<img src="/static/images/change.png"/>');
 button_on();
});


