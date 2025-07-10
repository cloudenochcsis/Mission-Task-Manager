# Army Task Manager

A military-themed task management application built for Army task management. This application provides a simple, fast, and clear interface for managing military tasks ("missions") with a camouflage-inspired design.

## Features

- Create, view, update, and delete tasks (missions)
- Military-themed UI with camouflage color palette
- Stencil typography for military aesthetics
- Clean and intuitive interface
- Responsive design
- Form validation with duplicate prevention
- Military-themed success/error messages
- Comprehensive test coverage
- Transaction-safe operations

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/cloudenochcsis/Mission-Task-Manager.git
cd Mission-Task-Manager
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- On macOS/Linux:
```bash
source venv/bin/activate
```
- On Windows:
```bash
.\venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Apply database migrations:
```bash
python manage.py migrate
```

> **Note:** If you encounter a `ModuleNotFoundError: No module named 'army_todo'` error when running migrations, this is because the project structure has been updated. The settings have been fixed in the latest version of the repository.

## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:8000/
```

## Running Tests

To run all tests:
```bash
python manage.py test
```

To run specific test suites:
```bash
# Run integration tests
python manage.py test tasks.tests.TaskIntegrationTests

# Run unit tests
python manage.py test tasks.test_units
```

## Project Structure

```
./
├── __init__.py        # Project initialization
├── settings.py        # Project settings
├── urls.py            # Project URL configuration
├── wsgi.py            # WSGI configuration
├── asgi.py            # ASGI configuration
├── tasks/             # Main application
│   ├── models.py      # Task model
│   ├── views.py       # View functions with error handling
│   ├── forms.py       # Form definitions with validation
│   ├── tests.py       # Integration tests
│   ├── test_units.py  # Unit tests
│   ├── urls.py        # App URL configuration
│   └── templates/     # Task-specific templates
├── static/            # Static files
│   └── styles.css     # Military-themed styles
├── templates/         # Base templates
│   └── base.html      # Base template with message display
├── manage.py          # Django management script
└── requirements.txt   # Project dependencies
```

## Features in Detail

### Task Management
- Create new missions with title and description
- View all current missions in a military-styled list
- Update mission details and status
- Delete missions with confirmation

### Data Protection
- Duplicate mission prevention (within 1-minute window)
- Transaction-safe database operations
- CSRF protection on all forms

### User Interface
- Military-themed color scheme (army green, olive drab, khaki)
- Stencil typography for headers
- Clear success/error messages with military styling
- Responsive design for all screen sizes

### Error Handling
- Graceful handling of all CRUD operations
- Clear feedback messages for users
- Proper validation of all inputs
- Safe deletion with confirmation

## Contributing

1. Write tests for new features
2. Ensure all tests pass before submitting changes
3. Follow the military theme guidelines for UI changes
4. Maintain clean code practices and documentation

## Security Notes

This is a proof of concept and may need additional security measures before production deployment:

- Add user authentication
- Implement role-based access control
- Add API rate limiting
- Configure proper production settings
- Set up proper static file serving

## Troubleshooting

### ModuleNotFoundError: No module named 'army_todo'

If you encounter this error when running migrations or starting the server, it means the Django settings module reference is incorrect. This has been fixed in the latest version, but if you're still experiencing it:

1. Open `manage.py` and change:
   ```python
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'army_todo.settings')
   ```
   to:
   ```python
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
   ```

2. Open `settings.py` and update:
   ```python
   ROOT_URLCONF = 'army_todo.urls'
   WSGI_APPLICATION = 'army_todo.wsgi.application'
   ```
   to:
   ```python
   ROOT_URLCONF = 'urls'
   WSGI_APPLICATION = 'wsgi.application'
   ```

### TemplateDoesNotExist: base.html

If you encounter this error when accessing the web interface, it means Django can't find the base template. To fix this:

1. Make sure `base.html` exists in both the `/templates` directory and the `/tasks/templates` directory.
2. If it doesn't exist in `/tasks/templates`, copy it there:
   ```bash
   cp templates/base.html tasks/templates/
   ```

### Static Files Not Loading (404 Error for styles.css)

If static files like CSS are not loading, check the STATICFILES_DIRS setting in `settings.py`. It should point to the correct absolute path:

```python
STATICFILES_DIRS = ['/path/to/your/project/static']
```

Replace `/path/to/your/project` with the actual path to your project directory.
