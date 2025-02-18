from django.contrib import admin
from .models import Company, PlacedStudent, SalaryDistribution

admin.site.register(Company)
admin.site.register(PlacedStudent)
admin.site.register(SalaryDistribution)