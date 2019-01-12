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
    $th_str .= "<th id=\"th_$row[0]\">$row[0]";
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
  <div id="Popupheader" style="background-color:#595959; height:35px;"><span id="popup_name_field" class="popup_name_field">TEST_NAME</span>  <span class="close_btn" onclick="ClsBtn_Popup()">&times</span></div>
  <div id="popupFrame" style="position: relative;">   </div>
  <div id="scaleBL" style="position:absolute;border-radius:5px; background-color:#c6c6c6;z-index:99;width:7px;height:7px;bottom:0px;cursor:ne-resize;"></div>
  <div id="scaleBR" style="position:absolute;border-radius:5px; right:0px; background-color:#c6c6c6;z-index:99;width:7px;height:7px;bottom:0px;cursor:nw-resize;"></div>
</div>

<div id="list" class="listing" > 

    <table style="margin:auto;">
      <tr id="main_tbl_head">
$;

print $th_str;
print "<th> <img width=\"20px\" src=\"wheel.svg\" onclick=\"Setting_Popup(this,600,500)\">";

print "\n";

while(my @row = $sth2->fetchrow_array()) {
 print " <tr id=\"tr_".$row[0]."\">";
    for (my $i=0;$i<8;$i++) {
      if ($row[$i] eq "id") {
        print "<td id=\"td_$data->{$i}\">$row[$i]";
      } else {
        if ($data->{$i} eq "amount" || $data->{$i} eq "place" ){
          print "<td id=\"td_$data->{$i}\" onclick=\"incDec_Popup(this,80,100)\">$row[$i]";
        } elsif ($data->{$i} eq "partnum"){
          print "<td id=\"td_$data->{$i}\" onclick=\"text_Popup(this,100,80)\">$row[$i]";
        } elsif ($data->{$i} eq "type"){
          print "<td id=\"td_$data->{$i}\" onclick=\"getdata_2('getSelection.cgi',select_Popup,this,'type',100,80)\">$row[$i]";
        } elsif ($data->{$i} eq "value"){
          print "<td id=\"td_$data->{$i}\" onclick=\"getdata_2('getSelection.cgi',select_Popup,this,'value',100,80)\">$row[$i]";
        } elsif ($data->{$i} eq "package"){
          print "<td id=\"td_$data->{$i}\" onclick=\"select_Popup(this,'package',100,80)\">$row[$i]</td>";
        } elsif ($data->{$i} eq "price"){
          print "<td id=\"td_$data->{$i}\" onclick=\"indec_money_Popup(this,'type',100,80)\">$row[$i]";
        } else {
          print "<td id=\"td_$data->{$i}\" >$row[$i]";
        }
      }  
    }
print "<td onclick=\"changeAll_Popup(this.parentNode)\"><img width=\"20px\"src=\"sett.svg\">";
print "\n";
}
print qq$	


    </table>
</div>
    <button onclick="topFunction()" id="myBtn" title="Go to top">Top</button>
    
    <label class="switchBtn">
      <input type="checkbox" onclick="showSearch()" id="SearchBtnInp" title="Search" checked="false"></input>
      <div id="SearchBtn" class="SearchBtn"">
        <img style="float : right;height: 25px;" src="search.svg">
      </div>
      <div class="SearchBlock">
        <input style="width:auto;height:25px; opacity:1"></input>
        <input type="button" value="Search" class="SendBtn" style="left:auto;height:25px;width:auto; opacity:1" >
      </div>
    </label> 
  </body>

<script>
var data_type;
var data_values;
var data_typeValPack;
var type = [];
var valueAddEntry = [];
document.getElementsByClassName("top-menu-ul")[0].style.marginTop = "0px";

window.onscroll = function() {scrollFunction()};

dragElement(document.getElementById("Popup"));

scaleElement(document.getElementById("scaleBL"));
scaleElement(document.getElementById("scaleBR"));


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
      if(cb) cb(xmlhttp.responseText);
      }
  }
  xmlhttp.open("GET",command,true);
  xmlhttp.send(null);
  }   

function getdata_2(command,callback,a,b,status,c,d) {
  var xmlhttp = null;
  var cb = null;  
  if (b){
  command = command+"?"+b;
    if (b == 'value') {
      var type = a.parentNode.childNodes[5].innerHTML; // get type of field "type"
      command = command +"-"+type;
    }
  }
//  alert(command);
  xmlhttp=new XMLHttpRequest();
  cb = callback;  
  xmlhttp.onreadystatechange = function() {
    if(xmlhttp.readyState == 4) {
      if (cb){
        cb(xmlhttp.responseText,a,b,status,c,d);
      }
    }
  }
  xmlhttp.open("GET",command,true);
  xmlhttp.send(null);
}   

/*function getTypeValPack(command,callback) {
  var xmlhttp = null;
  var cb = null;  
  xmlhttp=new XMLHttpRequest();
  cb = callback;  
  xmlhttp.onreadystatechange = function() {
    if(xmlhttp.readyState == 4) {
      if (cb){
        cb(xmlhttp.responseText);
      }
    }
  }
  xmlhttp.open("GET",command,true);
  xmlhttp.send(null);
}   
*/

function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

function topmenuselect(){
  var select = document.getElementsByClassName("top-menu-ul");
  if (select[0].style.marginTop != "0px") {
    select[0].style.marginTop = "0px";
    document.getElementById("list").style.marginTop = "0px";
  } else {
    select[0].style.marginTop = "-50px";
    document.getElementById("list").style.marginTop = "0px";
  }
}

function refreshMainList(d){
  var data;
  data = JSON.parse(d);
  var datasize = data.length;
  deleteMainListEntrys();

  for (var i in data){
    if (i !== 'title') {
      createMainListEntrys(i,data[i]);
    }
  }
}

function deleteMainListEntrys(){
  var nodeMain = document.getElementById("list").childNodes[1].childNodes[1];
  var node = document.getElementById("list").childNodes[1].childNodes[1].childNodes;
  var nodeLength = node.length;
  for (var i=(nodeLength-1); i>0;i--){
    nodeMain.removeChild(node[i]);
  }
}

function createMainListEntrys(id, data, MainNodeId){
  if (!MainNodeId) MainNodeId = "list";
  var nodeMain = document.getElementById(MainNodeId).childNodes[1].childNodes[1];
  var tr_node  = document.createElement("tr");
  tr_node.id = "tr_"+id;
  var td_node  = document.createElement("td");
  td_node.id = "td_id";
  td_node.innerHTML=id;
  tr_node.appendChild(td_node);

  var td_node  = document.createElement("td");
  td_node.id = "td_partnum";
  td_node.innerHTML=data.partnum;
  td_node.onclick = function (e){
    text_Popup(this,100,80);
  }
  tr_node.appendChild(td_node);

  var td_node  = document.createElement("td");
  td_node.id = "td_amount";
  td_node.innerHTML=data.amount;
  td_node.onclick = function (e){
    incDec_Popup(this,80,100);
  }
  tr_node.appendChild(td_node);

  var td_node  = document.createElement("td");
  td_node.id = "td_place";
  td_node.innerHTML=data.place;
  td_node.onclick = function (e){
    incDec_Popup(this,80,100);
  }
  tr_node.appendChild(td_node);

  var td_node  = document.createElement("td");
  td_node.id = "td_type";
  td_node.innerHTML=data.type;
  td_node.onclick = function (e){
    getdata_2('getSelection.cgi',select_Popup,this,'type',100,80);
  }
  tr_node.appendChild(td_node);

  var td_node  = document.createElement("td");
  td_node.id = "td_value";
  td_node.innerHTML=data.value;
  td_node.onclick = function (e){
    getdata_2('getSelection.cgi',select_Popup,this,'value',100,80);
  }
  tr_node.appendChild(td_node);

  var td_node  = document.createElement("td");
  td_node.id = "td_package";
  td_node.innerHTML=data.package;
  td_node.onclick = function (e){
    select_Popup(this,'package',100,80);
  }
  tr_node.appendChild(td_node);

  var td_node  = document.createElement("td");
  td_node.id = "td_price";
  td_node.innerHTML=data.price;
  td_node.onclick = function (e){
    indec_money_Popup(this,'type',100,80);
  }
  tr_node.appendChild(td_node);

  var td_node  = document.createElement("td");
  td_node.onclick = function (e){
    changeAll_Popup(this.parentNode);
  }
  var img_node = document.createElement("img");
  img_node.width = 20;
  img_node.src   = "sett.svg";
  td_node.appendChild(img_node);
  tr_node.appendChild(td_node);

  nodeMain.appendChild(tr_node);
}

//------------------------------------------------------------------//
//------------------------    Basic Popup    -----------------------//
//------------------------------------------------------------------//

function clearPopup(id){
  // delete recursively
  if (!id) id = "popupFrame";
  var popup_main = document.getElementById(id);
  if (popup_main.childNodes.length > 0){
    popup_main.removeChild(popup_main.childNodes[0]);
    clearPopup(id);
  }
}

function ClsBtn_Popup(){
  try {
    document.getElementById("switchBtn_Slider").style.transitionDuration = ".0s";
    document.getElementsByClassName("slider-text")[0].style.transitionDuration = ".0s";
  } catch (e){}
  document.getElementById("Popup").style.visibility = "hidden";
  getdata('getdb.cgi',refreshMainList);
}

function SetMainPopup(width,height,name) {
  var field   = document.getElementById("Popup");
  var clientW = document.body.clientWidth;
  var clientH = document.body.clientHeight;
  field.style.width  = width;
//  var corrHeight = parseInt(height) + 35;
  field.style.height = parseInt(height)+35;
  field.style.left   = ((clientW - parseInt(field.style.width.slice(0,-2)))/2) +"px";
  field.style.top    = ((parseInt(clientH) - parseInt(field.style.height.slice(0,-2)))/3) +"px";
  var topMenuHeight  = parseInt(document.getElementsByClassName("top-menu-ul")[0].style.marginTop) + parseInt(document.getElementsByClassName("top-menu-ul")[0].offsetHeight);

  if ( parseInt(field.style.top.slice(0,-2)) < topMenuHeight ){
    field.style.top = "50px";
  } 

  var name_field = document.getElementById("popup_name_field");
  var name_size = name.length;
//  var popupName = document.getElementById("popup_name_field").offsetWidth;
  var popupClose= document.getElementsByClassName("close_Btn")[0].offsetLeft;
//  alert(name_size*13 +"<"+ popupClose);
  if (name_size*13 < popupClose) {
    name_field.innerHTML=name;
  } else {
    name_field.innerHTML=name.slice(0,popupClose/13-2)+"...";
  }
 
  field.style.visibility = "visible";
}

//---------------------------------------------------------------------//
//-----------------       changeAll_Popup     -------------------------//
//---------------------------------------------------------------------//

function changeAll_Popup(dom) {
  clearPopup();
  SetMainPopup("600","130","Update");

  var id= dom.id.slice(3);
  var main_tbl_head = document.getElementById("main_tbl_head");
  var popupFrame = document.getElementById("popupFrame");
  var table_node =  document.createElement("table");
  table_node.id="popup_tbl";
  table_node.width="96%";
  var tr_node =  document.createElement("tr");

  for (var i=1; i<(main_tbl_head.childNodes.length - 1);i++){
    var th_node = document.createElement("th");
    th_node.innerHTML = main_tbl_head.childNodes[i].innerHTML;
    tr_node.appendChild(th_node);
  }
  table_node.appendChild(tr_node);

  tr_node = document.createElement("tr");
  for (var i=1; i<(dom.childNodes.length);i++){ 
    var td_node = document.createElement("td");

    //insert input fields in rows. Not in case of id.
    if (main_tbl_head.childNodes[i].innerHTML == "partnum" || main_tbl_head.childNodes[i].innerHTML == "amount" || main_tbl_head.childNodes[i].innerHTML == "place"
        ||main_tbl_head.childNodes[i].innerHTML == "price") {
      var input = document.createElement("input");
      if (main_tbl_head.childNodes[i].innerHTML == "amount" || main_tbl_head.childNodes[i].innerHTML == "place") {
        input.type="number";
      } else {
	input.type="text";
      }
      input.style.width="100%";
      input.value= dom.childNodes[i-1].innerHTML;      
      
      td_node.appendChild(input);
//      if (main_tbl_head.childNodes[i].innerHTML == "partnum") {alert("partnum");}

    } else {
      td_node.innerHTML = dom.childNodes[i-1].innerHTML;
    } 
    td_node.id=main_tbl_head.childNodes[i].innerHTML;  
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
//                document.getElementById("Popup").style.visibility = "hidden";
ClsBtn_Popup();
            };
  popupFrame.appendChild(btn_node);  
}


function send_btn_UpdateAll_Popup(dom) {
  var str ="";
  var tr = dom.childNodes[0].childNodes[1];
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
  SetMainPopup(newWidth,newHeight+30,dom.id.slice(3));
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

  //  <div id="slideBtn" class="slideBtn"><span>ON</span></div>
//<input type="checkbox" checked>
  
  var inp_node_slideBtn =  document.createElement("input");
  inp_node_slideBtn.type="checkbox";
  inp_node_slideBtn.id="inp_SwitchBtn";
  inp_node_slideBtn.checked="TRUE";
  inp_node_slideBtn.onclick= function (e) {
                  AddDel_Fctn(this);
            };
  var div_node_slideBtn =  document.createElement("label");
  div_node_slideBtn.id = "switchBtn";
  div_node_slideBtn.className = "switchBtn";
  var span_node_slideBtn =  document.createElement("span");
  span_node_slideBtn.className="slider round";
  span_node_slideBtn.id="switchBtn_Slider";

  var spanInner = document.createElement("span");
  spanInner.className="slider-text";

  div_node_slideBtn.appendChild(inp_node_slideBtn);
  div_node_slideBtn.appendChild(span_node_slideBtn);
  div_node_slideBtn.appendChild(spanInner);
  popupFrame.appendChild(div_node_slideBtn);
  //--------------------------//

  var div_node_Frame =  document.createElement("div");
  div_node_Frame.className="cardNav";

  var div_node_outer =  document.createElement("div");
  div_node_outer.className="cardNav_Top_outer";

  var div_node_main =  document.createElement("div");
  div_node_main.className="cardNav_main";
  div_node_main.id="cardNav_main";
  div_node_main.innerHTML="";
  div_node_main.style.backgroundColor="#aaa";

  var div_node_Top_PlaceHolder =  document.createElement("div");
  div_node_Top_PlaceHolder.className="cardNav_Top_placeHolder";
  div_node_outer.appendChild(div_node_Top_PlaceHolder);

  //-------- Top Row  -----------//
  var div_node_Top =  document.createElement("div");
  div_node_Top.className="cardNav_Top_active";
  div_node_Top.onclick= function (e) {
                cardNavSelect(this);
            };
  div_node_Top.style.backgroundColor="#aaa";
  div_node_Top.innerHTML="Add Entry";
  div_node_Top.id="cardNav_Top_inner_Entry";
  div_node_outer.appendChild(div_node_Top);

  div_node_Top =  document.createElement("div");
  div_node_Top.className="cardNav_Top_inner";
  div_node_Top.onclick= function (e) {
                cardNavSelect(this);
            };
  div_node_Top.style.backgroundColor="#ddd";
  div_node_Top.innerHTML="Add Type";
  div_node_Top.id="cardNav_Top_inner_Type";
  div_node_outer.appendChild(div_node_Top);

  div_node_Top =  document.createElement("div");
  div_node_Top.className="cardNav_Top_inner";
  div_node_Top.onclick= function (e) {
                cardNavSelect(this);
            };
  div_node_Top.style.backgroundColor="#999";
  div_node_Top.innerHTML="Add Value";
  div_node_Top.id="cardNav_Top_inner_Value";
  div_node_outer.appendChild(div_node_Top);
  //--------END Top Row  -----------//

  div_node_Frame.appendChild(div_node_outer);
  div_node_Frame.appendChild(div_node_main);
  popupFrame.appendChild(div_node_Frame);


 /* <div class="cardNav">
      <div class="cardNav_Top_outer">
      <div class="cardNav_Top_placeHolder"></div>
      <div class="cardNav_Top_inner"  id="cardNav_Top_inner_Entry" style="background-color: #aaa;" onclick="cardNavSelect(this)">Add Entry</div>
      <div class="cardNav_Top_active" id="cardNav_Top_inner_Type"  style="background-color: #ddd;" onclick="cardNavSelect(this)">Add Type</div>
      <div class="cardNav_Top_inner"  id="cardNav_Top_inner_Value" style="background-color: #777;" onclick="cardNavSelect(this)">Add Value</div>
    </div>
    <div id="cardNav_main" class="cardNav_main">
      najklsefkleasjklesjfkl
    </div>
  </div>
*/
  var activeCard = document.getElementsByClassName("cardNav_Top_active")[0];
  CreateMainCard(activeCard);
  SetMainPopup(width,height,"Settings");
}

function cardNavSelect(dom){
  var color = dom.style.backgroundColor;
  var oldWin = document.getElementsByClassName("cardNav_Top_active")[0];
  oldWin.className="cardNav_Top_inner";
  dom.className="cardNav_Top_active";
  var newdom =  document.getElementsByClassName("cardNav_main")[0];
  newdom.style.backgroundColor = color;

  CreateMainCard(dom);
}

function AddDel_Fctn(dom){
  var status = dom.checked;
  if (status == true){
    status = "Add";
  } else {
    status = "Delete";
  }
  var topInner = document.getElementsByClassName("cardNav_Top_inner");
  var topInnerLength = topInner.length;
  for (var i=0;i<topInnerLength;i++) {
    //change name of card accord. to slideBtn;
    if ( topInner[i].innerHTML.slice(0,3) == "Add")
    { //normal Window; not special;
      topInner[i].innerHTML= status+topInner[i].innerHTML.slice(3);
    } else if ( topInner[i].innerHTML.slice(0,6) == "Delete") {
      topInner[i].innerHTML= status+topInner[i].innerHTML.slice(6);
    }
  }

  var topInnerActiv = document.getElementsByClassName("cardNav_Top_active")[0];
  var name="";
  if ( topInnerActiv.innerHTML.slice(0,3) === "Add")
  { //normal Window; not special;
    topInnerActiv.innerHTML= status+topInnerActiv.innerHTML.slice(3);
  } else if ( topInnerActiv.innerHTML.slice(0,6) === "Delete") {
    topInnerActiv.innerHTML= status+topInnerActiv.innerHTML.slice(6);
  }
  
  CreateMainCard(topInnerActiv);
}

function CreateMainCard(activeCard){
  var status = document.getElementById("inp_SwitchBtn").checked;
  if (status == true){
    status = "Add";
  } else {
    status = "Del";
  }
  var dom = document.getElementById("cardNav_main");
//  dom.innerHTML = activeCard.innerHTML;

  if (activeCard.id.slice(18) === "Value"){
    getdata_2('getSelection.cgi',values_MainFrame_add,this,'type',status,100,80);
  }
  if (activeCard.id.slice(18) === "Type"){
    type_MainFrame_add(status);
  }
  if (activeCard.id.slice(18) === "Entry"){
    if (status === "Add") {
      getdata('getTypeValPack.cgi',entry_MainFrame_add);
    } else {
      getdata('getdb.cgi',entry_MainFrame_del);
    }
  }
}

//------------------------------------------------------//

function values_MainFrame_add(d,dom,type,status,w,h){
  clearPopup("cardNav_main");
  // Call getScript to get all kinds of values for a type.
  // returns all kinds which will be put here...
  var type_div_node = document.createElement("div");
  var type_txt_node = document.createElement("p");
  type_txt_node.innerHTML = "choose Type: ";
  type_txt_node.style.width="200px";
  var sel = document.createElement("SELECT");
  sel.style.width ="250px";
  sel.style.height="30px";
  var data;
  try { 
    data = JSON.parse(d);
    var datasize = data.length;
    for (var i in data){
      var opt = document.createElement("OPTION");
      opt.value= i;
      opt.innerHTML= i;
      sel.appendChild(opt);
    }
  }
  catch (e){
  }  

  sel.style.textAlign="center";
  type_div_node.appendChild(type_txt_node);  
  type_div_node.appendChild(sel);  
  document.getElementById("cardNav_main").appendChild(type_div_node);

  var val_txt_node = document.createElement("p");
  val_txt_node.innerHTML = "";
  if (status === "Add") {
    val_txt_node.innerHTML = "new Type: ";
  } else {
    val_txt_node.innerHTML = "delete Type:"
  }

  var val_div_node = document.createElement("div"); 
  var inp_node     = document.createElement("input");

  //inp_node.style.width="100%";
  inp_node.style.width ="250px";
  inp_node.style.height="30px";

  inp_node.type="text";
  val_div_node.appendChild(val_txt_node);
  val_div_node.appendChild(inp_node);

  document.getElementById("cardNav_main").appendChild(val_div_node);

  var btn_node= document.createElement("input");
  btn_node.type = "button";
  btn_node.value= "";
  if (status === "Add") {
    btn_node.value = "insert";
  } else {
    btn_node.value = "delete";
  }
  btn_node.className ="SendBtn";
  if (status === "Add") {
    btn_node.onclick = function (e) {
              getdata_2('add_val.cgi?'+sel.value+'-'+inp_node.value,null,null,null,null,null);
            };
  } else {   
     btn_node.onclick = function (e) {
    //          getdata_2('add_val.cgi?'+sel.value+'-'+inp_node.value,null,null,null,null,null);
    alert("delete");
            };   
  }
  btn_node.style.marginTop="0px";
  document.getElementById("cardNav_main").appendChild(btn_node);  
}

//------------------------------------------------------//

function type_MainFrame_add(status){
  clearPopup("cardNav_main");
  // Call getScript to get all kinds of values for a type.
  // returns all kinds which will be put here...
  var type_div_node = document.createElement("div");
  var type_txt_node = document.createElement("p");

  var val_txt_node = document.createElement("p");
  val_txt_node.innerHTML = "";
  if (status === "Add") {
    val_txt_node.innerHTML = "new Type: ";
  } else {
    val_txt_node.innerHTML = "delete Type:"
  }
  var val_div_node = document.createElement("div"); 
  var inp_node     = document.createElement("input");

  //inp_node.style.width="100%";
  inp_node.style.width ="250px";
  inp_node.style.height="30px";

  inp_node.type="text";
  val_div_node.appendChild(val_txt_node);
  val_div_node.appendChild(inp_node);

  document.getElementById("cardNav_main").appendChild(val_div_node);

  var btn_node= document.createElement("input");
  btn_node.type = "button";
  btn_node.value= "";
  if (status === "Add") {
    btn_node.value = "insert";
  } else {
    btn_node.value = "delete";
  }


  btn_node.className ="SendBtn";
  if (status === "Add") {
    btn_node.onclick = function (e) {
//       getdata_2('del_val.cgi?'+inp_node.value,null,null,null,null,null);
         getdata_2('add_val.cgi?'+inp_node.value,null,null,null,null,null);
       alert("add");
    };
  } else {
    btn_node.onclick = function (e) {
//       getdata_2('del_val.cgi?'+inp_node.value,null,null,null,null,null);
        alert("delete");
    };

  }
  btn_node.style.marginTop="0px";
  document.getElementById("cardNav_main").appendChild(btn_node);  
}

//-----------------------------------------------------------

function entry_MainFrame_add(d,dom,w,h){
  clearPopup("cardNav_main");
  try {
    data_typeValPack = JSON.parse(d);
    var type = [];
    for (i in data_typeValPack.Type) {
      type.push(data_typeValPack.Type[i]);
    }

    for (i in data_typeValPack.TypeValue) {
     valueAddEntry.push(data_typeValPack.TypeValue[i]);
    }

//    alert(data_typeValPack["TypeValue"]["R"]);
//    alert(data_typeValPack["Package"]);
  } catch(e){
  }

  var main_tbl_head = document.getElementById("main_tbl_head");
  var table_node =  document.createElement("table");
  table_node.id="entry_Settings_tbl";
  table_node.width="96%";
  var tr_node =  document.createElement("tr");

  for (var i=1; i<(main_tbl_head.childNodes.length - 1);i++){
    var th_node = document.createElement("th");
    th_node.innerHTML = main_tbl_head.childNodes[i].innerHTML;
    tr_node.appendChild(th_node);
  }
  table_node.appendChild(tr_node);

  tr_node =  document.createElement("tr");
  var start_type="";
  for (var i=1; i<(main_tbl_head.childNodes.length - 1);i++){ 
    var td_node = document.createElement("td");

    //insert input fields in rows. Not in case of id.
    if (main_tbl_head.childNodes[i].innerHTML == "partnum" || main_tbl_head.childNodes[i].innerHTML == "amount" || main_tbl_head.childNodes[i].innerHTML == "place"
        ||main_tbl_head.childNodes[i].innerHTML == "price") {
      var input = document.createElement("input");
      if (main_tbl_head.childNodes[i].innerHTML == "amount" || main_tbl_head.childNodes[i].innerHTML == "place") {
        input.type="number";
      } else {
	input.type="text";
      }
      td_node.id = "CardNav_AddEntry_" + main_tbl_head.childNodes[i].innerHTML;      
      input.style.width="100%";
      //input.value= dom.childNodes[i].innerHTML;      
      td_node.appendChild(input);
    } else if (main_tbl_head.childNodes[i].innerHTML === "type") {
      var sel_node = document.createElement("select");
      td_node.id = "CardNav_AddEntry_type";
      var typeLength = type.length;
      sel_node.style.width = "50px";
      sel_node.onchange = function (e) {changeSelect();};
      for (var j=0;j<typeLength;j++){      
        var opt_node = document.createElement("option");
        opt_node.value = type[j];
        opt_node.innerHTML = type[j];
        sel_node.appendChild(opt_node);
      }
      td_node.id="CardNav_AddEntry_type";
      start_type = sel_node.value;
      td_node.appendChild(sel_node);
    } else if (main_tbl_head.childNodes[i].innerHTML === "value") {
      td_node.id = "CardNav_AddEntry_value";
      var sel_node = document.createElement("select");
      sel_node.style.width = "70px";
      var valueAddEntry_loc = data_typeValPack["TypeValue"][start_type].split(",");
      var valLength = valueAddEntry_loc.length;

      for (var j=0;j<valLength;j++){      
        var opt_node = document.createElement("option");
        opt_node.value =valueAddEntry_loc[j];
        opt_node.innerHTML = valueAddEntry_loc[j];
        sel_node.appendChild(opt_node);
      }
      td_node.appendChild(sel_node);
    } else if (main_tbl_head.childNodes[i].innerHTML === "package") {
      td_node.id = "CardNav_AddEntry_package";
      var sel_node = document.createElement("select");
      sel_node.style.width = "70px";
//      alert(valLength);
      for (var j in data_typeValPack.Package ){      
        var opt_node = document.createElement("option");
        opt_node.value = data_typeValPack["Package"][j];
        opt_node.innerHTML = data_typeValPack["Package"][j];
        sel_node.appendChild(opt_node);
      }
      td_node.appendChild(sel_node);

    } else {
     // td_node.innerHTML = dom.childNodes[i].innerHTML;
    }   
    tr_node.appendChild(td_node);
  }

  table_node.appendChild(tr_node);  
  document.getElementById("cardNav_main").appendChild(table_node);  

  document.getElementById("entry_Settings_tbl").style.position="relative";
  document.getElementById("entry_Settings_tbl").style.top="10px";
//  document.getElementById("entry_Settings_tbl").style.left = ((document.getElementById("popupFrame").clientWidth - document.getElementById("entry_Settings_tbl").clientWidth)/2)+"px";

  //Button for Sending changes
  var btn_node= document.createElement("input");
  btn_node.type = "button";
  btn_node.value="insert";
  btn_node.className="SendBtn";
  //btn_node.style.marginRight=  document.getElementById("entry_Settings_tbl").style.left;
  btn_node.onclick= function (e) {
                //send_btn_UpdateAll_Popup(this.parentNode);
                document.getElementById("Popup").style.visibility = "hidden";
                var part   = document.getElementById("CardNav_AddEntry_partnum").firstChild.value;
                var amount = document.getElementById("CardNav_AddEntry_amount").firstChild.value;
                var place  = document.getElementById("CardNav_AddEntry_place").firstChild.value;
                var type   = document.getElementById("CardNav_AddEntry_type").firstChild.value;
                var value  = document.getElementById("CardNav_AddEntry_value").firstChild.value;
                var pack   = document.getElementById("CardNav_AddEntry_package").firstChild.value;
                var price  = document.getElementById("CardNav_AddEntry_price").firstChild.value;
                getdata('setdb.cgi?'+part+'-'+amount+'-'+place+'-'+type+'-'+value+'-'+pack+'-'+price+'-0-1');
            };
  document.getElementById("cardNav_main").appendChild(btn_node);  
}

function changeSelect(){
  var type = document.getElementById("CardNav_AddEntry_type").firstChild.value;
  var td_node = document.getElementById("CardNav_AddEntry_value");
  td_ChildNode_length = td_node.childNodes.length;
  if (td_ChildNode_length > 0 ){
    //delete ChildNodes
    td_node.removeChild(td_node.childNodes[0]);
  }
  td_node.id="CardNav_AddEntry_value";
  var sel_node = document.createElement("select");
  sel_node.style.width = "70px";
  var valueAddEntry_loc = data_typeValPack["TypeValue"][type].split(",");
  var valLength = valueAddEntry_loc.length;

  for (var j=0;j<valLength;j++){      
    var opt_node = document.createElement("option");
    opt_node.value =valueAddEntry_loc[j];
    opt_node.innerHTML = valueAddEntry_loc[j];
    sel_node.appendChild(opt_node);
  }
  td_node.appendChild(sel_node);
}

//----------------------------------------------------------//

function entry_MainFrame_del(d,page,NmbElmts){
  var LinesPerPage = 8;
  clearPopup("cardNav_main");
  if (!page) page = 0;
  var data;
  data = JSON.parse(d);
  var id=1;
  makeHeadline();
  var cnt = 0;
  if (!NmbElmts) {
    NmbElmts = 0;
    for(var i in data){
      if (i !== "title"){  
        NmbElmts++;
      }
    }
  }

  for (var i in data){
      if (i !== "title"){  
        //alert(data[i].partnum);
        if (cnt >= page) {
          makeEntry(data[i],i);
        }
        cnt++;
      }
      if (cnt === (page+LinesPerPage)) {break;}
  }

  var nodeMain = document.getElementById("cardNav_main");
  var NmbPages= Math.ceil(NmbElmts / LinesPerPage);
  var pageNmb_node = document.createElement("div");
  pageNmb_node.style.position="absolute";
  pageNmb_node.style.bottom="5px";
  pageNmb_node.style.left="40%";
  for (var i=0;i<(NmbPages);i++){
    var p_node = document.createElement("p");
    p_node.innerHTML = i+1;
    p_node.onclick = function(e) {
      entry_MainFrame_del(d,((this.innerHTML-1) * LinesPerPage),NmbElmts);
    };
    p_node.style.float="left";
    p_node.style.padding = "2px";
    p_node.style.cursor="pointer";
    pageNmb_node.appendChild(p_node);
  }
  nodeMain.appendChild(pageNmb_node);


  //--------------------------------------------------//
  function makeEntry(data,id){ 
    var nodeMain = document.getElementById("cardNav_Entry_tbl_del");
    var tr_node  = document.createElement("tr");
    tr_node.id = "tr_"+id+"cardNav";
    var td_node  = document.createElement("td");
    td_node.id = "td_id_cardNav";
    td_node.innerHTML=id;
    tr_node.appendChild(td_node);

    var td_node = document.createElement("td");
    td_node.id  = "td_"+id+"_partnum_cardNav";
    td_node.innerHTML=data.partnum;
    tr_node.appendChild(td_node);

    td_node    = document.createElement("td");
    td_node.id = "td_"+id+"_amount_cardNav";
    td_node.innerHTML=data.amount;
    tr_node.appendChild(td_node);

    td_node    = document.createElement("td");
    td_node.id = "td_"+id+"_place_cardNav";
    td_node.innerHTML=data.place;
    tr_node.appendChild(td_node);

    td_node    = document.createElement("td");
    td_node.id = "td_"+id+"_type_cardNav";
    td_node.innerHTML=data.type;
    tr_node.appendChild(td_node);

    td_node    = document.createElement("td");
    td_node.id = "td_"+id+"_value_cardNav";
    td_node.innerHTML=data.value;
    tr_node.appendChild(td_node);

    td_node    = document.createElement("td");
    td_node.id = "td_"+id+"_package_cardNav";
    td_node.innerHTML=data.package;
    tr_node.appendChild(td_node);

    td_node    = document.createElement("td");
    td_node.id = "td_"+id+"_price_cardNav";
    td_node.innerHTML=data.price;
    tr_node.appendChild(td_node);

    var td_node  = document.createElement("td");
    td_node.onclick = function (e){
      var id_val = this.parentNode.firstChild.innerHTML;
      getdata('removedb.cgi?'+id_val);
    }
    var img_node = document.createElement("img");
    img_node.width = 20;
    img_node.src   = "delete.svg";
    td_node.appendChild(img_node);
    tr_node.appendChild(td_node);

    nodeMain.appendChild(tr_node);
  }

  function makeHeadline(){ 
    var main     = document.getElementById("cardNav_main");
    var tbl_node = document.createElement("table");
    tbl_node.id  = "cardNav_Entry_tbl_del";
    var tr_node  = document.createElement("tr");
    tr_node.id   = "th_cardNav";

    var th_node = document.createElement("th");
    th_node.id = "td_id_cardNav";
    th_node.innerHTML="id";
    tr_node.appendChild(th_node);

    th_node = document.createElement("th");
    th_node.id = "td_partnum_cardNav";
    th_node.innerHTML="partnum";
    tr_node.appendChild(th_node);

    th_node = document.createElement("th");
    th_node.id = "td_amount_cardNav";
    th_node.innerHTML="amount";
    tr_node.appendChild(th_node);

    th_node = document.createElement("th");
    th_node.id = "td_place_cardNav";
    th_node.innerHTML="place";
    tr_node.appendChild(th_node);

    th_node = document.createElement("th");
    th_node.id = "td_type_cardNav";
    th_node.innerHTML="type";
    tr_node.appendChild(th_node);

    th_node = document.createElement("th");
    th_node.id = "td_value_cardNav";
    th_node.innerHTML="value";
    tr_node.appendChild(th_node);

    th_node = document.createElement("th");
    th_node.id = "td_package_cardNav";
    th_node.innerHTML="package";
    tr_node.appendChild(th_node);

    th_node = document.createElement("th");
    th_node.id = "td_price_cardNav";
    th_node.innerHTML="price";
    tr_node.appendChild(th_node);

    th_node = document.createElement("th");
    th_node.id = "td_del_cardNav";
    th_node.innerHTML="";
    tr_node.appendChild(th_node);

    tbl_node.appendChild(tr_node);
    main.appendChild(tbl_node);
  }
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
  SetMainPopup(width,height,dom.id.slice(3));
}

//--------------------------------------------------------------------------------------//
//---------------------         Select_Popup        --------------------------------------//
//--------------------------------------------------------------------------------------//

function select_Popup(d,dom,type,width,height){
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
  var res="";
  var data;
  try { 
    data = JSON.parse(d);
    var datasize = data.length;
    for (var i in data){
      var opt = document.createElement("OPTION");
      opt.value= i;
      opt.innerHTML= i;
      sel.appendChild(opt);
    }
  }
  catch (e){
  }  

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
  SetMainPopup(width,height,dom.id.slice(3));
}

//---------------------------------------------------------------------//
//---------------        Dragability of Popup      --------------------//
//---------------------------------------------------------------------//

function dragElement(elmnt) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (document.getElementById(elmnt.id + "header")) {
    // if present, the header is where you move the DIV from:
    document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
    document.getElementById(elmnt.id + "header").ontouchstart = dragtouchmove;
    document.getElementById(elmnt.id + "header").ontouchstop = closeDragElement;
  } else {
    // otherwise, move the DIV from anywhere inside the DIV:
 //   elmnt.onmousedown = dragMouseDown;
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function dragtouchmove(e) {
    document.getElementById(elmnt.id + "header").ontouchstart = null;
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.touches[0].clientX;
    pos4 = e.touches[0].clientY;
    // call a function whenever the cursor moves:
    document.ontouchmove = elementDragTouch;
    document.ontouchstop = closeDragElement;
  }
  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // set the element's new position:
    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
  }

  function elementDragTouch(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.touches[0].clientX;
    pos2 = pos4 - e.touches[0].clientY;
    pos3 = e.touches[0].clientX;
    pos4 = e.touches[0].clientY;
    // set the element's new position:
    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
  }

  function closeDragElement() {
    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;
    document.ontouchmove = null;
    document.getElementById(elmnt.id + "header").ontouchstart = dragtouchmove;
  }
}

//---------------------------------------------------------------------//
//---------------         Scaling of Popup         --------------------//
//---------------------------------------------------------------------//

function scaleElement(elmnt) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (document.getElementById(elmnt.id)) {
    // if present, the header is where you move the DIV from:
    document.getElementById(elmnt.id).onmousedown = scaleMouseDown;
  }

  function scaleMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeScaleElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementScale;
  }

  function elementScale(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // set the element's new position:
   
    if ( pos1 > 2 || pos2 > 2 || pos1 < -2 || pos2 < -2){
      if (elmnt.id.slice(-1) == "L"){
        elmnt.parentNode.style.left = (elmnt.parentNode.offsetLeft - pos1) + "px";
      }
      elmnt.parentNode.style.width = (elmnt.parentNode.offsetWidth - pos1) + "px";
      elmnt.parentNode.style.height = (elmnt.parentNode.offsetHeight - pos2) + "px";
    }
  }

  function closeScaleElement() {
    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;
  }

}

</script>
</html>

$;

