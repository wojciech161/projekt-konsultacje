//function
function button_off(){
        $('#button').removeAttr('class');
        $('#button').attr('disabled','disabled');
        $('#button').attr('style','color:#777777;');
        $('#button').attr('class','button_disabled');
}
function button_on(){
    if($('#date_name1_status').text()=='' && $('#date_name2_status').text()=='' && $('#date_name3_status').text()=='' && $('#date_value1_status').text()=='' && $('#date_value2_status').text()=='' && $('#date_value3_status').text()=='' && ($('#date_name1').val().length!=0 || $('#date_name2').val().length!=0 || $('#date_name3').val().length!=0 )){
        $('#button').removeAttr('class');
        $('#button').removeAttr('disabled');
        $('#button').removeAttr('style');
        $('#button').attr('class','button3');
    } 
    else button_off();
}
//----------------------------------


$(document).ready(function(){

$('#date_value3').datepicker({ minDate: '0d', dateFormat: 'dd/mm/yy',
    showOn: 'button',
    buttonImage: '/static/images/kalendarz.jpg', 
    buttonImageOnly: true,
    onClose: function(){
    
    var date_value3=$('#date_value3').val();
    var reg = /^([0-9]{1,2})+\/([0-9]{1,2})+\/([0-9]{1,4})$/;
    if(reg.test(date_value3) == true){
    button_on();
    $('#date_value3_status').html('');
    button_on();
    } else {
            button_off();
            $('#date_value3_status').html('');
           };
                                     } });
                                     


$('#date_value2').datepicker({ minDate: '0d', dateFormat: 'dd/mm/yy',
    showOn: 'button',
    buttonImage: '/static/images/kalendarz.jpg', 
    buttonImageOnly: true,
    onClose: function(){
    
    var date_value2=$('#date_value2').val();
    var reg = /^([0-9]{1,2})+\/([0-9]{1,2})+\/([0-9]{1,4})$/;
    if(reg.test(date_value3) == true){
    button_on();
    $('#date_value2_status').html('');
    button_on();
    } else {
            button_off();
            $('#date_value2_status').html('');
           };
                                     } });
                                     
                                     

$('#date_value1').datepicker({ minDate: '0d', dateFormat: 'dd/mm/yy',
    showOn: 'button',
    buttonImage: '/static/images/kalendarz.jpg', 
    buttonImageOnly: true,
    onClose: function(){
    var date_value1=$('#date_value1').val();
    var reg = /^([0-9]{1,2})+\/([0-9]{1,2})+\/([0-9]{1,4})$/;
    if(reg.test(date_value1) == true){
    button_on();
    $('#date_value1_status').html('');
    button_on();
    } else {
            button_off();
            $('#date_value1_status').html('wpisano złą date ');
           };
                                     } });
                                     
    });


$('#date_value1').keyup(function(){
    var date_value1=$('#date_value1').val();
    var reg = /^([0-9]{1,2})+\/([0-9]{1,2})+\/([0-9]{1,4})$/;
    if(reg.test(date_value1) == true){
    button_on();
    $('#date_value1_status').html('');
    button_on();
    } else {
            button_off();
            $('#date_value1_status').text('wpisano złą date ');
           }
});

$('#date_value1').focusin(function(){
   $('#date_value1_example').text('wzor: dd/mm/rrrr (30/12/2012)');
}).blur(function(){
    $('#date_value1_example').text('');
    var expiry=$('#date_value1').val();
    button_on();
    var reg = /^([0-9]{1,2})+\/([0-9]{1,2})+\/([0-9]{1,4})$/;
    if(reg.test(expiry) == false) {
    $('#date_value1_status').text('wpisano złą date '); 
    button_off();}
    else {$('#date_value1_status').html('');button_on();}
});


//////

$('#date_value2').keyup(function(){
    var date_value2=$('#date_value2').val();
    var reg = /^([0-9]{1,2})+\/([0-9]{1,2})+\/([0-9]{1,4})$/;
    if(reg.test(date_value2) == true){
    button_on();
    $('#date_value2_status').html('');
    button_on();
    } else {
            button_off();
            $('#date_value2_status').text('wpisano złą date ');
           }
});

$('#date_value2').focusin(function(){
   $('#date_value2_example').text('wzor: dd/mm/rrrr (30/12/2012)');
}).blur(function(){
    $('#date_value2_example').text('');
    var expiry=$('#date_value2').val();
    button_on();
    var reg = /^([0-9]{1,2})+\/([0-9]{1,2})+\/([0-9]{1,4})$/;
    if(reg.test(expiry) == false) {
    $('#date_value2_status').text('wpisano złą date '); 
    button_off();}
    else {$('#date_value2_status').html('');button_on();}
});

////

$('#date_value3').keyup(function(){
    var date_value3=$('#date_value3').val();
    var reg = /^([0-9]{1,2})+\/([0-9]{1,2})+\/([0-9]{1,4})$/;
    if(reg.test(date_value3) == true){
    button_on();
    $('#date_value3_status').text('');
    button_on();
    } else {
            button_off();
            $('#date_value3_status').text('wpisano złą date ');
           }
});

$('#date_value3').focusin(function(){
   $('#date_value3_example').text('wzor: dd/mm/rrrr (30/12/2012)');
}).blur(function(){
    $('#date_value3_example').text('');
    var expiry=$('#date_value3').val();
    button_on();
    var reg = /^([0-9]{1,2})+\/([0-9]{1,2})+\/([0-9]{1,4})$/;
    if(reg.test(expiry) == false) {
    $('#date_value3_status').text('wpisano złą date '); 
    button_off();}
    else {$('#date_value3_status').html('');button_on();}
});


////





// sprawdzenie poprawnosci data1
$('#date_name1').keyup(function(){
    var date_name1=$('#date_name1').val();
    button_on();
    var reg = /^([A-ZaACcEeSsZzNnOoZzLla-z\s]{0,50})$/;
    if(reg.test(date_name1) == false) {
    $('#date_name1_status').text('Zła nazwa daty'); 
    button_off();}
    else {$('#date_name1_status').html('');button_on();}
});

$('#date_name1').focusin(function(){
}).blur(function(){
    $('#date_name1_example').text('');
    var date_name1=$('#date_name1').val();
    button_on();
    var reg = /^([A-ZaACcEeSsZzNnOoZzLla-z\s]{0,50})$/;
    if(reg.test(date_name1) == false) {
    $('#date_name1_status').text('Zła nazwa daty'); 
    button_off();}
    else {$('#date_name1_status').html('');button_on();}
});

//end----------------------------------------------

// sprawdzenie poprawnosci data2
$('#date_name2').keyup(function(){
    var date_name2=$('#date_name2').val();
    button_on();
    var reg = /^([A-ZaACcEeSsZzNnOoZzLla-z\s]{0,50})$/;
    if(reg.test(date_name2) == false) {
    $('#date_name2_status').text('Zła nazwa daty'); 
    button_off();}
    else {$('#date_name2_status').html('');button_on();}
});

$('#date_name2').focusin(function(){
}).blur(function(){
    $('#date_name2_example').text('');
    var date_name2=$('#date_name2').val();
    button_on();
    var reg = /^([A-ZaACcEeSsZzNnOoZzLla-z\s]{0,50})$/;
    if(reg.test(date_name2) == false) {
    $('#date_name2_status').text('Zła nazwa daty'); 
    button_off();}
    else {$('#date_name2_status').html('');button_on();}
});

//end----------------------------------------------

// sprawdzenie poprawnosci data3
$('#date_name3').keyup(function(){
    var date_name3=$('#date_name3').val();
    button_on();
    var reg = /^([A-ZaACcEeSsZzNnOoZzLla-z\s]{0,50})$/;
    if(reg.test(date_name3) == false) {
    $('#date_name3_status').text('Zła nazwa daty'); 
    button_off();}
    else {$('#date_name3_status').html('');button_on();}
});

$('#date_name3').focusin(function(){
}).blur(function(){
    $('#date_name3_example').text('');
    var date_name3=$('#date_name3').val();
    button_on();
    var reg = /^([A-ZaACcEeSsZzNnOoZzLla-z\s]{0,50})$/;
    if(reg.test(date_name3) == false) {
    $('#date_name3_status').text('Zła nazwa daty'); 
    button_off();}
    else {$('#date_name3_status').html('');button_on();}
});

//end----------------------------------------------




