from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('<int:quiz_id>/take/', views.quiz_take, name='quiz_take'),
    path('result/<int:result_id>/', views.quiz_result, name='quiz_result'),
    path('history/', views.quiz_history, name='quiz_history'),
]
