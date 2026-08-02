from django.contrib import admin
from .models import Quiz, Question, Answer, QuizResult

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'marks')
    list_filter = ('quiz__topic__unit', 'quiz')
    inlines = [AnswerInline]

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'time_limit_minutes', 'pass_mark_percentage')
    list_filter = ('topic__unit', 'topic')

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'total_questions', 'percentage', 'passed', 'completed_at')
    list_filter = ('passed', 'completed_at')
    search_fields = ('user__username', 'quiz__title')
