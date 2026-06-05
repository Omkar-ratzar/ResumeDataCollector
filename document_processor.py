from Extraction.extract_pdf import extract_pdf
from Extraction.extract_meta import extract_pdf_metadata
from data_loader import AUTOMATON
import spacy
import re
# import ahocorasick
import pandas as pd
df1 = pd.read_csv("Data/country_codes.csv")
import phonenumbers
from phonenumbers import geocoder, carrier, timezone, number_type


path="E:\\Coding\\ResumeDataExtractor\\Resumes\\rajan_swami_resume.pdf"
resume_text=(extract_pdf(path))

print(resume_text)
# python -m spacy download en_core_web_trf
nlp = spacy.load("en_core_web_trf")

doc = nlp(resume_text)
print()
print()
print(doc)
print()
print()
# for ent in doc.ents:
#     if(ent.label_=="PERSON"):
#         print(ent.text)


def email_phone_re(resume_text):
    email = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', resume_text)
    phone = re.findall(r'\+?\d[\d\s-]{8,14}\d', resume_text)

    return (email if email else None,phone if phone else None)

def country_from_phone(phones):


    countries = []

    for phone in phones:
        phone = re.sub(r"[^\d]", "", str(phone))

        matches = []

        for _, row in df1.iterrows():
            code = re.sub(r"[^\d]", "", str(row["DIALINGCODE"]))

            if phone.startswith(code):
                matches.append((len(code), row["COUNTRY"]))

        if matches:
            matches.sort(reverse=True)
            countries.append(matches[0][1])
        else:
            countries.append("Unknown")

    return countries

SECTION_HEADERS = [
    "Education",
    "Experience",
    "Skills",
    "Projects",
    "Certifications",
    "Work history",
    "Contact",
    "Achievements"
]

def normalize_text(resume_text):
    resume_text = resume_text.lower()
    resume_text = re.sub(r"\s+", " ", resume_text)
    return resume_text



def extract_skills(resume_text):


    resume_text=normalize_text(resume_text)
    found = set()
    for end_idx, skill in AUTOMATON.iter(resume_text):
        start_idx = end_idx - len(skill) + 1
        before = resume_text[start_idx - 1] if start_idx > 0 else " "
        after = resume_text[end_idx + 1] if end_idx + 1 < len(resume_text) else " "
        if not before.isalnum() and not after.isalnum():
            found.add(skill)

    return sorted(found)



def extract_phone_metadata(text):
    candidates = []

    for match in phonenumbers.PhoneNumberMatcher(text, None):
        num = match.number

        if not phonenumbers.is_valid_number(num):
            continue

        num_type = number_type(num)

        candidates.append({
            "raw_match": match.raw_string,

            "e164": phonenumbers.format_number(
                num,
                phonenumbers.PhoneNumberFormat.E164
            ),

            "international": phonenumbers.format_number(
                num,
                phonenumbers.PhoneNumberFormat.INTERNATIONAL
            ),

            "national": phonenumbers.format_number(
                num,
                phonenumbers.PhoneNumberFormat.NATIONAL
            ),

            "rfc3966": phonenumbers.format_number(
                num,
                phonenumbers.PhoneNumberFormat.RFC3966
            ),
            "country_code": num.country_code,
            "national_number": num.national_number,
            "extension": num.extension if num.extension else None,
            "region_code": phonenumbers.region_code_for_number(num),
            "location": geocoder.description_for_number(num, "en"),
            "carrier": carrier.name_for_number(num, "en"),
            "timezones": timezone.time_zones_for_number(num),
            "is_valid": phonenumbers.is_valid_number(num),
            "is_possible": phonenumbers.is_possible_number(num),
            "is_international": match.raw_string.strip().startswith("+"),
            "number_type": str(num_type)
        })

    return candidates


def extract_metadata(path):
    return extract_pdf_metadata(path)

email_phone=email_phone_re(resume_text)

print(email_phone)
print(extract_skills(resume_text))
print(country_from_phone(["+91 983457626"]))
print(extract_phone_metadata(text=resume_text))
print(extract_metadata(path))

