function openModal(htmlElement) {
    document.getElementById(htmlElement).style.display = "block";
    document.body.classList.add("modal-open");
}

function closeModal(htmlElement) {
    document.getElementById(htmlElement).style.display = "none";
    document.body.classList.remove("modal-open");
}