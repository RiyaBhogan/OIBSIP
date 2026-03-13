// ================= SECTION NAVIGATION =================

function showSection(section){

document.getElementById("generatorSection").style.display="none";
document.getElementById("breachSection").style.display="none";
document.getElementById("managerSection").style.display="none";

document.getElementById(section).style.display="block";

/* FIX: hide password manager content until login */

if(section==="managerSection"){

document.getElementById("passwordManagerSection").style.display="none";
document.getElementById("loginForm").style.display="none";
document.getElementById("registerForm").style.display="none";

document.getElementById("authButtons").style.display="block";
document.getElementById("loginPrompt").style.display="block";

}

}

// ================= PASSWORD HISTORY =================

let passwordHistory = [];


// ================= SWITCH GENERATOR =================

function showGenerator(type){

document.getElementById("customGenerator").style.display="none";
document.getElementById("passphraseGenerator").style.display="none";
document.getElementById("customWordGenerator").style.display="none";

if(type==="custom") document.getElementById("customGenerator").style.display="block";
if(type==="phrase") document.getElementById("passphraseGenerator").style.display="block";
if(type==="word") document.getElementById("customWordGenerator").style.display="block";

document.getElementById("result").innerText="";
document.getElementById("analysis").innerText="";
document.getElementById("entropy").innerText="";
document.getElementById("ml_strength").innerText="";
document.getElementById("ml_crack_time").innerText="";
document.getElementById("suggestion").innerText="";

let bar=document.getElementById("strength-bar");

if(bar){
bar.style.width="0%";
}

}


// ================= PROCESS PASSWORD =================

// ================= PROCESS PASSWORD =================

function processPassword(password){

document.getElementById("result").innerText=password;

/* removed auto-fill of password manager */

analyzePassword(password);
addToHistory(password);

let formData=new FormData();
formData.append("password",password);

fetch("/predict",{method:"POST",body:formData})
.then(res=>res.json())
.then(data=>{

document.getElementById("ml_strength").innerText=
"Predicted Strength: "+data.class_strength;

document.getElementById("ml_crack_time").innerText=
""+data.crack_time;

let bar=document.getElementById("strength-bar");

let s=data.class_strength.toLowerCase();

if(s.includes("very weak")){
bar.style.width="20%";
bar.style.background="red";
}
else if(s.includes("weak")){
bar.style.width="40%";
bar.style.background="orange";
}
else if(s.includes("medium")){
bar.style.width="60%";
bar.style.background="yellow";
}
else if(s.includes("strong")){
bar.style.width="80%";
bar.style.background="lightgreen";
}
else if(s.includes("very strong")){
bar.style.width="100%";
bar.style.background="green";
}

});

}

// ================= PASSWORD GENERATOR =================

function generatePassword(){

let upper=parseInt(document.getElementById("upperCount").value)||0;
let lower=parseInt(document.getElementById("lowerCount").value)||0;
let num=parseInt(document.getElementById("numberCount").value)||0;
let sym=parseInt(document.getElementById("symbolCount").value)||0;

let total=upper+lower+num+sym;

if(total===0){
alert("Enter at least one character");
return;
}

document.getElementById("totalLength").innerText=total;

let formData=new FormData();

formData.append("upperCount",upper);
formData.append("lowerCount",lower);
formData.append("numberCount",num);
formData.append("symbolCount",sym);

fetch("/generate",{method:"POST",body:formData})
.then(res=>res.json())
.then(data=>{

processPassword(data.password);

document.getElementById("upperCount").focus();

});

}


// ================= PASSPHRASE =================

function generatePassphrase(){

let words=["green","tiger","river","sky","forest","moon","ocean","cloud"];

let p=
words[Math.floor(Math.random()*words.length)]+"-"+
words[Math.floor(Math.random()*words.length)]+"-"+
words[Math.floor(Math.random()*words.length)]+"-"+
Math.floor(Math.random()*100);

document.getElementById("passphraseResult").innerText=p;

processPassword(p);

}


// ================= CUSTOM WORD PASSWORD =================

function generateCustomPassword(){

let input=document.getElementById("customWord");
let word=input.value.trim();

if(word===""){
alert("Enter a word");
input.focus();
return;
}

let symbol=["@","#","!","$","%"][Math.floor(Math.random()*5)];

let password=word+symbol+Math.floor(Math.random()*10000)+"Secure";

document.getElementById("customPasswordResult").innerText=password;

processPassword(password);

input.value="";
input.focus();

}


// ================= COPY PASSWORD =================

function copyPassword(){

let password=document.getElementById("result").innerText;

navigator.clipboard.writeText(password);

alert("Password copied");

}


// ================= PASSWORD ANALYSIS =================

function analyzePassword(password){

let upper=(password.match(/[A-Z]/g)||[]).length;
let lower=(password.match(/[a-z]/g)||[]).length;
let numbers=(password.match(/[0-9]/g)||[]).length;
let symbols=(password.match(/[^A-Za-z0-9]/g)||[]).length;

document.getElementById("analysis").innerText=
"Uppercase: "+upper+
" | Lowercase: "+lower+
" | Numbers: "+numbers+
" | Symbols: "+symbols;

let suggestions=[];

if(password.length<8) suggestions.push("Use at least 8 characters");
if(upper===0) suggestions.push("Add uppercase letters");
if(lower===0) suggestions.push("Add lowercase letters");
if(numbers===0) suggestions.push("Add numbers");
if(symbols===0) suggestions.push("Add symbols");

if(suggestions.length===0){

document.getElementById("suggestion").innerText=
"Password meets all security requirements";

}
else{

document.getElementById("suggestion").innerText=
"Suggestions: "+suggestions.join(" | ");

}

let pool=0;

if(upper) pool+=26;
if(lower) pool+=26;
if(numbers) pool+=10;
if(symbols) pool+=32;

let entropy=Math.round(password.length*Math.log2(pool));

document.getElementById("entropy").innerText=
""+entropy+" bits";

}


// ================= PASSWORD HISTORY =================

function addToHistory(password){

passwordHistory.unshift(password);

if(passwordHistory.length>5) passwordHistory.pop();

let list=document.getElementById("historyList");

if(!list) return;

list.innerHTML="";

passwordHistory.forEach(p=>{

let li=document.createElement("li");
li.innerText=p;
list.appendChild(li);

});

}


// ================= BREACH CHECK =================

function checkBreach(){

let password=document.getElementById("breachInput");

let formData=new FormData();
formData.append("password",password.value);

fetch("/check_breach",{method:"POST",body:formData})
.then(res=>res.json())
.then(data=>{

document.getElementById("breachResult").innerText=
data.breached ?
"⚠ Found in data breaches"
:
"Not found in breaches";

password.value="";
password.focus();

});

}


// ================= SAVE PASSWORD =================

function savePassword(){

let site=document.getElementById("siteName").value;
let user=document.getElementById("userName").value;
let pass=document.getElementById("sitePassword").value;

if(site==="" || user==="" || pass===""){
alert("Please fill all fields");
return;
}

let formData=new FormData();

formData.append("website",site);
formData.append("username",user);
formData.append("password",pass);

fetch("/save_password",{method:"POST",body:formData})
.then(res=>{

if(res.status===401){
alert("Please login first");
return null;
}

return res.json();

})
.then(data=>{

if(!data) return;

document.getElementById("siteName").value="";
document.getElementById("userName").value="";
document.getElementById("sitePassword").value="";

loadPasswords();

});

}


// ================= LOAD PASSWORDS =================

function loadPasswords(){

fetch("/get_passwords")
.then(res=>{

if(res.status===401){

document.getElementById("loginPrompt").style.display="block";
document.getElementById("passwordManagerSection").style.display="none";
document.getElementById("logoutBtn").style.display="none";

return null;

}

return res.json();

})
.then(data=>{

if(!data) return;

document.getElementById("loginPrompt").style.display="none";
document.getElementById("passwordManagerSection").style.display="block";

let table=document.getElementById("passwordTable");

table.innerHTML=
"<tr><th>Website</th><th>Username</th><th>Password</th><th>Action</th></tr>";

data.forEach((row,index)=>{

let tr=document.createElement("tr");

tr.innerHTML=
"<td>"+row.website+"</td>"+
"<td>"+row.username+"</td>"+
"<td id='pass_"+index+"'>****** "+
"<button onclick='togglePassword("+index+", \""+row.password+"\")'>Show</button></td>"+
"<td><button onclick=\"deletePassword('"+row.website+"','"+row.username+"')\">Delete</button></td>";

table.appendChild(tr);

});

});

}


// ================= DELETE PASSWORD =================

function deletePassword(website,username){

let formData=new FormData();

formData.append("website",website);
formData.append("username",username);

fetch("/delete_password",{method:"POST",body:formData})
.then(()=>loadPasswords());

}


// ================= PAGE LOAD =================

window.onload=function(){

showSection("generatorSection");

loadPasswords();

let input=document.getElementById("customWord");

if(input){
input.addEventListener("keypress",function(e){
if(e.key==="Enter") generateCustomPassword();
});
}

}


// ================= TOGGLE PASSWORD =================

function togglePassword(id,password){

let cell=document.getElementById("pass_"+id);

if(cell.innerText.includes("******")){

cell.innerHTML=
password+" <button onclick='togglePassword("+id+", \""+password+"\")'>Hide</button>";

}
else{

cell.innerHTML=
"****** <button onclick='togglePassword("+id+", \""+password+"\")'>Show</button>";

}

}


// ================= REGISTER =================

function registerUser(){

let username=document.getElementById("registerUser").value;
let password=document.getElementById("registerPass").value;

let formData=new FormData();

formData.append("username",username);
formData.append("password",password);

fetch("/register",{method:"POST",body:formData})
.then(res=>res.json())
.then(data=>{

alert(data.message);

document.getElementById("registerUser").value="";
document.getElementById("registerPass").value="";

showLogin();

});

}


// ================= LOGIN =================

function loginUser(){

let username=document.getElementById("loginUser").value;
let password=document.getElementById("loginPass").value;

let formData=new FormData();

formData.append("username",username);
formData.append("password",password);

fetch("/login",{method:"POST",body:formData})
.then(res=>res.json())
.then(data=>{

if(data.success){

alert("Login successful");

document.getElementById("loginForm").style.display="none";
document.getElementById("registerForm").style.display="none";
document.getElementById("authButtons").style.display="none";

document.getElementById("logoutBtn").style.display="inline-block";

document.getElementById("passwordManagerSection").style.display="block";

loadPasswords();

}
else{

alert("Invalid username or password");

}

});

}


// ================= SHOW LOGIN =================

function showLogin(){

document.getElementById("loginForm").style.display="block";
document.getElementById("registerForm").style.display="none";

}


// ================= SHOW REGISTER =================

function showRegister(){

document.getElementById("registerForm").style.display="block";
document.getElementById("loginForm").style.display="none";

}



// ================= LOGOUT =================

function logoutUser(){

fetch("/logout")
.then(()=>{

alert("Logged out successfully");

location.reload();

});

}