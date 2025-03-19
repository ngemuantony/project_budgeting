# Project Budgeting System

A comprehensive Django-based project management and budgeting system that helps users track project expenses and manage budgets effectively.

## Features

- **Project Management**
  - Create and manage projects with detailed information
  - Track project timelines with start and end dates
  - Monitor project status (draft/pending/approved/rejected/completed)
  - View project progress and budget utilization

- **Budget Management**
  - Set budgets for different expense categories
  - Track allocated vs actual expenses
  - Dynamic budget allocation forms
  - Real-time budget utilization tracking

- **Expense Tracking**
  - Record and categorize expenses
  - Track expense dates and descriptions
  - Monitor expenses against budget allocations
  - Generate expense reports

- **User Interface**
  - Modern, responsive design using Tailwind CSS
  - Dark mode support
  - Dynamic forms with JavaScript
  - Clean and intuitive navigation

## Technology Stack

- **Backend**
  - Django 5.1.4
  - Python 3.12.3
  - SQLite (Development) / PostgreSQL (Production)

- **Frontend**
  - HTML5
  - Tailwind CSS
  - JavaScript (Vanilla)
  - HTMX for dynamic content

- **Development Tools**
  - Node.js & NPM (for Tailwind CSS)
  - Git for version control

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd django-starter
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Node.js dependencies:
   ```bash
   npm install
   ```

5. Set up the database:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Build the CSS:
   ```bash
   npx tailwindcss -i ./static/css/input.css -o ./static/css/dist/styles.css --minify
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
django-starter/
├── app/                    # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── forms.py           # Form definitions
│   └── urls.py            # URL routing
├── config/                 # Project configuration
│   ├── settings/          # Settings modules
│   │   ├── base.py       # Base settings
│   │   ├── development.py # Development settings
│   │   └── production.py  # Production settings
│   └── urls.py            # Main URL routing
├── static/                # Static files
│   ├── css/              # CSS files
│   └── js/               # JavaScript files
├── templates/            # HTML templates
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
└── package.json         # Node.js dependencies
```

## Usage

1. **Creating a Project**
   - Navigate to "Create Project"
   - Fill in project details
   - Add budget categories and allocations
   - Submit the form

2. **Managing Budgets**
   - View project details
   - Add/edit budget allocations
   - Monitor budget utilization

3. **Recording Expenses**
   - Navigate to project expenses
   - Add new expenses with categories
   - Track expense history

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django Framework
- Tailwind CSS
- HTMX
- All contributors and users of the system
