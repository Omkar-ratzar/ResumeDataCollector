from extract_pdf import extract_pdf
import spacy
import re


text=(extract_pdf("E:\Coding\ResumeDataExtractor\Omkar_swami_res.pdf"))

print(text)
# python -m spacy download en_core_web_trf
nlp = spacy.load("en_core_web_trf")

doc = nlp(text)

for ent in doc.ents:
    print(ent.text, ent.label_)

email = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text)
phone = re.findall(r'(?:\+?\d{1,3}[\s-]?)?(?:\d[\s-]?){10,}', text)
print(email[0],phone[0])




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


'''now we have:
Person name
Phone number
Email



'''
