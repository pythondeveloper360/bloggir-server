function deletePost(slug){
    var con = confirm("Are you sure you want to delete "+slug)
    if (con){
        console.log("dsdfsd")
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
like = (slug) =>{
    var xhr = new XMLHttpRequest();
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.open("POST","like",true);
    xhr.send(JSON.stringify({
        slug:slug
    }));
    xhr.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.responseText == "done"){
                M.toast({html:"Added to likes"})
            }
            else if (this.responseText == "not done"){
                M.toast({html:"Sign in to like blog"})
            }
    }
  }
}







signup = ()=>{

}
