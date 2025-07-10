from django.test import TestCase, Client
from django.urls import reverse
from bs4 import BeautifulSoup
from .models import Task
from datetime import datetime

class TaskIntegrationTests(TestCase):
    def setUp(self):
        # Set up test client
        self.client = Client()
        # Create a sample task for testing
        self.test_task = Task.objects.create(
            title='Test Mission',
            description='Test mission description',
            completed=False
        )

    def test_task_list_view(self):
        """Test that the task list view displays correctly"""
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertContains(response, 'Test Mission')
        # Verify only one instance of the task title exists
        self.assertEqual(response.content.decode().count('Test Mission'), 1)

    def test_task_create_no_duplicate(self):
        """Test task creation without duplication"""
        initial_count = Task.objects.count()
        task_data = {
            'title': 'New Mission',
            'description': 'New mission description',
            'completed': False
        }
        
        # Create task
        response = self.client.post(reverse('task_create'), task_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Verify exactly one task was created
        self.assertEqual(Task.objects.count(), initial_count + 1)
        new_task = Task.objects.get(title='New Mission')
        
        # Follow the redirect
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        
        # Get all task cards from the response
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        task_cards = soup.find_all('div', class_='task-card')
        
        # Count how many times this task appears
        matching_cards = [card for card in task_cards 
                         if new_task.title in card.find('h3').text]
        self.assertEqual(len(matching_cards), 1, 
                        'Task appears multiple times in the list')

    def test_task_delete_from_list(self):
        """Test task deletion directly from task list"""
        # Create a test task
        task = Task.objects.create(
            title='Delete Test Mission',
            description='Mission to be deleted'
        )
        
        # Send POST request to delete the task
        response = self.client.post(reverse('task_delete', args=[task.pk]))
        
        # Should redirect to task list
        self.assertEqual(response.status_code, 302)
        
        # Follow the redirect
        response = self.client.get(response.url)
        
        # Verify task is deleted from database
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
        
        # Task should not appear in the task list section
        soup = BeautifulSoup(response.content, 'html.parser')
        task_list = soup.find('div', class_='task-list')
        self.assertNotIn('Delete Test Mission', task_list.text)
        
        # Verify success message is displayed
        self.assertContains(response, 'successfully terminated')

    def test_task_delete_with_confirmation(self):
        """Test task deletion through confirmation page"""
        # Create a task to delete
        task = Task.objects.create(
            title='Confirm Delete Mission',
            description='To be deleted with confirmation'
        )
        
        # Get confirmation page
        response = self.client.get(reverse('task_delete', args=[task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_confirm_delete.html')
        
        # Confirm deletion
        response = self.client.post(reverse('task_delete', args=[task.pk]))
        self.assertEqual(response.status_code, 302)
        
        # Verify task is deleted
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_task_create_validation_empty_title(self):
        """Test validation for task creation"""
        initial_count = Task.objects.count()
        response = self.client.post(reverse('task_create'), {'title': ''})
        
        # Should stay on form page
        self.assertEqual(response.status_code, 200)
        
        # No new task should be created
        self.assertEqual(Task.objects.count(), initial_count)
        
        # Should show error in the rendered HTML
        self.assertContains(response, 'This field is required')

    def test_concurrent_operations(self):
        """Test handling of concurrent create/delete operations"""
        # Create multiple tasks rapidly
        tasks_data = [
            {'title': f'Concurrent Mission {i}', 'description': f'Test {i}'}
            for i in range(3)
        ]
        
        initial_count = Task.objects.count()
        
        # Create tasks
        for task_data in tasks_data:
            self.client.post(reverse('task_create'), task_data)
        
        # Verify exact number of tasks created
        self.assertEqual(
            Task.objects.count(),
            initial_count + len(tasks_data)
        )
        
        # Verify no duplicates in list view
        response = self.client.get(reverse('task_list'))
        for i in range(3):
            self.assertEqual(
                response.content.decode().count(f'Concurrent Mission {i}'),
                1
            )
