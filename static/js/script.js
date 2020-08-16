function deletePost(slug){
    var con = confirm("Are you sure you want to delete "+slug)
    if (con){
        $(`#${slug}`).remove();
        var xhr =   new XMLHttpRequest();
        xhr.open("POST","/delete/" + slug ,true);

        
}
}
function post(slug){
    var tittle = document.getElementById("tittle").value;
    var tagline = document.getElementById("tagline").value;
    var content = document.getElementById("content").innerHTML;
    
    var xhr = new XMLHttpRequest();
    xhr.open("POST","/update/" + slug,true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    var s = xhr.send(JSON.stringify({
    "tittle":tittle,
    "tagline":tagline,
    "content":content
    }));
    

}

function newpost(){
    var tittle = document.getElementById("tittle").value;
    var tagline = document.getElementById("tagline").value;
    var slug = document.getElementById("slug").value;
    var content = document.getElementById("content").innerHTML;
    
    var xhr = new XMLHttpRequest();
    xhr.open('POST','/new-post',true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    var r = xhr.send(JSON.stringify(
    {
        'tittle': tittle,
        'slug' : slug,
        'tagline': tagline,
        'content' : content 
    }    
    ))
}

function login(){
    var uname = document.getElementById('uname');
    var password = document.getElementById('pass');
    var xhr = new XMLHttpRequest();
    xhr.open('POST',"/login",true)
    xhr.setRequestHeader('Content-Type', 'application/json');
    var r = xhr.send(JSON.stringify(
    {
        'uname': uname,
        'password' : password 
    }    
    ))


    

}