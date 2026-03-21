function allCapsLetter(str){
    let result = "";
    for(let i = 0; i < str.length; i++){
        if(str[i] >= "A" && str[i] <="Z"){
            result += str[i];
        }
    }
    return result;
}

document.addEventListener("DOMContentLoaded", () => {
    const h1Element = document.querySelector("h1");
    if (h1Element) {
        h1Element.textContent = allCapsLetter(h1Element.textContent);
    }
});