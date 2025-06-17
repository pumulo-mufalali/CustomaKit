document.addEventListener('DOMContentLoaded', function() {
    // Update Customer Button
    document.getElementById('updateCustomerBtn').addEventListener('click', function() {
        window.location.href = "{% url 'customer_update' customer.id %}";
    });
    
    // Delete Customer Button
    document.getElementById('deleteCustomerBtn').addEventListener('click', function() {
        if (confirm('Are you sure you want to delete this customer? This action cannot be undone.')) {
            window.location.href = "{% url 'customer_delete' customer.id %}";
        }
    });
    
    // Search functionality
    document.getElementById('orderSearch').addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const rows = document.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
    
    // Order Update Buttons
    document.querySelectorAll('.update-order-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const orderId = this.getAttribute('data-order-id');
            window.location.href = `/orders/${orderId}/update/`;
        });
    });
    
    // Order Remove Buttons
    document.querySelectorAll('.remove-order-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const orderId = this.getAttribute('data-order-id');
            if (confirm('Are you sure you want to remove this order?')) {
                window.location.href = `/orders/${orderId}/delete/`;
            }
        });
    });
});