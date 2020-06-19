document.getElementById("button-id-next").onclick = function() {
    document.getElementById("form1").classList.add("d-none");
    document.getElementById("form2").classList.remove("d-none");
    scroll(0,0);
};

document.getElementById("button-id-back").onclick = function() {
    document.getElementById("form1").classList.remove("d-none");
    document.getElementById("form2").classList.add("d-none");
    scroll(0,0);
};

// CKEditor inserts it's content into textarea after the HTML form validation.
// So, on the moment, when validation is working, content field would be empty.
// But after that CKEditor will paste it's own data into the field
// and POST request would be correct.
// But at the moment of the Form validation, content field must be non-required.
document.getElementById("editor").required = false;