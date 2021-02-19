let liked = `{{url_for('static',filename = 'img/liked.png')}}`
let like = `{{url_for('static',filename = 'img/like.png')}}`
console.log(like,liked)


function deletePost(slug){
    var con = confirm("Are you sure you want to delete "+slug)
    if (con){
        var xhr =   new XMLHttpRequest();
        xhr.open("POST","/delete/" + slug ,true);
        xhr.send()
        $(`#${slug}`).remove();

}
}
function post(slug){
    var tittle = document.getElementById("tittle").value;
    var tagline = document.getElementById("tagline").value;
    var content = document.getElementById("content").value;

    var xhr = new XMLHttpRequest();
    xhr.open("POST","/update/" + slug,true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    var s = xhr.send(JSON.stringify({
    "tittle":tittle,
    "tagline":tagline,
    "content":content
    }));
}


function changePassword(){
    var current = document.getElementById("Cpassword").value;
    var passrword = document.getElementById("pass").value;
    var rpassrword = document.getElementById("rpass").value;
    if (passrword != rpassrword){
        M.toast({html:"Passwords are not same"})
    }
    else if (passrword.length<10){
        M.toast({html:"password should be longer than 10 character"})

    }
    else{
        M.toast({html:"Chaning Passoword"})
        var xhr = new XMLHttpRequest();
        xhr.open("POST","/changepassword",true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({
            "current" :current,
            "newpassword":passrword
        }))
        xhr.onreadystatechange = function() {
        if (this.readyState == 4) {
            if(this.responseText == "Done"){
                M.toast({html:"Passoword changed"})
            }
            else if(this.responseText == "Not done")  {
                M.toast({html:'Old password is incorrect'})
            }
        }
    };
    }
}





signup = ()=>{
    let data = {
        'name' : document.getElementById("name").value,
        'uname' : document.getElementById("uname").value,
        'email' : document.getElementById("email".value),
        'pass' : document.getElementById("pass").value,
        'about' : document.getElementById("about").value 
    }
    let xhr = new XMLHttpRequest();
    xhr.open("POST",'/signup',true)
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data))
    window.location = '/'

}
let signin = (redirect) =>{
    let co = confirm('You are not signed in do you want to sign in ?')
    if (co == true){
        window.location = redirect;
    }
    
}

let setting = ()=>{
    let data = {
        "name":document.getElementById("name").value,
        "about":document.getElementById("textarea1").value
    }
    let xhr = new XMLHttpRequest();
    xhr.open('POST','/setting',true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data));

}
let comment = (slug) => {
    let d = new Date();
    if (document.getElementById('comment').value){
    let data = {
        "comment" : document.getElementById('comment').value,
        "date": `${d.getDate()}:${d.getMonth()}:${d.getFullYear()}`
    }
    let xhr = new XMLHttpRequest()
    xhr.open('POST',"/comment",true)
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data))
    }
}