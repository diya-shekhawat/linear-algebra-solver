from django.contrib import admin
from .models import Unit, Topic, Lesson, Bookmark, Note, Progress

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit_number', 'title')
    ordering = ('unit_number',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit', 'order')
    list_filter = ('unit',)
    ordering = ('unit', 'order')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'order', 'has_interactive_calculator')
    list_filter = ('topic__unit', 'topic', 'has_interactive_calculator')
    search_fields = ('title', 'theory')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'created_at')
    search_fields = ('user__username', 'lesson__title')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'lesson', 'updated_at')
    search_fields = ('user__username', 'title', 'content')

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'completed_at')
    list_filter = ('completed',)
