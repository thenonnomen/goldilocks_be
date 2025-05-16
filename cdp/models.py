from django.db import models

# Create your models here.
class GoldilocksCDP(models.Model):
    name = models.CharField(max_length=255)
    headquarters = models.CharField(max_length=255, blank=True, null=True)
    revenue = models.JSONField(help_text="Time series data for revenue")
    industry = models.CharField(max_length=255, blank=True, null=True)
    ceo = models.CharField(max_length=255, blank=True, null=True)
    cfo = models.CharField(max_length=255, blank=True, null=True)
    employees = models.JSONField(help_text="Time series data for employee count")
    founded = models.DateField(blank=True, null=True)
    marketCap = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    digital_traffic = models.JSONField(help_text="Time series data for digital traffic")
    sector = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
# ====================================================================================================================================
FIDELITY_CHOICES = (
    ("High", "High"),
    ("Medium", "Medium"),
    ("Low", "Low")
)

class PrimaryCompanyInfo(models.Model):
    company_name = models.TextField(max_length=255)
    company_domain = models.URLField(max_length=2000)
    linkedin_company_profile = models.URLField(max_length=2000, blank=True, null=True)
    country_code = models.TextField(max_length=10)
    locations = models.TextField()
    company_size = models.TextField(max_length=50)
    organization_type = models.TextField(max_length=100)
    industries = models.TextField()
    crunchbase_url = models.URLField(max_length=2000)
    founded = models.IntegerField(null=True, blank=True)
    headquarters = models.TextField(max_length=255)
    image = models.URLField(blank=True, null=True, max_length=2000)
    logo = models.URLField(max_length=2000)
    get_directions_url = models.URLField(max_length=2000, blank=True, null=True)
    sic_code = models.TextField(max_length=20, blank=True, null=True)
    name_sectors = models.TextField()
    parent_industry_sectors = models.TextField()
    company_id = models.IntegerField(unique=True, default=0)
    data_fidelity = models.TextField(choices=FIDELITY_CHOICES, default="Low")

    def __str__(self):
        return self.company_name


class SecondaryCompanyInfo(models.Model):
    primary_info = models.OneToOneField(PrimaryCompanyInfo, on_delete=models.CASCADE, related_name='secondary_info')
    employee_count = models.IntegerField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    specialties = models.TextField(blank=True, null=True)
    similar = models.JSONField(help_text= "Companies that are similar to he selected comapny.",blank=True, null=True)
    updates = models.TextField(blank=True, null=True)
    slogan = models.CharField(max_length=2550, blank=True, null=True)
    affiliated = models.TextField(blank=True, null=True)
    investors = models.TextField(blank=True, null=True)
    parent_website = models.URLField(blank=True, null=True, max_length=2000)
    parent_name = models.CharField(max_length=2550, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Details of {self.primary_info.company_name}"


class FinancialInfo(models.Model):
    primary_info = models.OneToOneField(PrimaryCompanyInfo, on_delete=models.CASCADE, related_name='financial_info')
    employee_count = models.IntegerField(blank=True, null=True)
    total_funding = models.BigIntegerField(blank=True, null=True)
    latest_funding_round = models.CharField(max_length=100, blank=True, null=True)
    revenue = models.CharField(max_length=100, blank=True, null=True)
    first_name_ceo = models.CharField(max_length=100)
    last_name_ceo = models.CharField(max_length=100)
    ceo_rating = models.CharField(max_length=100)

    def __str__(self):
        return f"Financial info for {self.primary_info.company_name}"


class BusinessTracker(models.Model):
    primary_info = models.OneToOneField(PrimaryCompanyInfo, on_delete=models.CASCADE, related_name='business_tracker')
    organic_social_visits = models.BigIntegerField(blank=True, null=True)
    organic_search_visits = models.BigIntegerField(blank=True, null=True)
    paid_social_visits = models.BigIntegerField(blank=True, null=True)
    paid_search_visits = models.BigIntegerField(blank=True, null=True)
    display_ad_visits = models.BigIntegerField(blank=True, null=True)
    referral_visits = models.BigIntegerField(blank=True, null=True)
    social_visits = models.BigIntegerField(blank=True, null=True)
    search_visits = models.BigIntegerField(blank=True, null=True)
    direct_visits = models.BigIntegerField(blank=True, null=True)
    paid_visits = models.BigIntegerField(blank=True, null=True)
    mail_visits = models.BigIntegerField(blank=True, null=True)
    average_pages_per_visit = models.FloatField(blank=True, null=True)
    average_time_on_site = models.FloatField(blank=True, null=True)
    average_bounce_rate = models.FloatField(blank=True, null=True)
    traffic_rank = models.BigIntegerField(blank=True, null=True)
    total_visits = models.BigIntegerField(blank=True, null=True)
    total_users = models.BigIntegerField(blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True, max_length=2000)
    twitter_link = models.URLField(blank=True, null=True, max_length=2000)
    facebook_link = models.URLField(blank=True, null=True, max_length=2000)
    linkedin_followers = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Web traffic for {self.primary_info.company_name}"
