function deletePost(slug){
    var con = confirm("Are you sure you want to delete "+slug)
    if (con){
        $(`#${slug}`).remove();
        var xhr =   new XMLHttpRequest();
        xhr.open("POST","/delete/" + slug ,true);
        xhr.send();
        
}
}
function post(slug){
    var tittle = document.getElementById("tittle").value
    var tagline = document.getElementById("tagline").value
    var content = document.getElementById("content").value
    
    var xhr = new XMLHttpRequest();
    xhr.open("POST","/update/" + slug,true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    var s = xhr.send(JSON.stringify({
    "tittle":tittle,
    "tagline":tagline,
    "content":content
    }));
    if (s){
        document.getElementById("name").innerHTML = ` <h2> ${tittle} </h2>`
    }


}

function newpost(){
    var tittle = document.getElementById("tittle").value;
    var tagline = document.getElementById("tagline").value;
    var slug = document.getElementById("slug").value;
    var content = document.getElementById("content").innerHTML;
    
    var xhr = XMLHttpRequest()
    xhr.open('POST','/edit/new-post',true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    var r = xhr.send(JSON.stringify(
    {
        'tittle': tittle,
        'slug' : slug,
        'tagline': tagline,
        'content' : content 
    }    
    ))
    if (r){
        
    window.location.replace('/cp');
    }





}