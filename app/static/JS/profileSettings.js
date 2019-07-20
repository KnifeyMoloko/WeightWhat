// activate name input field
function activateNameField() {
    var btn = document.querySelector("#ww-profile-name-btn");
    var field = document.querySelector("#ww-profile-name");
    field.removeAttribute("class");
    field.removeAttribute("readonly");
    field.setAttribute("class", "form-control");
    field.setAttribute("type", "text");
    btn.setAttribute("onclick", "updateName()");
    btn.innerHTML = "Update";
    console.log(btn);
}

// update user name based on the input field
function updateName() {
    var field = document.querySelector("#ww-profile-name");
    field.setAttribute("disabled", "disabled");
    var submit = document.querySelector("#ww-profile-submit");
    //submit.click();
    console.log(submit);
}