from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from multiselectfield import MultiSelectField
# Create your models here.

class GoldilocksCDP(models.Model):
    """Model to store core company data for GoldilocksCDP."""
    name = models.CharField(max_length=255)
    headquarters = models.CharField(max_length=255, blank=True, null=True)
    revenue = models.CharField(max_length=255, blank=True, null=True)
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

FIDELITY_CHOICES = (
    ("High", "High"),
    ("Medium", "Medium"),
    ("Low", "Low")
)

class PrimaryCompanyInfo(models.Model):
    """Model to store primary company information."""
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
    """Model to store secondary company information."""
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
    """Model to store financial information for a company."""
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
    """Model to store business tracker information for a company."""
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

class UserSearchPrompts(models.Model):
    """Model to store user search prompts."""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    prompt = models.TextField(blank=True, null=True)
    # change to "query_filters"
    query_filters = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    query_key = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']


User = get_user_model()

class UserHistory(models.Model):
    """Model to store user request and activity history."""
    method = models.CharField(max_length=10)
    path = models.TextField()
    headers = models.TextField()
    body = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} {self.path} at {self.timestamp}"

QUERY_KEY_CHOICES = [
    ("FMCG Financial Filter", "Show Indian FMCG companies with revenue between ₹50 Cr and ₹500 Cr and EBITDA margins above 15%"),
    ("Personal Care Growth", "Identify Indian personal care brands with YoY revenue growth over 25% for the last 3 years"),
    ("Food Channel Mix", "Find Indian mid-sized food brands with >60% revenue from general trade and low digital penetration"),
    ("Natural Regulatory Brands", "Identify Indian Ayurvedic or natural ingredient-based brands with regulatory certifications"),
    ("South Regional Focus", "Identify Indian regional brands with strong share in South India and minimal North presence"),
    ("High Consumer Sentiment", "Identify Indian brands with high consumer sentiment (avg. review >4.2 across marketplaces)"),
    ("Flagship Product Rating", "Find Indian firms whose flagship product has a 4.5+ rating on Amazon/Flipkart"),
    ("Bootstrapped Growth Longevity", "Find bootstrapped Indian companies with growing topline and 5+ years of operations"),
    ("PE Exit Timing", "Identify PE-backed firms in India near the end of a 5-year holding cycle"),
    ("Tier 2 Expansion", "Find Indian brands expanding from Tier 2 to Tier 1 cities in the last 18 months"),
    ("Tier2 Personal Growth", "Among these, identify personal care brands with a high Tier 2 city presence and consistent YoY growth over the last 3 years."),
    ("Ayurvedic Skincare Niche", "From these, highlight Ayurvedic or plant-based skincare brands targeting women aged 25–40, with flagship products rated 4.5+ on Amazon or Nykaa.")
]

class WatchlistData(models.Model):
    """Model to store company watchlist data with associated query keys."""
    company_name = models.CharField(max_length=455)
    headquarters = models.CharField(max_length=455, blank=True, null=True)
    company_domain = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    employees = models.CharField(max_length=100, blank=True, null=True)
    revenue = models.CharField(max_length=100, blank=True, null=True)
    query_key = MultiSelectField(choices=QUERY_KEY_CHOICES, blank=True)
    is_public = models.BooleanField(default=False)
    priority = models.IntegerField(default=31)

    def __str__(self):
        return self.company_name

class WatchlistInsights(models.Model):
    """Model to store insights for each watchlist entry and query key."""
    query_key = models.CharField(max_length=455, choices=QUERY_KEY_CHOICES)
    insights = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Insights for {self.watchlist_data.company_name} on {self.query_key}"
