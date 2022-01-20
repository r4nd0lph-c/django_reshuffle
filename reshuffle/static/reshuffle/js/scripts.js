// auth.html
// ----------
// update border color dynamically

let pass_in = document.getElementById("id_password");
let eye_span = document.getElementById("eye_span");

pass_in.addEventListener("focusin", (event) => {
    eye_span.style.border = "1px solid #86b7fe";
});

pass_in.addEventListener("focusout", (event) => {
    eye_span.style.border = "1px solid #ced4da";
});