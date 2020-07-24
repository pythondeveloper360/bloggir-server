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