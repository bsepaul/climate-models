function change_state(obj) {
    if (obj.checked) {
        //if checkbox is being checked, add a "checked" class
        obj.parentNode.classList.add("checked");
    }
    else {
        //else remove it
        obj.parentNode.classList.remove("checked");
    }
}