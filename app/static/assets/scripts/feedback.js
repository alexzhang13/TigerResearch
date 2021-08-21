function openForm() {
    document.getElementById("feedback-form").style.display = "block";
    document.getElementById("feedback-btn").style.color = "white";
}

function closeForm() {
    document.getElementById("feedback-form").style.display = "none";
    document.getElementById("feedback-btn").style.color = "#ff5400";
}

function triggerForm() {
    if (document.getElementById("feedback-form").style.display === "block") {
        closeForm();
    } else {
        openForm();
    }
}