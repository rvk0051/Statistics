from django.urls import path
from .views import placement_stats, get_chart_data, get_salary_distribution   

urlpatterns = [
    path('placement-stats/', placement_stats, name='placement_stats'),  # API endpoint
    path('get_chart_data/', get_chart_data, name='get_chart_data'),
    path('get_salary_distribution/', get_salary_distribution, name='get_salary_distribution')
]