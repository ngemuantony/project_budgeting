"""
Forms for the project budgeting application.

This module contains all the forms used in the application for creating and managing
projects, budgets, and expenses. It includes both model forms and formsets for
handling complex data entry scenarios.
"""

from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Project, Category, Budget, Expense
from datetime import datetime

INPUT_CLASSES = "w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
SELECT_CLASSES = "w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
TEXTAREA_CLASSES = "w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"

class ProjectForm(forms.ModelForm):
    """
    Form for creating and editing projects.

    Handles the main project details including name, description, and timeline.
    All fields are required to ensure complete project information.

    Fields:
        name: The project name
        description: Detailed project description
        start_date: Project start date
        end_date: Project end date
    """
    
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']
        labels = {
            'name': 'Project Name',
            'description': 'Description',
            'start_date': 'Start Date',
            'end_date': 'End Date',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'description': forms.Textarea(attrs={'class': TEXTAREA_CLASSES, 'rows': 4}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASSES}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASSES}),
        }

    def clean(self):
        """
        Validate the form data.

        Performs custom validation to ensure:
        1. End date is after start date
        2. Project name is unique for the user
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("End date must be after start date")
        
        return cleaned_data

class CategoryForm(forms.ModelForm):
    """
    Form for creating and editing categories.

    Handles the creation of new budget categories.
    Ensures category names are unique.

    Fields:
        name: The category name
    """
    
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
        }

    def clean_name(self):
        """Ensure category name is unique."""
        name = self.cleaned_data['name']
        if Category.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("A category with this name already exists")
        return name

class BudgetForm(forms.ModelForm):
    """
    Form for creating and editing budget allocations.

    Handles budget allocations for specific categories within a project.
    Ensures proper validation of budget amounts.

    Fields:
        category: The expense category (can be an existing one or a new one)
        amount: The allocated budget amount
    """
    
    category_name = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Enter category name'
        })
    )
    
    class Meta:
        model = Budget
        fields = ['category_name', 'amount']
        labels = {
            'category_name': 'Category Name',
            'amount': 'Budget Amount',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': INPUT_CLASSES, 
                'step': '0.01', 
                'min': '0',
                'placeholder': 'Enter budget amount'
            }),
        }

    def clean_amount(self):
        """Validate that the budget amount is positive."""
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Budget amount must be greater than zero")
        return amount

    def save(self, commit=True):
        """
        Save the budget allocation, creating a new category if needed.
        """
        budget = super().save(commit=False)
        category_name = self.cleaned_data['category_name']
        
        # Get or create the category
        category, created = Category.objects.get_or_create(
            name__iexact=category_name,
            defaults={'name': category_name}
        )
        
        budget.category = category
        
        if commit:
            budget.save()
        return budget

class ExpenseForm(forms.ModelForm):
    """
    Form for creating and editing expenses.

    Handles individual expense entries within a project and category.
    Includes validation to ensure expenses don't exceed budget allocations.

    Fields:
        category: The expense category
        description: Description of the expense
        amount: The expense amount
        date_incurred: Date when the expense occurred
    """
    
    class Meta:
        model = Expense
        fields = ['category', 'description', 'amount', 'date_incurred']
        widgets = {
            'category': forms.Select(attrs={'class': SELECT_CLASSES}),
            'description': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'amount': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'step': '0.01', 'min': '0'}),
            'date_incurred': forms.DateInput(attrs={'type': 'date', 'class': INPUT_CLASSES})
        }

    def clean(self):
        """
        Validate the expense data.

        Performs custom validation to ensure:
        1. Expense amount is positive
        2. Date is within project timeline
        3. Expense doesn't exceed remaining budget
        """
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        date_incurred = cleaned_data.get('date_incurred')

        if amount and amount <= 0:
            raise forms.ValidationError("Expense amount must be greater than zero")

        if self.instance.project:
            if date_incurred:
                if date_incurred < self.instance.project.start_date:
                    raise forms.ValidationError("Expense date cannot be before project start date")
                if date_incurred > self.instance.project.end_date:
                    raise forms.ValidationError("Expense date cannot be after project end date")

        return cleaned_data

# Create formset for handling multiple budget allocations
BudgetFormSet = inlineformset_factory(
    Project, Budget,
    form=BudgetForm,
    fields=('category_name', 'amount'),
    extra=1,
    can_delete=True
)

# Create formset for handling multiple expense entries
ExpenseFormSet = forms.inlineformset_factory(
    Project, Expense,
    form=ExpenseForm,
    extra=1,
    can_delete=True
)