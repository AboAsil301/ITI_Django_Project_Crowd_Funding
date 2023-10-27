document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("register-form");

    function checkPasswordMatch(input) {
        const passwordField = document.getElementById("pass");
        if (input.value !== passwordField.value) {
            input.setCustomValidity("Passwords do not match");
        } else {
            input.setCustomValidity("");
        }
    }

    form.addEventListener("submit", function (event) {
        // Manually trigger HTML5 form validation
        if (!form.checkValidity()) {
            event.preventDefault();
            return;
        }

        const passwordField = document.getElementById("pass");
        const rePasswordField = document.getElementById("re_pass");
        const mobilePhoneField = document.getElementById("mobile_phone");
        const profilePictureField = document.getElementById("Profile_Picture");
        let valid = true;

        // Password validation
        if (passwordField.value !== rePasswordField.value) {
            valid = false;
            passwordField.setCustomValidity("Passwords do not match");
        } else {
            passwordField.setCustomValidity("");
        }

        // Mobile phone validation
        const mobilePhoneValue = mobilePhoneField.value;
        const mobilePhonePattern = /^(011|010|012|015)\d{8}$/; // Egyptian mobile number pattern

        if (!mobilePhonePattern.test(mobilePhoneValue)) {
            valid = false;
            mobilePhoneField.setCustomValidity("Invalid mobile phone number. Please enter a valid Egyptian mobile number.");
        } else {
            mobilePhoneField.setCustomValidity("");
        }

        // Profile picture validation
        if (profilePictureField.files.length > 0) {
            const allowedImageTypes = ["image/jpeg", "image/png", "image/gif"];
            const selectedFileType = profilePictureField.files[0].type;

            if (!allowedImageTypes.includes(selectedFileType)) {
                valid = false;
                profilePictureField.setCustomValidity("Invalid file type. Please select an image (JPEG, PNG, GIF).");
            } else {
                profilePictureField.setCustomValidity("");
            }
        }

        if (!valid) {
            event.preventDefault();
        }
    });

    // Reset custom validation messages when the input fields are modified
    const inputFields = form.querySelectorAll("input");
    inputFields.forEach(function (field) {
        field.addEventListener("input", function () {
            field.setCustomValidity(""); // Clear custom validation messages
        });
    });
});
