from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo_url = models.CharField(max_length=500)
    details_url = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name
    
class PlacedStudent(models.Model):
    student_id = models.CharField(max_length=10, primary_key=True)
    student_name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    placement_year = models.IntegerField()
    salary_lpa=models.FloatField()
    def __str__(self):
        return self.student_name

