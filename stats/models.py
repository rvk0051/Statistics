from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo_url = models.CharField(max_length=255)
    details_url = models.URLField(blank=True, null=True)
    def __str__(self):
        return self.name
    
class PlacedStudent(models.Model):
    student_id = models.CharField(max_length=10, primary_key=True)
    student_name = models.CharField(max_length=255)
    branch = models.CharField(max_length=200, default="Unknown")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    placement_year = models.IntegerField()
    salary_lpa=models.FloatField()
    photo= models.ImageField(upload_to='achievers/', default='achievers/Designer_1.png',blank=True, null=True) 

    def __str__(self):
        return self.student_name

