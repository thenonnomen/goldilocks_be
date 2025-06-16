from django.db import models
from multiselectfield import MultiSelectField

THESIS_LIBRARY_TITLES = [
    # FMCG THEME VIEWS ###
    ("Profitable Mid-Market FMCG", "Scouting India's ₹50–500 Cr Performers"),
    ("Beauty in Momentum", "High-Growth Indian Personal Care Brands"),
    ("Offline Strongholds", "Food Brands Dominating General Trade"),
    # REAL ESTATE THEME VIEWS ###
    ("Roofing Material Leaders", "Scouting India's ₹50–500 Cr Roofing Manufacturers"),
    ("Tier 2 Roofing Expansion", "Roofing Brands Growing in Tier 2 & Tier 3 Cities"),
    ("Innovative Roofing Tech", "Solar, Modular & Smart Roofing Platforms"),
    # US v1 THEME VIEWS ###
    ("Distributed Infra Platforms", "US Platforms Aggregating Solar, Towers, Fiber, Water"),
    ("Storage & Trailer Rollups", "Consolidating U.S. Self-Storage & Trailer Leasing"),
    ("C&I Solar Expansion", "Commercial Solar Developers with Recurring Revenue"),
    ("High-Occupancy Storage", "Top Storage Rollups with 85%+ Utilization"),
]

# THESIS_LIBRARY_TITLES = [
#     ("Scouting India's ₹50–500 Cr Performers", "Profitable Mid-Market FMCG"),
#     ("High-Growth Indian Personal Care Brands", "Beauty in Momentum"),
#     ("Food Brands Dominating General Trade", "Offline Strongholds"),
# ]

class ThesisQueryResult(models.Model):
    """Model to store Thesis query results."""
    query = models.TextField()
    query_key = MultiSelectField(choices=THESIS_LIBRARY_TITLES, blank=True)
    query_id = models.CharField(max_length=255, unique=True)  # ID from ChromaDB
    created_at = models.DateTimeField(auto_now_add=True)
    query_stats = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Query {self.id}: {self.query[:50]}..."

class ThesisLibrary(models.Model):
    """Model to store Thesis Views."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    finding_summary = models.CharField(max_length=255)  # single-line summary
    findings = models.ForeignKey(ThesisQueryResult, on_delete=models.CASCADE, related_name='libraries')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ThesisCompanyProfile(models.Model):
    """Model to store company profile data for thesis analysis and tracking."""
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_id = models.CharField(max_length=255, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    founded = models.CharField(null=True, blank=True)
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
    total_users = models.TextField(blank=True, null=True)
    average_time_on_site = models.TextField(blank=True, null=True)
    organic_search = models.TextField(blank=True, null=True)
    organic_social_visits = models.TextField(blank=True, null=True)
    paid_search = models.TextField(blank=True, null=True)
    mail_visits = models.TextField(blank=True, null=True)
    traffic_rank = models.TextField(blank=True, null=True)
    referral_visits = models.TextField(blank=True, null=True)
    parent_website = models.URLField(blank=True, null=True)
    employees = models.TextField(blank=True, null=True)
    employee_count = models.CharField(max_length=50, blank=True, null=True)
    ceo_name = models.CharField(max_length=255, blank=True, null=True)
    cfo_name = models.CharField(max_length=255, blank=True, null=True)
    ceo_phone_number = models.CharField(max_length=50, blank=True, null=True)
    ceo_rating = models.CharField(max_length=50, blank=True, null=True)
    query_key = MultiSelectField(choices=THESIS_LIBRARY_TITLES, blank=True)
    is_public = models.BooleanField(default=False)
    priority = models.IntegerField(default=31)

    def __str__(self):
        return self.company_name or "Unknown Company"
  
    class Meta:
        ordering = ['priority']
