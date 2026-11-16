from django.contrib import admin

from .models import Comment, Label, Task


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'status', 'priority', 'assignee', 'due_date']
    list_filter = ['status', 'priority', 'project']
    search_fields = ['title', 'description']
    filter_horizontal = ['labels']
    inlines = [CommentInline]


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'color']
    list_filter = ['project']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'author', 'created_at']
