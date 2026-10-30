/**
 * NIVORA – Form Validation Utilities
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Password confirmation match check
  const regForm = document.getElementById('registrationForm');
  if (regForm) {
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');

    if (password && confirmPassword) {
      confirmPassword.addEventListener('input', function () {
        if (this.value && this.value !== password.value) {
          this.setCustomValidity("Passwords do not match.");
        } else {
          this.setCustomValidity("");
        }
      });
    }
  }

  // 2. Phone number formatting & validation
  const phoneInputs = document.querySelectorAll('input[type="tel"], input[name*="phone"]');
  phoneInputs.forEach(input => {
    input.addEventListener('input', function () {
      // Allow only numbers, spaces, plus and dashes
      this.value = this.value.replace(/[^0-9+\-\s]/g, '');
    });
  });
});

