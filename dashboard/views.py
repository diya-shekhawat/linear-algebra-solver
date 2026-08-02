from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from courses.models import Lesson, Progress, Bookmark, Note, Unit
from quiz.models import QuizResult, Quiz
from accounts.models import Profile

@login_required
def student_dashboard(request):
    """
    Renders the Student Dashboard with progress overview, quiz scores, learning streak,
    bookmarks, notes, and recommended lessons.
    """
    user = request.user
    profile = getattr(user, 'profile', None)
    if profile:
        profile.update_streak()

    total_lessons = Lesson.objects.count()
    user_progress = Progress.objects.filter(user=user, completed=True).select_related('lesson__topic')
    completed_lessons_count = user_progress.count()

    progress_percentage = (completed_lessons_count / total_lessons * 100) if total_lessons > 0 else 0

    recent_results = QuizResult.objects.filter(user=user).select_related('quiz__topic')[:5]
    avg_score = QuizResult.objects.filter(user=user).aggregate(Avg('percentage'))['percentage__avg'] or 0

    bookmarks = Bookmark.objects.filter(user=user).select_related('lesson__topic')[:6]
    notes = Note.objects.filter(user=user).select_related('lesson')[:5]

    completed_lesson_ids = set(user_progress.values_list('lesson_id', flat=True))
    
    # Recommended lessons: uncompleted lessons ordered by unit & order
    recommended_lessons = Lesson.objects.exclude(id__in=completed_lesson_ids).select_related('topic__unit')[:4]

    recent_lessons = Lesson.objects.filter(id__in=completed_lesson_ids).select_related('topic')[:5]

    context = {
        'profile': profile,
        'total_lessons': total_lessons,
        'completed_lessons_count': completed_lessons_count,
        'progress_percentage': round(progress_percentage, 1),
        'recent_results': recent_results,
        'avg_score': round(avg_score, 1),
        'bookmarks': bookmarks,
        'notes': notes,
        'recommended_lessons': recommended_lessons,
        'recent_lessons': recent_lessons,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def admin_dashboard(request):
    """
    Admin control panel view displaying system statistics:
    Student count, quiz attempts, progress statistics, and recent registrations.
    """
    if not request.user.is_staff:
        return redirect('dashboard:student_dashboard')

    total_students = User.objects.filter(is_staff=False).count()
    total_quiz_attempts = QuizResult.objects.count()
    pass_rate = (QuizResult.objects.filter(passed=True).count() / total_quiz_attempts * 100) if total_quiz_attempts > 0 else 0

    recent_users = User.objects.order_by('-date_joined')[:10]
    recent_quiz_attempts = QuizResult.objects.select_related('user', 'quiz').order_by('-completed_at')[:10]

    unit_progress = Unit.objects.annotate(
        topic_count=Count('topics')
    )

    context = {
        'total_students': total_students,
        'total_quiz_attempts': total_quiz_attempts,
        'pass_rate': round(pass_rate, 1),
        'recent_users': recent_users,
        'recent_quiz_attempts': recent_quiz_attempts,
        'unit_progress': unit_progress,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
