function confirmDeleteAccount() {
    if (confirm("Are you sure you want to delete your account? This action is irreversible.")) {
        // update the action value
        document.getElementById("settings-form-action").value = "delete_account";
        // submit the form
        document.getElementById("settings-form").submit();
    }

    return false;
}