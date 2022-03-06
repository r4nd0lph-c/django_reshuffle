// auth.html
// ----------
// show/hide eye-button for password.
function pass_visibility() {
    let pass_in = document.getElementById("id_password");
    let eye_icon = document.getElementById("eye_icon");

    if (pass_in.type === "password") {
        pass_in.type = "text";
        eye_icon.className = "bi bi-eye-slash";
    } else {
        pass_in.type = "password";
        eye_icon.className = "bi bi-eye";
    }
}


// creation.html
// ----------
// extra validation for input values from form;
// this need for showing overlay.
function validation() {
    // 0 <= extra_val <= max - min
    const extra_val = 7;

    let overlay = document.getElementById("overlay");

    let subject_form = document.getElementById("id_subject");
    let is_subject = subject_form.options[subject_form.selectedIndex].value.length;

    let amount_form = document.getElementById("id_amount");
    let value = Number(amount_form.value);
    let min = Number(amount_form.min);
    let max = Number(amount_form.max);

    if (is_subject && value >= min + extra_val && value <= max) {
        overlay.style.display = "block";
    }
}