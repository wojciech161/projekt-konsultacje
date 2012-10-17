//function
function button_off(){
        $('#button').removeAttr('class');
        $('#button').attr('disabled','disabled');
        $('#button').attr('style','color:#777777;');
        $('#button').attr('class','button_disabled');
}
function button_on(){
    if($('#login_massage_status').html()=='' && $('#name').val()!='' && $('#name_massage_status').html()=='' && $('#surname').val()!='' && $('#surname_massage_status').html()=='' && $('#degree').val()!='' && $('#degree_massage_status').html()=='' && $('#instytute').val()!='' && $('#instytute_massage_status').html()=='' && $('#building').val()!='' && $('#building_massage_status').html()=='' && $('#room').val()!='' && $('#room_massage_status').html()=='' && $('#login').val()!='' && $('#email').val()!='' && $('#email_massage_status').html()=='' && $('#www_massage_status').html()=='' && $('#phone_massage_status').html()==''){
        $('#button').removeAttr('class');
        $('#button').removeAttr('disabled');
        $('#button').removeAttr('style');
        $('#button').attr('class','button3');
    }

}
//----------------------------------

$(document).ready(function(){
    
//start-----------------------------------
// sprawdzenie poprawności tytułu  
$('#login').keyup(function(){
    var login=$('#login').val();
    button_on();
    var reg = /^([A-ZąĄĆćĘęŚśŻżŹźŁłÓóŃńa-z]{1,20})+\.([A-ZąĄĆćĘęŚśŻżŹźŁła-z]{2,30})$/;
    if(reg.test(login) == false) {
    $('#login_massage_status').text('Login nie jest w postaci: imie.nazwisko'); 
    button_off();}
    else {$('#login_massage_status').text(''); button_on();
     }
});


$('#login').focusin(function(){
   $('#login_massage_example').text(' wzór: imie.nazwisko');
}).blur(function(){
    $('#login_massage_example').text('');
    var login=$('#login').val();
    button_on();
    var reg = /^([A-ZąĄĆćĘęŚśŻżŹŃńźŁłÓóa-z]{1,20})+\.([A-ZąĄĆćĘęŚśŻżŹźŁła-z]{2,30})$/;
    if(reg.test(login) == false) {
    $('#login_massage_status').text('Login nie jest w postaci: imie.nazwisko'); 
    button_off();}
    else {$('#login_massage_status').text(''); }
});
//end----------------------------------

//start-----------------------------------
// sprawdzenie poprawności tytułu  
$('#degree').keyup(function(){
    var degree=$('#degree').val();
    button_on();
    var reg = /^([A-ZąĄĆćĘęŚśŻżŃńŹźÓóŁła-z. ]{2,40})$/;
    if(reg.test(degree) == false) {
    $('#degree_massage_status').text('Tytul jest niepoprawny'); 
    button_off();}
    else {$('#degree_massage_status').text(''); button_on()}
});

$('#degree').focusin(function(){
   $('#degree_massage_example').text(' wzór: dr inż.');
    var degree=$('#degree').val();
    button_on();
    var reg = /^([A-ZąĄĆćĘęŚśŻżŃńŹźÓóŁła-z. ]{2,40})$/;
    if(reg.test(degree) == false) {
    $('#degree_massage_status').text('Tytul jest niepoprawny'); 
    button_off();}
    else $('#degree_massage_status').text('');
    
}).blur(function(){
    $('#degree_massage_example').text('');
    var degree=$('#degree').val();
    button_on();
    var reg = /^([A-ZąĄĆćĘęŚśŻżŃńŹźÓóŁła-z. ]{2,40})$/;
    if(reg.test(degree) == false) {
    $('#degree_massage_status').text('Tytul jest niepoprawny'); 
    button_off();}
    else $('#degree_massage_status').text('');
});
//end----------------------------------

//start------------------------------------
// sprawdzenie poprawności imienia
$('#name').keyup(function(){
    var name=$('#name').val();
    button_on();
    var reg = /^([A-ZąĄĆćĘęŚśŻżŃńÓóŹźŁła-z]{2,20})$/;
    if(reg.test(name) == false) {
    $('#name_massage_status').text('Imię jest niepoprawne'); 
    button_off();}
    else {$('#name_massage_status').text(''); button_on();}
});

$('#name').focusin(function(){
   $('#name_massage_example').text(' wzór: Michał');
   var name=$('#name').val();
    button_on();
    var reg = /^([A-ZąĄĆćĘęŚśŻżŃńÓóŹźŁła-z]{2,20})$/;
    if(reg.test(name) == false) {
    $('#name_massage_status').text('Imię jest niepoprawne'); 
    button_off();}
    else $('#name_massage_status').text('');
}).blur(function(){
    $('#name_massage_example').text('');
    var name=$('#name').val();
    button_on();
    var reg = /^([A-ZąĄĆćĘęŚśŻżŃńÓóŹźŁła-z]{2,20})$/;
    if(reg.test(name) == false) {
    $('#name_massage_status').text('Imię jest niepoprawne'); 
    button_off();}
    else $('#name_massage_status').text('');
});
//end-----------------------------------------

//start---------------------------------------
// sprawdzenie poprawności nazwiska
$('#surname').keyup(function(){
    var surname=$('#surname').val();
    button_on();
    var reg = /^([-A-ZąĄĆćĘęŚśŻżŃńÓóŹźŁła-z-]{2,50})$/;
    if(reg.test(surname) == false) {
    $('#surname_massage_status').text('Nazwisko jest niepoprawneAA'); 
    button_off();}
    else {$('#surname_massage_status').text(''); button_on();}
});

$('#surname').focusin(function(){
   $('#surname_massage_example').text(' wzór: Kowalski');
   var surname=$('#surname').val();
    button_on();
    var reg = /^([-A-ZąĄĆćĘęŚśŻżŃńÓóŹźŁła-z-]{2,50})$/;
    if(reg.test(surname) == false) {
    $('#surname_massage_status').text('Nazwisko jest niepoprawne'); 
    button_off();}
    else $('#surname_massage_status').text('');
}).blur(function(){
    $('#surname_massage_example').text('');
    var surname=$('#surname').val();
    button_on();
    var reg = /^([-A-ZąĄĆćĘęŚśŻżŃńÓóŹźŁła-z-]{2,50})$/;
    if(reg.test(surname) == false) {
    $('#surname_massage_status').text('Nazwisko jest niepoprawne'); 
    button_off();}
    else $('#surname_massage_status').text('');
});

//end----------------------------------------------

//start---------------------------------------
// sprawdzenie poprawności nazwiska
$('#instytute').keyup(function(){
    var instytute=$('#instytute').val();
    button_on();
    var reg = /^([A-ZąĄĆćĘęŚśŻżŹźŃńŁła-z\-]{3,6})$/;
    var instytute = $('#instytute').val();
    if(reg.test(instytute) == false) {
    $('#instytute_massage_status').text('Nazwa instytutu jest niepoprawna'); 
    button_off();}
    else {$('#instytute_massage_status').text(''); button_on();}
});

$('#instytute').focusin(function(){
   $('#instytute_massage_example').text(' wzór: iiar');
}).blur(function(){
    $('#instytute_massage_example').text('');
    var instytute=$('#instytute').val();
    button_on();
    var reg = /^([A-ZąĄĆćĘęŚśŻżŹźŃńŁła-z\-]{3,6})$/;
    var instytute = $('#instytute').val();
    if(reg.test(instytute) == false) {
    $('#instytute_massage_status').text('Nazwa instytutu jest niepoprawna'); 
    button_off();}
    else {$('#instytute_massage_status').text(''); button_on(); }
});

//end----------------------------------------------

//start---------------------------------------
// sprawdzenie poprawności nazwiska
$('#building').keyup(function(){
    var building=$('#building').val();
    button_on();
    var reg = /^([A-ZĄĆĘŚŻŹŁŃÓ]{1,1})+\-([0-9]{1,4})$/;
    if(reg.test(building) == false) {
    $('#building_massage_status').text('Nazwa budynku jest niepoprawna'); 
    button_off();}
    else {$('#building_massage_status').text('');button_on();}
});

$('#building').focusin(function(){
   $('#building_massage_example').text(' wzór: C-1');
   $('#building_massage_example').text('');
    var building=$('#building').val();
    button_on();
    var reg = /^([A-ZĄĆĘŚŻŹŁŃÓ]{1,1})+\-([0-9]{1,4})$/;
    if(reg.test(building) == false) {
    $('#building_massage_status').text('Nazwa budynku jest niepoprawna'); 
    button_off();}
    else $('#building_massage_status').text('');
}).blur(function(){
    $('#building_massage_example').text('');
    var building=$('#building').val();
    button_on();
    var reg = /^([A-ZĄĆĘŚŻŹŁŃÓs]{1,1})+\-([0-9]{1,4})$/;
    if(reg.test(building) == false) {
    $('#building_massage_status').text('Nazwa budynku jest niepoprawna'); 
    button_off();}
    else $('#building_massage_status').text('');
    
});

//end----------------------------------------------

//start---------------------------------------
// sprawdzenie poprawności nazwiska
$('#room').keyup(function(){
    var room=$('#room').val();
    button_on();
    var reg = /^([0-9A-Za-z]{1,4})$/;
    if(reg.test(room) == false) {
    $('#room_massage_status').text('Wprowadzono niepoprawny pokój'); 
    button_off();}
    else {$('#room_massage_status').text(''); button_on();}
});

$('#room').focusin(function(){
   $('#room_massage_example').text(' wzór: 123');
    var room=$('#room').val();
    button_on();
    var reg = /^([0-9A-Za-z]{1,4})$/;
    if(reg.test(room) == false) {
    $('#room_massage_status').text('Wprowadzono niepoprawny pokój'); 
    button_off();}
    else $('#room_massage_status').text('');
}).blur(function(){
    $('#room_massage_example').text('');
    var room=$('#room').val();
    button_on();
    var reg = /^([0-9A-Z]{1,4})$/;
    if(reg.test(room) == false) {
    $('#room_massage_status').text('Wprowadzono niepoprawny pokój'); 
    button_off();}
    else $('#room_massage_status').text('');
});

//end----------------------------------------------

//start---------------------------------------
// sprawdzenie poprawności nazwiska
$('#phone').keyup(function(){
    var phone=$('#phone').val();
    button_on();
    if(phone!=''){
    var reg = /^\(+\++([0-9 ]{5,7})+\)+([0-9\-]{5,11})$/;
    if(reg.test(phone) == false) {
    $('#phone_massage_status').text('Numer telefonu jest niepoprawny'); 
    button_off();}
    else {$('#phone_massage_status').text(''); button_on();}
    }
    else $('#phone_massage_status').text('');
});

$('#phone').focusin(function(){
   $('#phone_massage_example').text(' wzór: (+48 71)320-22-79');
    var phone=$('#phone').val();
    button_on();
    if(phone!=''){
    var reg = /^\(+\++([0-9 ]{5,7})+\)+([0-9\-]{5,11})$/;
    if(reg.test(phone) == false) {
    $('#phone_massage_status').text('Numer telefonu jest niepoprawny'); 
    button_off();}
    else {$('#phone_massage_status').text(''); button_on();}
    }
}).blur(function(){
    $('#phone_massage_example').text('');
    var phone=$('#phone').val();
    button_on();
    if(phone!=''){
    var reg = /^\(+\++([0-9 ]{5,7})+\)+([0-9\-]{5,11})$/;
    if(reg.test(phone) == false) {
    $('#phone_massage_status').text('Numer telefonu jest niepoprawny'); 
    button_off();}
    else $('#phone_massage_status').text('');
    }
    else $('#phone_massage_status').text('');
});

//end----------------------------------------------

//start---------------------------------------
// sprawdzenie poprawności nazwiska
$('#email').keyup(function(){
    var email=$('#email').val();
    button_on();
    var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    if(reg.test(email) == false) {
    $('#email_massage_status').text('Wprowadzony zły adres'); 
    button_off();}
    else {$('#email_massage_status').text(''); button_on();}
});

$('#email').focusin(function(){
   $('#email_massage_example').text(' wzór: imie.nazwisko@pwr.wroc.pl');
    var email=$('#email').val();
    button_on();
    var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    if(reg.test(email) == false) {
    $('#email_massage_status').text('Wprowadzony zły adres'); 
    button_off();}
    else {$('#email_massage_status').text(''); button_on();}  
}).blur(function(){
    $('#email_massage_example').text('');
    var email=$('#email').val();
    button_on();
    var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    if(reg.test(email) == false) {
    $('#email_massage_status').text('Wprowadzony zły adres'); 
    button_off();}
    else $('#email_massage_status').text('');
});

//end----------------------------------------------

//start---------------------------------------
// sprawdzenie poprawności nazwiska
$('#www').keyup(function(){
    var www=$('#www').val();
    button_on();
    if(www!=''){
    button_on(); }
});

$('#www').focusin(function(){
   $('#www_massage_example').text(' wzór: www.xxx.yy');
    var www=$('#www').val();
    button_on();
    if(www!=''){
    button_on(); }
}).blur(function(){
    $('#www_massage_example').text('');
    var www=$('#www').val();
    button_on();
    if(www!=''){
    button_on(); }
});
//end----------------------------------------------


});
