#!/usr/bin/perl -w

use warnings;
use strict; 

use CGI::Carp qw(fatalsToBrowser);
use DBI;

print "Content-type: text/html\r\n\r\n";

my $driver   = "Pg";
my $database = "stock";
my $dsn = "DBI:$driver:dbname = $database;host = 127.0.0.1;port = 5432";
my $userid = "postgres";
my $password = "\$postgres";
my $dbh = DBI->connect($dsn, $userid, $password, { RaiseError => 1 })
   or die $DBI::errstr;
#print "Opened database successfully\n";

#my $stmt = qq(SELECT * from stock;);
my $stmt = qq(SELECT column_name FROM information_schema.columns WHERE table_name = 'stock';);

my $sth = $dbh->prepare( $stmt );
my $rv = $sth->execute() or die $DBI::errstr;

my $selection = "*";
my $order  = "id";
my $updown = "ASC";
my $stmt2 = qq(SELECT $selection FROM stock ORDER BY $order $updown;);

my $sth2 = $dbh->prepare( $stmt2 );
my $data = $sth2->execute() or die $DBI::errstr;
$dbh->disconnect();
my $th_str = "";
my $cnt =0;
my $data;

while(my @row = $sth->fetchrow_array()) {
    $th_str .= "<th id=\"th_$row[0]\">$row[0]</th>";
    $data->{$cnt} = $row[0];
    $cnt++;
}


#INSERT INTO stock VALUES (DEFAULT,'345',1,56,'Res','220pF','SOT',0.24);

print qq$

<html>
  <head>
    <title>Lagerbestand</title>
    <link rel="stylesheet" type="text/css" href="styles.css">
  </head>
  <body>
<div>
    <ul class="top-menu-ul">
        <li class="top-menu"> <a class="top-menu" style="color: black" href="/index.html">Home</a></li>
        <li class="top-menu"> <a class="active-top" style="color: white" href="/stock/index.cgi">Lager</a></li>
    </ul>
    <div class="top-menu-select" onclick="topmenuselect()"><a href="#select">&#9776;</a></div>
</div>

<div class="popup" id="Popup">
  <div style="background-color:#595959; height:35px;">  <span class="close_btn" onclick="ClsBtn_Popup()">&times</span></div>
  <div id="popupFrame" style="position: relative;"> 
  </div>
</div>

<div id="list" class="listing" > 

    <table style="margin:auto;">
      <tr id="main_tbl_head">
$;

print $th_str;
print "<th> <img width=\"20px\" src=\"wheel.svg\" onclick=\"Setting_Popup(this,600,500)\"> </th>";

print "</tr>\n";

while(my @row = $sth2->fetchrow_array()) {
 print " <tr id=\"tr_".$row[0]."\">  \n";
    for (my $i=0;$i<8;$i++) {
      if ($row[$i] eq "id") {
        print "<td id=\"td_$data->{$i}\">$row[$i]</td>";
      } else {
        if ($data->{$i} eq "amount" || $data->{$i} eq "place" ){
          print "<td id=\"td_$data->{$i}\" onclick=\"incDec_Popup(this,80,100)\">$row[$i]</td>";
        } elsif ($data->{$i} eq "partnum"){
          print "<td id=\"td_$data->{$i}\" onclick=\"text_Popup(this,100,80)\">$row[$i]</td>";
        } elsif ($data->{$i} eq "type"){
          print "<td id=\"td_$data->{$i}\" onclick=\"select_Popup(this,'type',100,80)\">$row[$i]</td>";
        } elsif ($data->{$i} eq "value"){
          print "<td id=\"td_$data->{$i}\" onclick=\"select_Popup(this,'value',100,80)\">$row[$i]</td>";
        } elsif ($data->{$i} eq "package"){
          print "<td id=\"td_$data->{$i}\" onclick=\"select_Popup(this,'package',100,80)\">$row[$i]</td>";
        } elsif ($data->{$i} eq "price"){
          print "<td id=\"td_$data->{$i}\" onclick=\"indec_money_Popup(this,'type',100,80)\">$row[$i]</td>";
        } else {
          print "<td id=\"td_$data->{$i}\" >$row[$i]</td>";
        }
      }  
    }
print "<td onclick=\"changeAll_Popup(this.parentNode)\"><img width=\"20px\"src=\"sett.svg\"></td>";
print "</tr>\n";
}
print qq$	


    </table>
</div>
    <button onclick="topFunction()" id="myBtn" title="Go to top">Top</button>

  </body>

<script>
document.getElementsByClassName("top-menu-ul")[0].style.marginTop = "0px";

window.onscroll = function() {scrollFunction()};

//--------------------------------------------------------------------------//
//---------------                Basic                   -------------------//
//--------------------------------------------------------------------------//

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("myBtn").style.display = "block";
    } else {
        document.getElementById("myBtn").style.display = "none";
    }
}

function getdata(command,callback) {
  var xmlhttp = null;
  var cb = null;
  xmlhttp=new XMLHttpRequest();
  cb = callback;
  
  xmlhttp.onreadystatechange = function() {
    if(xmlhttp.readyState == 4) {
      if(cb)
        //cb(xmlhttp.responseText);
        alert(xmlhttp.responseText);
      }
    }
  xmlhttp.open("GET",command,true);
  xmlhttp.send(null);
  }   

function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

function topmenuselect(){
  var select = document.getElementsByClassName("top-menu-ul");
  if (select[0].style.marginTop != "0px") {
    select[0].style.marginTop = "0px";
    document.getElementById("list").style.marginTop = "50px";
  } else {
    select[0].style.marginTop = "-50px";
    document.getElementById("list").style.marginTop = "0px";
  }
}


//------------------------------------------------------------------//
//------------------------    Basic Popup    -----------------------//
//------------------------------------------------------------------//

function clearPopup(){
  // delete recursively
  var popup_main = document.getElementById("popupFrame");
  if (popup_main.childNodes.length >1){
    popup_main.removeChild(popup_main.childNodes[1]);
    clearPopup();
  }
}

function ClsBtn_Popup(){
  document.getElementById("Popup").style.visibility = "hidden";
}

function SetMainPopup(width,height) {
  var field   = document.getElementById("Popup");
  var clientW = document.body.clientWidth;
  var clientH = document.body.clientHeight;
  field.style.width  = width;
//  var corrHeight = parseInt(height) + 35;
  field.style.height = parseInt(height)+35;
  field.style.left   = ((clientW - parseInt(field.style.width.slice(0,-2)))/2) +"px";
  field.style.top    = ((parseInt(clientH) - parseInt(field.style.height.slice(0,-2)))/3) +"px";
  field.style.visibility = "visible";
}

//---------------------------------------------------------------------//
//-----------------       changeAll_Popup     -------------------------//
//---------------------------------------------------------------------//

function changeAll_Popup(dom) {
  clearPopup();
  SetMainPopup("600","130");

  var id= dom.id.slice(3);
  var main_tbl_head = document.getElementById("main_tbl_head");
  var popupFrame = document.getElementById("popupFrame");
  var table_node =  document.createElement("table");
  table_node.id="popup_tbl";
  var tr_node =  document.createElement("tr");

  for (var i=1; i<(main_tbl_head.childNodes.length - 1);i++){
    var th_node = document.createElement("th");
    th_node.innerHTML = main_tbl_head.childNodes[i].innerHTML;
    tr_node.appendChild(th_node);
  }
  table_node.appendChild(tr_node);

  tr_node =  document.createElement("tr");
  for (var i=1; i<(dom.childNodes.length - 1);i++){ 
    var td_node = document.createElement("td");

    //insert input fields in rows. Not in case of id.
    if (main_tbl_head.childNodes[i].innerHTML !== "id") {
      var input = document.createElement("input");
      input.style.width="50px";
      input.type="text";
      input.value= dom.childNodes[i].innerHTML;      
      td_node.appendChild(input);
    } else {
      td_node.innerHTML = dom.childNodes[i].innerHTML;
    }   
    tr_node.appendChild(td_node);
  }

  table_node.appendChild(tr_node);  
  popupFrame.appendChild(table_node);
  document.getElementById("popup_tbl").style.position="relative";
  document.getElementById("popup_tbl").style.top="10px";
  document.getElementById("popup_tbl").style.left = ((document.getElementById("popupFrame").clientWidth - document.getElementById("popup_tbl").clientWidth)/2)+"px";

  
  //Button for Sending changes
  var btn_node= document.createElement("input");
  btn_node.type = "button";
  btn_node.value="change";
  btn_node.className="SendBtn";
  btn_node.style.marginRight=  document.getElementById("popup_tbl").style.left;
  btn_node.onclick= function (e) {
                send_btn_UpdateAll_Popup(this.parentNode);
                document.getElementById("Popup").style.visibility = "hidden";
            };
  popupFrame.appendChild(btn_node);  
}


function send_btn_UpdateAll_Popup(dom) {
  var str ="";
  var tr = dom.childNodes[1].childNodes[1];
  for (var i=0; i<(tr.childNodes.length);i++){
    if ( tr.childNodes[i].firstChild.nodeName == "INPUT" ) {   
      if ( i===(tr.childNodes.length-1)) { 
        str += tr.childNodes[i].firstChild.value.slice(1)+"-";
      } else {
        str += tr.childNodes[i].firstChild.value+"-";
      }
    } else {
      str += tr.childNodes[i].innerHTML+"-";
    }
  }
  getdata('updatedb_all.cgi?'+str,topFunction());
}

//---------------------------------------------------------------//
//----               Increase/Decrease Popup           ----------//
//---------------------------------------------------------------//

function incDec_Popup(dom,width,height){
  clearPopup();

  var table_node =  document.createElement("table");
  table_node.id="popup_tbl";
  table_node.className="UpDownTabl";
  var tr_node = document.createElement("tr");
  tr_node.className="UpDownTabl";

  var td_node = document.createElement("td");
  td_node.className="UpDownTabl";

  var input = document.createElement("input");
  input.style.width ="50px";
  input.style.height="50px";
  input.type="text";
  input.value= dom.innerHTML;
  input.style.textAlign="center";
  td_node.appendChild(input);
  td_node.rowSpan="2";

  tr_node.appendChild(td_node);
  var td_node2 = document.createElement("td");
  td_node2.innerHTML='&#9650;';
  td_node2.onclick= function (e) {
                inc(this);
            };
  td_node2.className="UpDownTabl";

  tr_node.appendChild(td_node2);

  var tr_node2 = document.createElement("tr");
  var td_node3 = document.createElement("td");
  td_node3.innerHTML='&#9660;';
  td_node3.onclick= function (e) {
                dec(this);
            };

  td_node3.className="UpDownTabl";
  
  tr_node2.appendChild(td_node3);
  tr_node2.className="UpDownTabl";
 
  table_node.appendChild(tr_node);
  table_node.appendChild(tr_node2);
  popupFrame.appendChild(table_node);

  var btn_node= document.createElement("input");
  btn_node.type = "button";
  btn_node.value= "change";
  btn_node.className="SendBtn";
  btn_node.onclick= function (e) {
                send_btn_decinc(this.parentNode);
            };
  btn_node.style.marginTop="0px";
  popupFrame.appendChild(btn_node);
  var newWidth = document.getElementById("popup_tbl").clientWidth;
  var newHeight = document.getElementById("popup_tbl").clientHeight;
  SetMainPopup(newWidth,newHeight+30);
}

function inc(dom){
               var inp = dom.parentNode.firstChild.firstChild.value;
               var val = (parseInt(inp)+1);
               dom.parentNode.firstChild.firstChild.value = val;	
}

function dec(dom){
               var inp = dom.parentNode.parentNode.firstChild.firstChild.firstChild.value;
               var val = (parseInt(inp)-1);
 	       if (val >= 0){
                 dom.parentNode.parentNode.firstChild.firstChild.firstChild.value = val;
               } else {
                 dom.parentNode.parentNode.firstChild.firstChild.firstChild.value = "0";
               }
}

function send_btn_decinc(dom) {
  var str ="";
//  getdata('updatedb.cgi?'+str,topFunction());
alert("TEST");
}

//--------------------------------------------------------------------------------------//
//---------------------      Setting_Popup        --------------------------------------//
//--------------------------------------------------------------------------------------//

function Setting_Popup(dom,width,height){
  clearPopup();

  var table_node =  document.createElement("table");
  table_node.id="popup_tbl";
  table_node.className="UpDownTabl";
  var tr_node = document.createElement("tr");
  tr_node.className="UpDownTabl";

  var td_node = document.createElement("td");
  td_node.className="UpDownTabl";

  var input = document.createElement("input");
  input.style.width ="50px";
  input.style.height="50px";
  input.type="text";
  input.value= dom.innerHTML;
  input.style.textAlign="center";
  td_node.appendChild(input);
  td_node.rowSpan="2";

  tr_node.appendChild(td_node);
  var td_node2 = document.createElement("td");
  td_node2.innerHTML='&#9650;';
  td_node2.onclick= function (e) {
                inc(this);
            };
  td_node2.className="UpDownTabl";

  tr_node.appendChild(td_node2);

  var tr_node2 = document.createElement("tr");
  var td_node3 = document.createElement("td");
  td_node3.innerHTML='&#9660;';
  td_node3.onclick= function (e) {
                dec(this);
            };

  td_node3.className="UpDownTabl";
  
  tr_node2.appendChild(td_node3);
  tr_node2.className="UpDownTabl";
 
  table_node.appendChild(tr_node);
  table_node.appendChild(tr_node2);
  popupFrame.appendChild(table_node);

  var btn_node= document.createElement("input");
  btn_node.type = "button";
  btn_node.value= "change";
  btn_node.className="SendBtn";
  btn_node.onclick= function (e) {
                send_btn_decinc(this.parentNode);
            };
  btn_node.style.marginTop="0px";
  popupFrame.appendChild(btn_node);
  //var newWidth = document.getElementById("popup_tbl").clientWidth;
  //var newHeight = document.getElementById("popup_tbl").clientHeight;
  //SetMainPopup(newWidth,newHeight+30);
  SetMainPopup(width,height);
}

//--------------------------------------------------------------------------------------//
//---------------------         Text_Popup        --------------------------------------//
//--------------------------------------------------------------------------------------//

function text_Popup(dom,width,height){
  clearPopup();

  var table_node =  document.createElement("table");
  table_node.id="popup_tbl";
  var tr_node = document.createElement("tr");
  var td_node = document.createElement("td");
  td_node.className="UpDownTabl";

  var input = document.createElement("input");
  input.style.width ="100%";
  input.style.height="34px";
  input.type="text";
  input.style.fontSize="16";
  input.value= dom.innerHTML;
  input.style.textAlign="center";
  td_node.appendChild(input);
  tr_node.appendChild(td_node);
  table_node.appendChild(tr_node);
  popupFrame.appendChild(table_node);

  var btn_node= document.createElement("input");
  btn_node.type = "button";
  btn_node.value= "change";
  btn_node.className="SendBtn";
  btn_node.onclick= function (e) {
                send_btn_decinc(this.parentNode);
            };
  btn_node.style.marginTop="0px";
  popupFrame.appendChild(btn_node);
  //var newWidth = document.getElementById("popup_tbl").clientWidth;
  //var newHeight = document.getElementById("popup_tbl").clientHeight;
  //SetMainPopup(newWidth,newHeight+30);
  SetMainPopup(width,height);
}

//--------------------------------------------------------------------------------------//
//---------------------         Select_Popup        --------------------------------------//
//--------------------------------------------------------------------------------------//

function select_Popup(dom,type,width,height){
  clearPopup();

  // Call getScript to get all kinds of values for a type.
  // returns all kinds which will be put here...

  var table_node =  document.createElement("table");
  table_node.id="popup_tbl";
  table_node.style.width="100%";
  var tr_node = document.createElement("tr");
  var td_node = document.createElement("td");
  td_node.className="UpDownTabl";
  td_node.style.width="100%";

  var sel = document.createElement("SELECT");
  sel.style.width ="100%";
  sel.style.height="38px";

// loop over all returned kinds/values
  var opt = document.createElement("OPTION");
  opt.value= dom.innerHTML;
  opt.innerHTML= dom.innerHTML;
  sel.appendChild(opt);

  opt = document.createElement("OPTION");
  opt.value= "TEST";
  opt.innerHTML= "TEST";
  sel.appendChild(opt);

// end loop

  sel.style.textAlign="center";
  td_node.appendChild(sel);
  tr_node.appendChild(td_node);
  table_node.appendChild(tr_node);
  popupFrame.appendChild(table_node);

  var btn_node= document.createElement("input");
  btn_node.type = "button";
  btn_node.value= "change";
  btn_node.className ="SendBtn";
  btn_node.onclick = function (e) {
                send_btn_decinc(this.parentNode);
            };
  btn_node.style.marginTop="0px";
  popupFrame.appendChild(btn_node);
  //var newWidth = document.getElementById("popup_tbl").clientWidth;
  //var newHeight = document.getElementById("popup_tbl").clientHeight;
  //SetMainPopup(newWidth,newHeight+30);
  SetMainPopup(width,height);
}




</script>
</html>

$;

