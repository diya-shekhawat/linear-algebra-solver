from django.db import models
from django.contrib.auth.models import User

class Unit(models.Model):
    unit_number = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='bi-diagram-3')

    class Meta:
        ordering = ['unit_number']

    def __str__(self):
        return f"Unit {self.unit_number}: {self.title}"

class Topic(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=1)

    class Meta:
        ordering = ['unit', 'order']

    def __str__(self):
        return f"{self.unit.title} - {self.title}"

class Lesson(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=1)
    introduction = models.TextField(help_text="Lesson overview and high level context")
    objectives = models.TextField(help_text="Bullet points of lesson learning objectives")
    theory = models.TextField(help_text="In-depth theoretical explanation with MathJax LaTeX support")
    definitions = models.TextField(help_text="Key definitions and terminology")
    formula_cards = models.TextField(help_text="JSON or text formatted key formulas with LaTeX")
    worked_examples = models.TextField(help_text="Step-by-step solved examples")
    practice_questions = models.TextField(help_text="Interactive practice questions")
    summary = models.TextField(help_text="Lesson summary recap")
    references = models.TextField(blank=True, default="1. Strang, G. (2016). Introduction to Linear Algebra.\n2. Lay, D. C. (2012). Linear Algebra and Its Applications.")
    has_interactive_calculator = models.BooleanField(default=False)
    calculator_type = models.CharField(max_length=50, blank=True, help_text="e.g. matrix, vector, system, transformation")

    class Meta:
        ordering = ['topic', 'order']

    def __str__(self):
        return f"{self.topic.title} - {self.title}"

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} bookmarked {self.lesson.title}"

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_records')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_entries')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}: {'Completed' if self.completed else 'In Progress'}"
