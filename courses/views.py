from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Unit, Topic, Lesson, Bookmark, Note, Progress

def course_index(request):
    """
    Renders the full curriculum overview grouped by Units and Topics.
    """
    units = Unit.objects.all().prefetch_related('topics__lessons')
    
    user_completed_lesson_ids = set()
    if request.user.is_authenticated:
        user_completed_lesson_ids = set(
            Progress.objects.filter(user=request.user, completed=True).values_list('lesson_id', flat=True)
        )

    context = {
        'units': units,
        'completed_ids': user_completed_lesson_ids
    }
    return render(request, 'courses/course_index.html', context)

def topic_detail(request, topic_id):
    """
    Shows topic details and all associated lessons.
    """
    topic = get_object_or_404(Topic.objects.select_related('unit'), id=topic_id)
    lessons = topic.lessons.all()

    completed_ids = set()
    if request.user.is_authenticated:
        completed_ids = set(
            Progress.objects.filter(user=request.user, completed=True).values_list('lesson_id', flat=True)
        )

    context = {
        'topic': topic,
        'lessons': lessons,
        'completed_ids': completed_ids
    }
    return render(request, 'courses/topic_detail.html', context)

def lesson_detail(request, lesson_id):
    """
    Full learning page for a specific lesson with LaTeX formulas, examples, and study tools.
    """
    lesson = get_object_or_404(
        Lesson.objects.select_related('topic__unit').prefetch_related('topic__lessons'),
        id=lesson_id
    )

    is_bookmarked = False
    is_completed = False
    user_notes = []

    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, lesson=lesson).exists()
        is_completed = Progress.objects.filter(user=request.user, lesson=lesson, completed=True).exists()
        user_notes = Note.objects.filter(user=request.user, lesson=lesson)
        request.user.profile.update_streak()

    # Next & Previous lesson navigation
    all_lessons = list(Lesson.objects.all())
    current_index = next((i for i, l in enumerate(all_lessons) if l.id == lesson.id), None)
    prev_lesson = all_lessons[current_index - 1] if current_index is not None and current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index is not None and current_index < len(all_lessons) - 1 else None

    context = {
        'lesson': lesson,
        'is_bookmarked': is_bookmarked,
        'is_completed': is_completed,
        'user_notes': user_notes,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
    }
    return render(request, 'courses/lesson_detail.html', context)

@login_required
def toggle_bookmark(request, lesson_id):
    """
    AJAX endpoint to bookmark or un-bookmark a lesson.
    """
    lesson = get_object_or_404(Lesson, id=lesson_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, lesson=lesson)
    
    if not created:
        bookmark.delete()
        bookmarked = False
        msg = "Bookmark removed."
    else:
        bookmarked = True
        msg = "Lesson bookmarked successfully!"

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'bookmarked': bookmarked, 'message': msg})
    
    messages.success(request, msg)
    return redirect('courses:lesson_detail', lesson_id=lesson.id)

@login_required
def toggle_complete(request, lesson_id):
    """
    AJAX endpoint to toggle lesson completion state.
    """
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress, created = Progress.objects.get_or_create(user=request.user, lesson=lesson)
    
    if not created and progress.completed:
        progress.completed = False
        progress.save()
        completed = False
        msg = "Lesson marked as incomplete."
    else:
        progress.completed = True
        progress.save()
        completed = True
        msg = "Lesson marked as completed!"

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'completed': completed, 'message': msg})

    messages.success(request, msg)
    return redirect('courses:lesson_detail', lesson_id=lesson.id)

@login_required
def save_note(request, lesson_id):
    """
    Creates or updates a user note for a lesson.
    """
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        note_id = request.POST.get('note_id')
        title = request.POST.get('title', 'Study Note').strip()
        content = request.POST.get('content', '').strip()

        if content:
            if note_id:
                note = get_object_or_404(Note, id=note_id, user=request.user)
                note.title = title
                note.content = content
                note.save()
                messages.success(request, 'Note updated successfully!')
            else:
                Note.objects.create(user=request.user, lesson=lesson, title=title, content=content)
                messages.success(request, 'Note added successfully!')
        else:
            messages.error(request, 'Note content cannot be empty.')

    return redirect('courses:lesson_detail', lesson_id=lesson.id)

@login_required
def delete_note(request, note_id):
    """
    Deletes a user note.
    """
    note = get_object_or_404(Note, id=note_id, user=request.user)
    lesson_id = note.lesson.id
    note.delete()
    messages.success(request, 'Note deleted successfully.')
    return redirect('courses:lesson_detail', lesson_id=lesson_id)
