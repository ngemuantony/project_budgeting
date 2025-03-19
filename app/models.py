"""
Models for the project budgeting application.

This module contains the core models that represent the domain entities of the budgeting system:
- Project: Represents a project with its budget allocations
- Category: Represents expense categories for budget allocation
- Budget: Links projects with categories and their allocated amounts
- Expense: Tracks actual expenses within projects and categories
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

class Category(models.Model):
    """
    Represents a budget/expense category.

    Categories are used to classify different types of expenses and budget allocations.
    They help in organizing and tracking project finances effectively.

    Attributes:
        name (str): The name of the category
        description (text): Detailed description of what the category encompasses
    """
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the category."""
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Project(models.Model):
    """
    Represents a project with budget allocations and expenses.

    A project is owned by a user and can have multiple budget allocations across
    different categories. It tracks the project timeline and overall status.

    Attributes:
        name (str): The name of the project
        description (text): Detailed description of the project
        owner (User): The user who created and owns the project
        start_date (date): Project start date
        end_date (date): Project end date
        created_at (datetime): Timestamp of project creation
        updated_at (datetime): Timestamp of last update
        status (str): Current status of the project (draft/pending/approved/rejected/completed)
    """
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_projects')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        """Return a string representation of the project."""
        return self.name

    @property
    def total_budget(self):
        """Calculate and return the total budget allocated across all categories."""
        return sum(budget.amount for budget in self.budgets.all())

    @property
    def total_expenses(self):
        """Calculate and return the total expenses across all categories."""
        return sum(expense.amount for expense in self.expenses.all())

    @property
    def budget_remaining(self):
        """Calculate and return the remaining budget (total budget - total expenses)."""
        return self.total_budget - self.total_expenses

class Budget(models.Model):
    """
    Represents a budget allocation for a specific category within a project.

    Links projects with categories and specifies the amount allocated for each category.
    This helps in tracking how the project budget is distributed across different expense types.

    Attributes:
        project (Project): The project this allocation belongs to
        category (Category): The category this allocation is for
        amount (decimal): The amount allocated for this category
    """
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the budget allocation."""
        return f"{self.project.name} - {self.category.name} Budget"

class Expense(models.Model):
    """
    Represents an actual expense within a project.

    Tracks individual expenses, linking them to specific projects and categories.
    This allows for detailed expense tracking and budget monitoring.

    Attributes:
        project (Project): The project this expense belongs to
        category (Category): The category this expense falls under
        description (text): Detailed description of the expense
        amount (decimal): The amount spent
        date_incurred (date): The date the expense was incurred
        created_at (datetime): Timestamp of when the expense was recorded
    """
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    description = models.TextField()
    date_incurred = models.DateField()
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the expense."""
        return f"{self.project.name} - {self.category.name} Expense ({self.date_incurred})"