// Project form functionality
window.projectForm = {
    init() {
        this.updateFormCount();
        
        // Add any initialization code here
        const totalForms = document.querySelector('#id_category_set-TOTAL_FORMS');
        if (totalForms) {
            this.updateFormCount();
        }
    },

    updateFormCount() {
        const totalForms = document.querySelector('#id_category_set-TOTAL_FORMS');
        if (totalForms) {
            const forms = document.querySelectorAll('.budget-category-form');
            totalForms.value = forms.length;
        }
    },

    showAddCategoryModal() {
        const modal = document.getElementById('add-category-modal');
        if (modal) {
            modal.classList.remove('hidden');
        }
    },

    hideAddCategoryModal() {
        const modal = document.getElementById('add-category-modal');
        const nameInput = document.getElementById('new-category-name');
        const amountInput = document.getElementById('new-category-amount');
        
        if (modal) {
            modal.classList.add('hidden');
        }
        
        // Clear form inputs
        if (nameInput) nameInput.value = '';
        if (amountInput) amountInput.value = '';
    },

    addNewCategory() {
        const nameInput = document.getElementById('new-category-name');
        const amountInput = document.getElementById('new-category-amount');
        
        if (!nameInput || !amountInput) {
            console.error('Category form inputs not found');
            return;
        }

        const name = nameInput.value;
        const amount = amountInput.value;

        if (!name || !amount) {
            alert('Please fill in all fields');
            return;
        }

        const totalForms = document.querySelector('#id_category_set-TOTAL_FORMS');
        if (!totalForms) {
            console.error('Total forms input not found');
            return;
        }

        const formIdx = parseInt(totalForms.value);
        const template = `
            <div class="budget-category-form rounded-lg border border-gray-200 bg-gray-50 p-4 dark:border-gray-700 dark:bg-gray-700">
                <div class="grid gap-4 md:grid-cols-2">
                    <div>
                        <label for="id_category_set-${formIdx}-category_name" class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">Category Name</label>
                        <input type="text" name="category_set-${formIdx}-category_name" id="id_category_set-${formIdx}-category_name" value="${name}" class="w-full rounded-lg border border-gray-300 bg-white p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-800 dark:text-white dark:placeholder-gray-400" required>
                    </div>
                    <div>
                        <label for="id_category_set-${formIdx}-amount" class="mb-2 block text-sm font-medium text-gray-900 dark:text-white">Budget Amount</label>
                        <input type="number" name="category_set-${formIdx}-amount" id="id_category_set-${formIdx}-amount" value="${amount}" class="w-full rounded-lg border border-gray-300 bg-white p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-800 dark:text-white dark:placeholder-gray-400" required>
                    </div>
                </div>
                <div class="mt-4 flex justify-end">
                    <button type="button" onclick="window.projectForm.deleteForm(this)" class="inline-flex items-center gap-x-2 rounded-lg border border-red-600 px-4 py-2 text-sm font-semibold text-red-600 hover:bg-red-50 dark:border-red-500 dark:text-red-500 dark:hover:bg-red-950">
                        <svg class="size-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                        Remove Category
                    </button>
                </div>
            </div>
        `;

        const container = document.getElementById('budget-categories');
        if (container) {
            container.insertAdjacentHTML('beforeend', template);
            totalForms.value = parseInt(totalForms.value) + 1;
            this.hideAddCategoryModal();
        }
    },

    deleteForm(button) {
        const form = button.closest('.budget-category-form');
        if (form) {
            form.remove();
            this.updateFormCount();
        }
    }
};

// Initialize the form functionality when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.projectForm.init();
});
