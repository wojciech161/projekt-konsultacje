//function
function button_off(){
        $('#button').removeAttr('class');
        $('#button').attr('disabled','disabled');
        $('#button').attr('style','color:#777777;');
        $('#button').attr('class','button_disabled');
}
function button_on(){
    if($('#login_massage_status').html()=='' && $('#name').val()!='' && $('#name_massage_status').html()=='' && $('#surname').val()!='' && $('#surname_massage_status').html()=='' && $('#login').val()!=''){
        $('#button').removeAttr('class');
        $('#button').removeAttr('disabled');
        $('#button').removeAttr('style');
        $('#button').attr('class','button3');
    }

}
//----------------------------------

$(document).ready(function(){
    
//start-----------------------------------
// sprawdzenie poprawnosci tytulu  
$('#login').keyup(function(){
    var login=$('#login').val();
    button_on();
    var reg = /^([A-ZaACcEeSsZzZzLlOoNna-z]{1,20})+\.([A-ZaACcEeSsZzZNnOnzLla-z]{2,30})$/;
    if(reg.test(login) == false) {
    $('#login_massage_status').text('Login nie jest w postaci: imie.nazwisko'); 
    button_off();}
    else {$('#login_massage_status').text(''); button_on();
     }
});


$('#login').focusin(function(){
   $('#login_massage_example').text(' wzor: imie.nazwisko');
}).blur(function(){
    $('#login_massage_example').text('');
    var login=$('#login').val();
    button_on();
    var reg = /^([A-ZaACcEeSsZzZNnzLlOoa-z]{1,20})+\.([A-ZaACcEeSsZzZzLla-z]{2,30})$/;
    if(reg.test(login) == false) {
    $('#login_massage_status').text('Login nie jest w postaci: imie.nazwisko'); 
    button_off();}
    else {$('#login_massage_status').text(''); }
});

$('#login').focusout(function(){
    $('#login_massage_example').text('');
    var login=$('#login').val();
    button_on();
    var reg = /^([A-ZaACcEeSsZzZNnzLlOoa-z]{1,20})+\.([A-ZaACcEeSsZzZzLla-z]{2,30})$/;
    if(reg.test(login) == false) {
    $('#login_massage_status').text('Login nie jest w postaci: imie.nazwisko'); 
    button_off();}
    else {$('#login_massage_status').text(''); }
});   
//end----------------------------------

//start------------------------------------
// sprawdzenie poprawnosci imienia
$('#name').keyup(function(){
    var name=$('#name').val();
    button_on();
    var reg = /^([A-ZaACcEeSsZzNnOoZzLla-z]{2,20})$/;
    if(reg.test(name) == false) {
    $('#name_massage_status').text('Imie jest niepoprawne'); 
    button_off();}
    else {$('#name_massage_status').text(''); button_on();}
});

$('#name').focusin(function(){
   $('#name_massage_example').text(' wzor: Michal');
   var name=$('#name').val();
    button_on();
    var reg = /^([A-ZaACcEeSsZzNnOoZzLla-z]{2,20})$/;
    if(reg.test(name) == false) {
    $('#name_massage_status').text('Imie jest niepoprawne'); 
    button_off();}
    else $('#name_massage_status').text('');
}).blur(function(){
    $('#name_massage_example').text('');
    var name=$('#name').val();
    button_on();
    var reg = /^([A-ZaACcEeSsZzNnOoZzLla-z]{2,20})$/;
    if(reg.test(name) == false) {
    $('#name_massage_status').text('Imie jest niepoprawne'); 
    button_off();}
    else $('#name_massage_status').text('');
});

$('#name').focusout(function(){
    $('#name_massage_example').text('');
    var name=$('#name').val();
    button_on();
    var reg = /^([A-ZaACcEeSsZzNnOoZzLla-z]{2,20})$/;
    if(reg.test(name) == false) {
    $('#name_massage_status').text('Imie jest niepoprawne'); 
    button_off();}
    else $('#name_massage_status').text('');
});
//end-----------------------------------------

//start---------------------------------------
// sprawdzenie poprawnosci nazwiska
$('#surname').keyup(function(){
    var surname=$('#surname').val();
    button_on();
    var reg = /^([A-ZaACcEeSsZzNnOoZzLla-z]{2,50})$/;
    if(reg.test(surname) == false) {
    $('#surname_massage_status').text('Nazwisko jest niepoprawne'); 
    button_off();}
    else {$('#surname_massage_status').text(''); button_on();}
});

$('#surname').focusin(function(){
   $('#surname_massage_example').text(' wzor: Abacki');
   var surname=$('#surname').val();
    button_on();
    var reg = /^([A-ZaACcEeSsZzNnOoZzLla-z]{2,50})$/;
    if(reg.test(surname) == false) {
    $('#surname_massage_status').text('Nazwisko jest niepoprawne'); 
    button_off();}
    else $('#surname_massage_status').text('');
}).blur(function(){
    $('#surname_massage_example').text('');
    var surname=$('#surname').val();
    button_on();
    var reg = /^([A-ZaACcEeSsZzNnOoZzLla-z]{2,50})$/;
    if(reg.test(surname) == false) {
    $('#surname_massage_status').text('Nazwisko jest niepoprawne'); 
    button_off();}
    else $('#surname_massage_status').text('');
});

$('#surname').focusout(function(){
    $('#surname_massage_example').text('');
    var surname=$('#surname').val();
    button_on();
    var reg = /^([A-ZaACcEeSsZzNnOoZzLla-z]{2,50})$/;
    if(reg.test(surname) == false) {
    $('#surname_massage_status').text('Nazwisko jest niepoprawne'); 
    button_off();}
    else $('#surname_massage_status').text('');
    
});
//end----------------------------------------------


});