"""
Static reference data for each of the 41 diseases the model can predict.

IMPORTANT SAFETY NOTE:
- "medicine_categories" are general OTC/treatment *categories* only (e.g.
  "antihistamines", "rest and fluids") — NEVER specific drug names, doses,
  or prescription medications. This is intentional: the app is a triage/
  decision-support tool, not a prescriber.
- "specialist" maps to the medical specialty used to search nearby doctors.
- "emergency" flags conditions where the UI should show an urgent-care banner.
"""

DISEASE_INFO = {
    "(vertigo) Paroymsal  Positional Vertigo": {
        "specialist": "ENT specialist / Neurologist",
        "medicine_categories": ["Vestibular rehabilitation exercises", "Anti-vertigo medication (as prescribed)"],
        "summary": "A inner-ear balance disorder causing brief episodes of spinning sensation triggered by head movement.",
        "emergency": False,
    },
    "AIDS": {
        "specialist": "Infectious Disease specialist",
        "medicine_categories": ["Antiretroviral therapy (ART) — specialist-managed only"],
        "summary": "An immune system condition caused by HIV requiring ongoing specialist management.",
        "emergency": False,
    },
    "Acne": {
        "specialist": "Dermatologist",
        "medicine_categories": ["Topical retinoids", "Benzoyl peroxide", "Topical/oral antibiotics (as prescribed)"],
        "summary": "A common skin condition caused by clogged hair follicles, resulting in pimples and inflammation.",
        "emergency": False,
    },
    "Alcoholic hepatitis": {
        "specialist": "Hepatologist / Gastroenterologist",
        "medicine_categories": ["Complete alcohol cessation", "Nutritional support", "Specialist-managed treatment"],
        "summary": "Liver inflammation caused by heavy alcohol use, ranging from mild to life-threatening.",
        "emergency": True,
    },
    "Allergy": {
        "specialist": "Allergist / Immunologist",
        "medicine_categories": ["Antihistamines", "Decongestants", "Avoiding known triggers"],
        "summary": "An immune reaction to a substance (pollen, food, dust) causing sneezing, itching, or rash.",
        "emergency": False,
    },
    "Arthritis": {
        "specialist": "Rheumatologist",
        "medicine_categories": ["NSAIDs (anti-inflammatories)", "Physical therapy", "Joint-support supplements"],
        "summary": "Joint inflammation causing pain and stiffness, often worsening with age or overuse.",
        "emergency": False,
    },
    "Bronchial Asthma": {
        "specialist": "Pulmonologist",
        "medicine_categories": ["Bronchodilator inhalers", "Inhaled corticosteroids"],
        "summary": "A chronic condition where airways narrow and swell, causing wheezing and shortness of breath.",
        "emergency": False,
    },
    "Cervical spondylosis": {
        "specialist": "Orthopedist / Neurologist",
        "medicine_categories": ["Pain relievers", "Physical therapy", "Neck support"],
        "summary": "Age-related wear affecting spinal disks in the neck, causing pain and stiffness.",
        "emergency": False,
    },
    "Chicken pox": {
        "specialist": "General Physician / Dermatologist",
        "medicine_categories": ["Antihistamines for itching", "Fever reducers", "Calamine lotion"],
        "summary": "A contagious viral infection causing an itchy, blister-like rash and fever.",
        "emergency": False,
    },
    "Chronic cholestasis": {
        "specialist": "Hepatologist / Gastroenterologist",
        "medicine_categories": ["Specialist-managed treatment for bile flow issues"],
        "summary": "A condition where bile flow from the liver is reduced or blocked, causing itching and jaundice.",
        "emergency": False,
    },
    "Common Cold": {
        "specialist": "General Physician",
        "medicine_categories": ["Rest and fluids", "Decongestants", "Fever reducers"],
        "summary": "A mild viral upper-respiratory infection causing sneezing, congestion, and sore throat.",
        "emergency": False,
    },
    "Dengue": {
        "specialist": "General Physician / Infectious Disease specialist",
        "medicine_categories": ["Fluids and rest", "Fever reducers (avoid NSAIDs — consult a doctor)"],
        "summary": "A mosquito-borne viral infection causing high fever, severe headache, and joint pain.",
        "emergency": True,
    },
    "Diabetes": {
        "specialist": "Endocrinologist",
        "medicine_categories": ["Blood sugar management plan (specialist-guided)", "Dietary changes"],
        "summary": "A chronic condition affecting how the body regulates blood sugar.",
        "emergency": False,
    },
    "Dimorphic hemmorhoids(piles)": {
        "specialist": "Proctologist / General Surgeon",
        "medicine_categories": ["Topical creams", "Fiber supplements", "Sitz baths"],
        "summary": "Swollen veins in the lower rectum/anus causing discomfort and bleeding.",
        "emergency": False,
    },
    "Drug Reaction": {
        "specialist": "Allergist / General Physician",
        "medicine_categories": ["Discontinue suspected medication and consult a doctor immediately", "Antihistamines"],
        "summary": "An adverse reaction to a medication, ranging from mild rash to severe systemic reaction.",
        "emergency": True,
    },
    "Fungal infection": {
        "specialist": "Dermatologist",
        "medicine_categories": ["Antifungal creams", "Keeping the area clean and dry"],
        "summary": "A skin infection caused by fungi, common in warm, moist areas of the body.",
        "emergency": False,
    },
    "GERD": {
        "specialist": "Gastroenterologist",
        "medicine_categories": ["Antacids", "Proton pump inhibitors (as advised)", "Dietary changes"],
        "summary": "Gastroesophageal reflux disease — stomach acid frequently flows back into the esophagus.",
        "emergency": False,
    },
    "Gastroenteritis": {
        "specialist": "General Physician / Gastroenterologist",
        "medicine_categories": ["Oral rehydration solutions", "Rest"],
        "summary": "Inflammation of the stomach and intestines, usually from infection, causing diarrhea and vomiting.",
        "emergency": False,
    },
    "Heart attack": {
        "specialist": "Cardiologist — EMERGENCY",
        "medicine_categories": ["Call emergency services immediately — do not self-treat"],
        "summary": "A blockage of blood flow to the heart muscle. This is a medical emergency.",
        "emergency": True,
    },
    "Hepatitis B": {
        "specialist": "Hepatologist / Infectious Disease specialist",
        "medicine_categories": ["Antiviral therapy (specialist-managed)"],
        "summary": "A viral infection that attacks the liver and can become chronic.",
        "emergency": False,
    },
    "Hepatitis C": {
        "specialist": "Hepatologist / Infectious Disease specialist",
        "medicine_categories": ["Antiviral therapy (specialist-managed)"],
        "summary": "A viral infection causing liver inflammation, often spread through blood contact.",
        "emergency": False,
    },
    "Hepatitis D": {
        "specialist": "Hepatologist",
        "medicine_categories": ["Specialist-managed treatment"],
        "summary": "A liver infection that only occurs in people already infected with Hepatitis B.",
        "emergency": False,
    },
    "Hepatitis E": {
        "specialist": "Hepatologist / Gastroenterologist",
        "medicine_categories": ["Rest and fluids", "Specialist follow-up"],
        "summary": "A liver infection usually spread through contaminated water, generally self-limiting.",
        "emergency": False,
    },
    "Hypertension": {
        "specialist": "Cardiologist",
        "medicine_categories": ["Blood pressure management plan (specialist-guided)", "Lifestyle changes"],
        "summary": "Persistently high blood pressure that increases risk of heart disease and stroke.",
        "emergency": False,
    },
    "Hyperthyroidism": {
        "specialist": "Endocrinologist",
        "medicine_categories": ["Thyroid-regulating treatment (specialist-managed)"],
        "summary": "An overactive thyroid gland producing excess hormone, speeding up metabolism.",
        "emergency": False,
    },
    "Hypoglycemia": {
        "specialist": "Endocrinologist",
        "medicine_categories": ["Fast-acting sugar/glucose if mild", "Seek care if severe or recurrent"],
        "summary": "Abnormally low blood sugar, which can cause shakiness, confusion, or fainting.",
        "emergency": False,
    },
    "Hypothyroidism": {
        "specialist": "Endocrinologist",
        "medicine_categories": ["Thyroid hormone replacement (specialist-managed)"],
        "summary": "An underactive thyroid gland producing insufficient hormone, slowing metabolism.",
        "emergency": False,
    },
    "Impetigo": {
        "specialist": "Dermatologist",
        "medicine_categories": ["Topical/oral antibiotics (as prescribed)", "Keeping area clean"],
        "summary": "A contagious bacterial skin infection common in children, causing sores and blisters.",
        "emergency": False,
    },
    "Jaundice": {
        "specialist": "Hepatologist / Gastroenterologist",
        "medicine_categories": ["Treat underlying cause (specialist evaluation needed)"],
        "summary": "Yellowing of skin/eyes caused by elevated bilirubin, often signaling a liver issue.",
        "emergency": False,
    },
    "Malaria": {
        "specialist": "Infectious Disease specialist",
        "medicine_categories": ["Antimalarial medication (specialist-prescribed)"],
        "summary": "A mosquito-borne parasitic infection causing fever, chills, and flu-like illness.",
        "emergency": True,
    },
    "Migraine": {
        "specialist": "Neurologist",
        "medicine_categories": ["Pain relievers", "Rest in a dark, quiet room", "Trigger avoidance"],
        "summary": "A neurological condition causing intense, often one-sided headaches, sometimes with aura.",
        "emergency": False,
    },
    "Osteoarthristis": {
        "specialist": "Orthopedist / Rheumatologist",
        "medicine_categories": ["Pain relievers", "Physical therapy", "Weight management"],
        "summary": "Degeneration of joint cartilage over time, causing pain and reduced mobility.",
        "emergency": False,
    },
    "Paralysis (brain hemorrhage)": {
        "specialist": "Neurologist — EMERGENCY",
        "medicine_categories": ["Call emergency services immediately — do not self-treat"],
        "summary": "Bleeding within the brain, often causing sudden weakness or paralysis. Medical emergency.",
        "emergency": True,
    },
    "Peptic ulcer diseae": {
        "specialist": "Gastroenterologist",
        "medicine_categories": ["Antacids", "Proton pump inhibitors (as advised)"],
        "summary": "Open sores in the stomach lining or upper intestine, often causing burning pain.",
        "emergency": False,
    },
    "Pneumonia": {
        "specialist": "Pulmonologist",
        "medicine_categories": ["Antibiotics if bacterial (as prescribed)", "Rest and fluids"],
        "summary": "An infection that inflames air sacs in one or both lungs, causing cough and fever.",
        "emergency": True,
    },
    "Psoriasis": {
        "specialist": "Dermatologist",
        "medicine_categories": ["Topical corticosteroids", "Moisturizers", "Phototherapy (specialist-guided)"],
        "summary": "A chronic autoimmune condition causing rapid skin cell buildup and scaly patches.",
        "emergency": False,
    },
    "Tuberculosis": {
        "specialist": "Pulmonologist / Infectious Disease specialist",
        "medicine_categories": ["Long-course antibiotic therapy (specialist-managed)"],
        "summary": "A bacterial infection primarily affecting the lungs, requiring extended specialist treatment.",
        "emergency": False,
    },
    "Typhoid": {
        "specialist": "General Physician / Infectious Disease specialist",
        "medicine_categories": ["Antibiotics (as prescribed)", "Fluids and rest"],
        "summary": "A bacterial infection spread through contaminated food/water, causing prolonged fever.",
        "emergency": False,
    },
    "Urinary tract infection": {
        "specialist": "Urologist / General Physician",
        "medicine_categories": ["Antibiotics (as prescribed)", "Increased fluid intake"],
        "summary": "A bacterial infection anywhere in the urinary system, causing pain and frequent urination.",
        "emergency": False,
    },
    "Varicose veins": {
        "specialist": "Vascular Surgeon",
        "medicine_categories": ["Compression stockings", "Leg elevation", "Lifestyle changes"],
        "summary": "Enlarged, twisted veins usually in the legs, caused by weakened vein valves.",
        "emergency": False,
    },
    "hepatitis A": {
        "specialist": "Gastroenterologist / General Physician",
        "medicine_categories": ["Rest and fluids", "Typically resolves without specific treatment"],
        "summary": "A contagious liver infection spread through contaminated food or water.",
        "emergency": False,
    },
}

DEFAULT_INFO = {
    "specialist": "General Physician",
    "medicine_categories": ["Consult a doctor for personalized guidance"],
    "summary": "A condition matching your reported symptoms — please consult a doctor for a full evaluation.",
    "emergency": False,
}


def get_disease_info(disease_name: str) -> dict:
    return DISEASE_INFO.get(disease_name, DEFAULT_INFO)
