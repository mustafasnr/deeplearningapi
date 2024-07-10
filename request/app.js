const ranges= document.getElementsByClassName("probs")
const names= document.getElementsByClassName("probnames")
async function uploadImage() {
    var formData = new FormData();
    var fileInput = document.getElementById('imageInput');
    var file = fileInput.files[0];
    console.log(Object.prototype.toString.call(file).slice(8, -1));// File
    formData.append('file', file,file.name);
    
    response = await fetch('http://127.0.0.1:8000/models/vgg16', {
        method: 'post',
        body: formData
    }).catch(console.error)
    probs = await response.json();
    keys=Object.keys(probs)
    
    for (let i = 0; i < ranges.length; i++) {
        ranges[i].style.width=`${probs[keys[i]]*300}px`
        names[i].innerHTML=keys[i]
    }
}