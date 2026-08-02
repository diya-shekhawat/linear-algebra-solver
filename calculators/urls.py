from django.urls import path
from . import views

app_name = 'calculators'

urlpatterns = [
    path('matrix/', views.matrix_calculator, name='matrix'),
    path('vector/', views.vector_calculator, name='vector'),
    path('system/', views.system_solver, name='system'),
    path('transformations/', views.linear_transformations, name='transformations'),
]
