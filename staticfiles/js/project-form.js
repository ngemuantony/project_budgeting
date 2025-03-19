// Function to add a new budget category
function addBudgetCategory() {
    const container = document.getElementById('budget-categories');
    const totalFormsInput = document.getElementById('id_form-TOTAL_FORMS');
    
    if (!container || !totalFormsInput) {
        console.error('Required elements not found');
        return;
    }
    
    const formNum = parseInt(totalFormsInput.value);
    
    // Create category options HTML
    const categoryOptions = window.CATEGORIES_DATA.map(category => 
        `<option value="${category.id}">${category.name}</option>`
    ).join('');
    
    const newForm = `
        <div class="budget-category rounded-lg border border-gray-200 bg-gray-50 p-4 dark:border-gray-700 dark:bg-gray-900">
            <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
                <div>
                    <label for="id_form-${formNum}-category" class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">Category</label>
                    <select name="form-${formNum}-category" id="id_form-${formNum}-category" class="w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500" required>
                        <option value="">Select a category</option>
                        ${categoryOptions}
                    </select>
                </div>
                <div>
                    <label for="id_form-${formNum}-amount" class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">Budget Amount</label>
                    <input type="number" name="form-${formNum}-amount" id="id_form-${formNum}-amount" class="w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500" step="0.01" min="0" required>
                </div>
            </div>
            <input type="hidden" name="form-${formNum}-id" id="id_form-${formNum}-id">
            <input type="hidden" name="form-${formNum}-DELETE" id="id_form-${formNum}-DELETE">
            <div class="mt-4 flex justify-end">
                <button type="button" class="inline-flex items-center gap-x-2 rounded-lg border border-red-600 px-4 py-2 text-sm font-semibold text-red-600 hover:bg-red-50 dark:border-red-500 dark:text-red-500 dark:hover:bg-red-950" onclick="deleteForm(this)">
                    <svg class="size-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    Remove
                </button>
            </div>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', newForm);
    totalFormsInput.value = formNum + 1;
}

// Function to delete a budget category form
function deleteForm(button) {
    const formDiv = button.closest('.budget-category');
    if (formDiv) {
        formDiv.style.display = 'none';
        const deleteInput = formDiv.querySelector('input[name$="-DELETE"]');
        if (deleteInput) {
            deleteInput.value = 'on';
        }
    }
}

// Initialize form count when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Initialize form count
    const formCount = document.querySelectorAll('.budget-category').length;
    const totalFormsInput = document.getElementById('id_form-TOTAL_FORMS');
    if (totalFormsInput) {
        totalFormsInput.value = formCount;
    }
});
