from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'learning_streak', 'total_quiz_score', 'last_activity_date', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('learning_streak', 'last_activity_date')
