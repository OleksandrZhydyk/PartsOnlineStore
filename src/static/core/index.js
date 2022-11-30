const buttonPlus = document.querySelector("#button-plus");
function handlePlus(event) {
    event.preventDefault();
    alert("plus");
}
buttonPlus.addEventListener(onClick, handlePlus);