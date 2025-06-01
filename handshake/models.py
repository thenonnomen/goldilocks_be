from django.db import models
from cdp.models import PrimaryCompanyInfo
from django.contrib.auth.models import User
from thesis.models import ThesisCompanyProfile
# Create your models here.

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    din = models.CharField("DIN", max_length=20, unique=True)
    designation = models.CharField(max_length=255)
    date_of_appointment = models.DateField()
    date_of_cessation = models.DateField(null=True, blank=True)
    past_companies = models.ManyToManyField(PrimaryCompanyInfo, related_name='former_employees', blank=True)
    current_company = models.ForeignKey(
        PrimaryCompanyInfo, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_employees'
    )

    def __str__(self):
        return f"{self.designation} - {self.user.get_full_name() or self.user.username}"


class Pathway(models.Model):
    CONNECTION_STRENGTH_CHOICES = [
        ('STRONG', 'Strong'),
        ('WEAK', 'Weak'),
        ('MEDIUM', 'Medium'),
    ]

    STATUS_CHOICES = [
        ('CONNECTED', 'Connected'),
        ('PENDING', 'Pending'),
        ('EXPLORE', 'Explore'),
        ('OBSOLETE', 'Obsolete'),
    ]

    relationship = models.CharField(max_length=255)
    target_company = models.ForeignKey(PrimaryCompanyInfo, on_delete=models.CASCADE, related_name='pathways')
    connection_strength = models.CharField(max_length=10, choices=CONNECTION_STRENGTH_CHOICES)
    match_score = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.relationship} → {self.target_company.name}"


class Connection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connection_emp')
    company = models.ForeignKey(ThesisCompanyProfile, on_delete=models.CASCADE, related_name='conectiom_company')