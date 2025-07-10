from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Task
from .forms import TaskForm

class TaskModelTests(TestCase):
    def test_task_creation(self):
        """Test task model creation with valid data"""
        task = Task.objects.create(
            title="Patrol Mission",
            description="Conduct routine patrol in sector A",
            completed=False
        )
        self.assertEqual(task.title, "Patrol Mission")
        self.assertEqual(task.description, "Conduct routine patrol in sector A")
        self.assertFalse(task.completed)
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)

    def test_task_string_representation(self):
        """Test the string representation of a task"""
        task = Task.objects.create(title="Supply Mission")
        self.assertEqual(str(task), "Supply Mission")

    def test_task_timestamps(self):
        """Test that timestamps are set correctly"""
        task = Task.objects.create(title="Time Sensitive Mission")
        self.assertLessEqual(task.created_at, timezone.now())
        self.assertLessEqual(task.updated_at, timezone.now())

    def test_task_title_max_length(self):
        """Test task title max length validation"""
        long_title = "A" * 201  # 201 characters
        with self.assertRaises(ValidationError):
            task = Task(title=long_title)
            task.full_clean()

class TaskFormTests(TestCase):
    def test_valid_form(self):
        """Test form with valid data"""
        form_data = {
            'title': 'Training Exercise',
            'description': 'Conduct training exercise in field',
            'completed': False
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Test form with invalid data"""
        form_data = {
            'title': '',  # Title is required
            'description': 'Test description'
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_widgets(self):
        """Test that form widgets are properly configured"""
        form = TaskForm()
        self.assertEqual(
            form.fields['title'].widget.attrs['placeholder'],
            'Mission objective'
        )
        self.assertEqual(
            form.fields['description'].widget.attrs['placeholder'],
            'Operation details'
        )

    def test_form_field_types(self):
        """Test form field types and attributes"""
        form = TaskForm()
        self.assertTrue(form.fields['title'].required)
        self.assertFalse(form.fields['description'].required)
        self.assertFalse(form.fields['completed'].required)

class TaskValidationTests(TestCase):
    def test_blank_description(self):
        """Test that blank description is allowed"""
        task = Task.objects.create(
            title="Quick Mission",
            description=""
        )
        task.full_clean()  # Should not raise ValidationError

    def test_duplicate_titles_allowed(self):
        """Test that duplicate titles are allowed"""
        title = "Routine Patrol"
        Task.objects.create(title=title)
        Task.objects.create(title=title)  # Should not raise any exception
        self.assertEqual(Task.objects.filter(title=title).count(), 2)

    def test_completed_default_value(self):
        """Test that completed field defaults to False"""
        task = Task.objects.create(title="New Mission")
        self.assertFalse(task.completed)

    def test_update_timestamps(self):
        """Test that updated_at changes on update"""
        task = Task.objects.create(title="Time Test")
        original_updated_at = task.updated_at
        
        # Wait a small amount of time
        import time
        time.sleep(0.1)
        
        task.title = "Updated Time Test"
        task.save()
        self.assertGreater(task.updated_at, original_updated_at)
