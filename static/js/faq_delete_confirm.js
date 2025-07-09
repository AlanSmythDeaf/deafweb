let formToDelete = null;
let deleteModal = null;

// Wait for DOM ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap modal once
    deleteModal = new bootstrap.Modal(document.getElementById('deleteConfirmModal'));

    // Listen for clicks on delete buttons
    document.querySelectorAll('.delete-faq-btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            formToDelete = document.getElementById(this.dataset.formId);
            deleteModal.show();
        });
    });

    // Handle confirm delete button
    document.getElementById('confirmDeleteBtn').addEventListener('click', function() {
        if (formToDelete) {
            formToDelete.submit();
            formToDelete = null;
            deleteModal.hide();
        }
    });
});
