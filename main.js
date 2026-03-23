function allCapsLetter(str){
    let result = "";
    for(let i = 0; i < str.length; i++){
        if((str[i] >= "A" && str[i] <= "Z") || (str[i] >= "a" && str[i] <= "z")){
            result += str[i].toUpperCase();
        }
    }
    return result;
}

document.addEventListener("DOMContentLoaded", () => {
    const h1Element = document.querySelector("h1");
    const pElements = document.querySelectorAll("p");
    if (h1Element) {
        h1Element.textContent = allCapsLetter(h1Element.textContent);
    }
    if (pElements) {
        pElements.forEach(pElement => {
            pElement.textContent = allCapsLetter(pElement.textContent);
        });
    }
});
