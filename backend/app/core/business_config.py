from typing import Dict, Any
from pydantic import BaseModel, EmailStr

class BusinessInfo(BaseModel):
    friendly_name: str
    legal_name: str
    email: EmailStr
    phone: str
    domain: str
    website: str
    niche: str
    business_type: str
    industry: str
    registration_type: str
    ein: str
    ghl_location_id: str = None

BUSINESS_CONFIGS: Dict[str, Dict[str, Any]] = {
    "airei": {
        "friendly_name": "The AI Real Estate Investor",
        "legal_name": "THE AI REAL ESTATE INVESTOR",
        "email": "info@theairealestateinvestor.com",
        "phone": "(405) 963-2596",
        "domain": "lc.theairealestateinvestor.com",
        "website": "https://theairealestateinvestor.com",
        "niche": "Marketing Consultant",
        "business_type": "Limited Liability Company",
        "industry": "Education",
        "registration_type": "USA: Employer Identification Number (EIN)",
        "ein": "99-1783082",
        "ghl_location_id": "4dgRQSZuc9AztQgaeErm"
    },
    "lhb": {
        "friendly_name": "Local House Buyers",
        "legal_name": "LOCAL HOUSE BUYERS LLC",
        "email": "mark@localhousebuyers.net",
        # Add other fields...
    }
} 