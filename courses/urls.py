from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_index, name='index'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:lesson_id>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('lesson/<int:lesson_id>/complete/', views.toggle_complete, name='toggle_complete'),
    path('lesson/<int:lesson_id>/note/save/', views.save_note, name='save_note'),
    path('note/<int:note_id>/delete/', views.delete_note, name='delete_note'),
]
