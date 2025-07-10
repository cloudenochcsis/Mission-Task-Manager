from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from django.utils import timezone
from .models import Task
from .forms import TaskForm

# Create your views here.

def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Check if a task with the same title was created in the last minute
                    title = form.cleaned_data['title']
                    recent_task = Task.objects.filter(
                        title=title,
                        created_at__gte=timezone.now() - timezone.timedelta(minutes=1)
                    ).first()
                    
                    if recent_task:
                        messages.warning(request, f'Mission "{title}" was already created recently.')
                        return redirect('task_list')
                    
                    # Save the task and show success message
                    task = form.save()
                    messages.success(request, f'Mission "{task.title}" successfully created.')
                    return redirect('task_list')
            except Exception as e:
                messages.error(request, f'Error creating mission: {str(e)}')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    return redirect('task_list')
            except Exception as e:
                form.add_error(None, 'An error occurred while updating the task.')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

def task_delete(request, pk):
    try:
        # First verify the task exists
        task = Task.objects.filter(pk=pk).first()
        if not task:
            messages.error(request, f'Task with ID {pk} not found.')
            return redirect('task_list')

        if request.method == 'POST':
            try:
                with transaction.atomic():
                    task_title = task.title  # Store title before deletion
                    task.delete()
                    messages.success(request, f'Mission "{task_title}" successfully terminated.')
                    return redirect('task_list')
            except Exception as e:
                messages.error(request, f'Error deleting task: {str(e)}')
                return redirect('task_list')
        
        # GET request - show confirmation page
        return render(request, 'tasks/task_confirm_delete.html', {'task': task})
    except Exception as e:
        messages.error(request, f'Unexpected error: {str(e)}')
        return redirect('task_list')
