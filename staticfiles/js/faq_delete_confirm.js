let formToDelete = null;

// Listen for clicks on delete buttons
document.addEventListener('DOMContentLoaded', function() {
  // For all delete buttons with the class .delete-faq-btn
  document.querySelectorAll('.delete-faq-btn').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      formToDelete = document.getElementById(this.dataset.formId);
      // Show the modal
      const modal = new bootstrap.Modal(document.getElementById('deleteConfirmModal'));
      modal.show();

      // Confirm button logic
      const confirmBtn = document.getElementById('confirmDeleteBtn');
      // Remove any previous event listeners to prevent multiple submits
      confirmBtn.replaceWith(confirmBtn.cloneNode(true));
      document.getElementById('confirmDeleteBtn').addEventListener('click', function() {
        if (formToDelete) {
          formToDelete.submit();
          formToDelete = null;
          modal.hide();
        }
      });
    });
  });
});
