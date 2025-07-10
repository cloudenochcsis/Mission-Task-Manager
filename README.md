# Army Task Manager

A military-themed task management application built for Army task management. This application provides a simple, fast, and clear interface for managing military tasks ("missions") with a camouflage-inspired design.

## Features

- Create, view, update, and delete tasks (missions)
- Military-themed UI with camouflage color palette
- Stencil typography for military aesthetics
- Clean and intuitive interface
- Responsive design
- Form validation
- Comprehensive test coverage

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

1. Clone the repository:
```bash
git clone [repository-url]
cd army_todo
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
army_todo/
├── army_todo/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/              # Main application
│   ├── models.py       # Task model
│   ├── views.py        # View functions
│   ├── forms.py        # Form definitions
│   ├── tests.py        # Integration tests
│   ├── test_units.py   # Unit tests
│   └── templates/      # HTML templates
├── static/             # Static files
│   └── styles.css      # Military-themed styles
├── templates/          # Base templates
└── manage.py          # Django management script
```

## Development

- The application uses Django's built-in SQLite database for development
- Static files are served directly by Django in development mode
- All templates extend from a base template that includes the military styling
- Form validation ensures data integrity
- Transaction atomic operations prevent data inconsistencies

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
