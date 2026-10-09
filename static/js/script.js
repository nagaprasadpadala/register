// ============================
// Toggle Password Visibility
// ============================

function togglePassword(inputId) {

    const input = document.getElementById(inputId);

    if (input.type === "password") {

        input.type = "text";

    } else {

        input.type = "password";

    }
}


// ============================
// Signup Validation
// ============================

const signupForm = document.getElementById("signupForm");


if (signupForm) {

    signupForm.addEventListener("submit", function (event) {

        let valid = true;


        const name =
            document.getElementById("name").value.trim();

        const email =
            document.getElementById("email").value.trim();

        const password =
            document.getElementById("password").value;

        const confirmPassword =
            document.getElementById("confirmPassword").value;


        const nameError =
            document.getElementById("nameError");

        const emailError =
            document.getElementById("emailError");

        const passwordError =
            document.getElementById("passwordError");

        const confirmPasswordError =
            document.getElementById("confirmPasswordError");


        // Clear errors

        nameError.textContent = "";

        emailError.textContent = "";

        passwordError.textContent = "";

        confirmPasswordError.textContent = "";


        // Name validation

        if (name.length < 3) {

            nameError.textContent =
                "Name must contain at least 3 characters.";

            valid = false;
        }


        // Email validation

        const emailPattern =
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


        if (!emailPattern.test(email)) {

            emailError.textContent =
                "Enter a valid email address.";

            valid = false;
        }


        // Password validation

        if (password.length < 8) {

            passwordError.textContent =
                "Password must contain at least 8 characters.";

            valid = false;
        }


        // Confirm password

        if (password !== confirmPassword) {

            confirmPasswordError.textContent =
                "Passwords do not match.";

            valid = false;
        }


        // Stop form submission if invalid

        if (!valid) {

            event.preventDefault();

        }

    });

}


// ============================
// Signin Validation
// ============================

const signinForm =
    document.getElementById("signinForm");


if (signinForm) {

    signinForm.addEventListener("submit", function (event) {

        let valid = true;


        const email =
            document.getElementById("signinEmail").value.trim();

        const password =
            document.getElementById("signinPassword").value;


        const emailError =
            document.getElementById("signinEmailError");

        const passwordError =
            document.getElementById("signinPasswordError");


        emailError.textContent = "";

        passwordError.textContent = "";


        const emailPattern =
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


        if (!emailPattern.test(email)) {

            emailError.textContent =
                "Enter a valid email address.";

            valid = false;
        }


        if (password.length === 0) {

            passwordError.textContent =
                "Password is required.";

            valid = false;
        }


        if (!valid) {

            event.preventDefault();

        }

    });

}