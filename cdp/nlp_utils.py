import spacy
import re

nlp = spacy.load("en_core_web_sm")

# Define custom mappings between terms and model fields
FIELD_MAP = {
    # PrimaryCompanyInfo Model
    "name": "company_name",
    "company": "company_name",
    "company name": "company_name",
    "domain": "company_domain",
    "linkedin": "linkedin_company_profile",
    "country": "country_code",
    "location": "locations",
    "size": "company_size",
    "type": "organization_type",
    "industry": "industries",
    "founded": "founded",
    "headquarters": "headquarters",
    "logo": "logo",
    "sectors": "name_sectors",
    "parent_sector": "parent_industry_sectors",

    # SecondaryCompanyInfo Model
    "employees": "secondary_info__employee_count",
    "employee_count": "secondary_info__employee_count",
    "employee count": "secondary_info__employee_count",
    "about": "secondary_info__about",
    "specialties": "secondary_info__specialties",
    "slogan": "secondary_info__slogan",
    "investors": "secondary_info__investors",
    "parent_name": "secondary_info__parent_name",

    # FinancialInfo Model
    "revenue": "financial_info__revenue",
    "funding": "financial_info__total_funding",
    "funding_round": "financial_info__latest_funding_round",
    "ceo_first_name": "financial_info__first_name_ceo",
    "ceo_last_name": "financial_info__last_name_ceo",
    "ceo_rating": "financial_info__ceo_rating",

    # BusinessTracker Model
    "traffic_rank": "business_tracker__traffic_rank",
    "total_visits": "business_tracker__total_visits",
    "linkedin_followers": "business_tracker__linkedin_followers",
}

COMPARATORS = {
    "more than": "__gt",
    "greater than": "__gt",
    "above": "__gt",
    "over": "__gt",
    "less than": "__lt",
    "below": "__lt",
    "under": "__lt",
    "equal to": "",
    "exactly": "",
    "after": "__gt",
    "before": "__lt",
    "get": "",
}

def parse_comparison(text):
    for phrase, op in COMPARATORS.items():
        if phrase in text:
            return op, text.split(phrase)[-1].strip()
    return "", text.strip()

# def extract_filters(prompt: str):
#     doc = nlp(prompt)
#     filters = {}
#     limit = 10  

#     top_match = re.search(r'top (\d+)', prompt)
#     if top_match:
#         limit = int(top_match.group(1))

#     for token in doc:
#         token_text = token.text.lower()
#         for keyword, field_path in FIELD_MAP.items():
#             if keyword in token_text:
#                 surrounding = " ".join([t.text.lower() for t in doc[max(0, token.i-3):token.i+4]])
#                 op, val = parse_comparison(surrounding)

#                 try:
#                     if "million" in val:
#                         num = float(val.replace("million", "").strip()) * 1_000_000
#                     elif "billion" in val:
#                         num = float(val.replace("billion", "").strip()) * 1_000_000_000
#                     else:
#                         num = float(re.sub(r"[^\d.]", "", val))
#                     filters[field_path + op] = num
#                 except:
#                     import pdb;pdb.set_trace()
#                     filters[field_path + "__icontains"] = val.strip()

#     return filters, limit

def extract_filters(prompt: str):
    doc = nlp(prompt)
    filters = {}
    limit = 10  # Default

    # --- Handle "top N" ---
    top_match = re.search(r'top\s+(\d+)', prompt.lower())
    if top_match:
        limit = int(top_match.group(1))

    matched_fields = set()

    # --- Rule-based field matching ---
    for token in doc:
        token_text = token.text.lower()
        for keyword, field_path in FIELD_MAP.items():
            if keyword in token_text and field_path not in matched_fields:
                surrounding = " ".join([t.text.lower() for t in doc[max(0, token.i-3):token.i+4]])
                op, val = parse_comparison(surrounding)

                try:
                    if "million" in val:
                        num = float(val.replace("million", "").strip()) * 1_000_000
                    elif "billion" in val:
                        num = float(val.replace("billion", "").strip()) * 1_000_000_000
                    else:
                        num = float(re.sub(r"[^\d.]", "", val))
                    filters[field_path + op] = num
                except:
                    filters[field_path + "__icontains"] = val.strip()

                matched_fields.add(field_path)

    # ✅ STEP 1: Regex for "named", "called", or "name" followed by actual name
    name_regex = re.search(
        r"(?:named|called|name(?:d)?(?: is| is)?)\s+([a-zA-Z0-9&\-.]{2,50})",
        prompt, re.IGNORECASE
    )
    if name_regex:
        filters["company_name__icontains"] = name_regex.group(1).strip()
    else:
        # ✅ STEP 2: NER fallback (only short, clean names)
        for ent in doc.ents:
            if (
                ent.label_ in ["ORG", "GPE", "PERSON"]
                and "company_name__icontains" not in filters
            ):
                candidate = ent.text.strip()
                if len(candidate.split()) > 3:
                    continue  # skip long NER spans
                if "find the" in candidate.lower() or "company" in candidate.lower():
                    continue  # skip junk matches
                filters["company_name__icontains"] = candidate
                break
    # import pdb; pdb.set_trace()
    return filters, limit
