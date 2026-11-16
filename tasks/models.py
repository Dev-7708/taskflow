from django.conf import settings
from django.db import models

from projects.models import Project


class Label(models.Model):
    """A coloured tag that can be attached to tasks within one project."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='labels',
    )
    name = models.CharField(max_length=40)
    color = models.CharField(
        max_length=7,
        default='#6366f1',
        help_text='Hex colour, e.g. #6366f1',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'name'],
                name='unique_label_per_project',
            )
        ]
        ordering = ['name']

    def __str__(self):
        return self.name


class Task(models.Model):
    """A card on the Kanban board."""

    class Status(models.TextChoices):
        TODO = 'todo', 'To Do'
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE = 'done', 'Done'

    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tasks',
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
        related_name='tasks',
    )
    # Ordering of the card inside its column. Without this the board
    # reshuffles every time it is reloaded.
    position = models.PositiveIntegerField(default=0)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['status', 'position', '-created_at']
        indexes = [
            models.Index(fields=['project', 'status']),
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    """A message left on a task."""

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author} on {self.task}'
