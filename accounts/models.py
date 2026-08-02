from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, default="Passionate Linear Algebra Learner!")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    learning_streak = models.IntegerField(default=1)
    last_activity_date = models.DateField(default=timezone.now)
    total_quiz_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def update_streak(self):
        """Update daily study streak count."""
        today = timezone.now().date()
        if self.last_activity_date == today:
            return
        elif self.last_activity_date == today - timezone.timedelta(days=1):
            self.learning_streak += 1
        else:
            self.learning_streak = 1
        self.last_activity_date = today
        self.save()

    def __str__(self):
        return f"{self.user.username}'s Profile"
