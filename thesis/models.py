from django.db import models

class ThesisQueryResult(models.Model):
    query = models.TextField()
    query_key = models.TextField()
    query_id = models.CharField(max_length=255, unique=True)  # ID from ChromaDB
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query {self.id}: {self.query[:50]}..."

class ThesisLibrary(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    finding_summary = models.CharField(max_length=255)  # single-line summary
    findings = models.ForeignKey(ThesisQueryResult, on_delete=models.CASCADE, related_name='libraries')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ThesisCompanyProfile(models.Model):
    company_id = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    founded = models.DateField(null=True, blank=True)
    locations = models.TextField(blank=True, null=True)
    formatted_locations = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slogan = models.CharField(max_length=255, blank=True, null=True)
    specialties = models.TextField(blank=True, null=True)
    revenue = models.CharField(max_length=100, blank=True, null=True)
    total_funding = models.CharField(max_length=100, blank=True, null=True)
    latest_funding_round = models.CharField(max_length=255, blank=True, null=True)
    funding = models.TextField(blank=True, null=True)
    investors = models.TextField(blank=True, null=True)
    stock_info = models.TextField(blank=True, null=True)
    similar_companies = models.TextField(blank=True, null=True)
    total_users = models.IntegerField(blank=True, null=True)
    average_time_on_site = models.FloatField(blank=True, null=True)
    organic_search = models.IntegerField(blank=True, null=True)
    organic_social_visits = models.IntegerField(blank=True, null=True)
    paid_search = models.IntegerField(blank=True, null=True)
    mail_visits = models.IntegerField(blank=True, null=True)
    traffic_rank = models.IntegerField(blank=True, null=True)
    referral_visits = models.IntegerField(blank=True, null=True)
    parent_website = models.URLField(blank=True, null=True)
    employees = models.TextField(blank=True, null=True)
    employee_count = models.CharField(max_length=50, blank=True, null=True)
    ceo_name = models.CharField(max_length=255)
    cfo_name = models.CharField(max_length=255)
    ceo_phone_number = models.CharField(max_length=50, blank=True, null=True)
    ceo_rating = models.CharField(max_length=50, blank=True, null=True)
    linkedin_company_profile = models.URLField(blank=True, null=True)
    crunchbase_url = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    image = models.ImageField(upload_to='company_images/', blank=True, null=True)
    updates = models.TextField(blank=True, null=True)
    affiliated = models.CharField(max_length=255, blank=True, null=True)
    get_directions_url = models.URLField(blank=True, null=True)
    parent_name = models.CharField(max_length=255, blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    sic_code = models.CharField(max_length=50, blank=True, null=True)
    name_sectors = models.CharField(max_length=255, blank=True, null=True)
    parent_industry_sectors = models.CharField(max_length=255, blank=True, null=True)
    paid_social_visits = models.IntegerField(blank=True, null=True)
    display_ad_visits = models.IntegerField(blank=True, null=True)
    average_bounce_rate = models.FloatField(blank=True, null=True)
    query_stats = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.company_id
