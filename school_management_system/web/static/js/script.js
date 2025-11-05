// Main JavaScript file for School Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Handle sidebar toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            document.body.classList.toggle('sidebar-collapsed');
        });
    }

    // Handle form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Handle data tables
    const dataTables = document.querySelectorAll('.data-table');
    if (dataTables.length > 0 && typeof $.fn.DataTable !== 'undefined') {
        dataTables.forEach(table => {
            $(table).DataTable({
                responsive: true,
                language: {
                    search: "_INPUT_",
                    searchPlaceholder: "Search...",
                }
            });
        });
    }

    // Handle date pickers
    const datePickers = document.querySelectorAll('.date-picker');
    if (datePickers.length > 0 && typeof flatpickr !== 'undefined') {
        datePickers.forEach(picker => {
            flatpickr(picker, {
                dateFormat: "Y-m-d",
                allowInput: true
            });
        });
    }

    // Handle alerts auto-close
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        if (!alert.classList.contains('alert-persistent')) {
            setTimeout(() => {
                const closeButton = alert.querySelector('.btn-close');
                if (closeButton) {
                    closeButton.click();
                }
            }, 5000);
        }
    });

    // Handle dynamic form fields
    const addFieldButtons = document.querySelectorAll('.add-field-button');
    addFieldButtons.forEach(button => {
        button.addEventListener('click', function() {
            const container = document.querySelector(this.dataset.container);
            const template = document.querySelector(this.dataset.template);
            if (container && template) {
                const clone = template.content.cloneNode(true);
                const index = container.children.length;
                
                // Update IDs and names with new index
                const elements = clone.querySelectorAll('[id], [name]');
                elements.forEach(el => {
                    if (el.id) el.id = el.id.replace('__index__', index);
                    if (el.name) el.name = el.name.replace('__index__', index);
                });
                
                container.appendChild(clone);
            }
        });
    });

    // Handle dynamic removal of form fields
    document.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('remove-field-button')) {
            const fieldGroup = e.target.closest('.field-group');
            if (fieldGroup) {
                fieldGroup.remove();
            }
        }
    });
});

// Utility functions
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

function showNotification(message, type = 'info') {
    if (typeof toastr !== 'undefined') {
        toastr[type](message);
    } else {
        alert(message);
    }
}
