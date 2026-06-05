import ollama



# resume_text=extract_pdf(path)
# print(resume_text)
def auto(resume_text):

   content="""You are an information extraction system.

Extract entities from the resume and classify them into EXACTLY ONE of the following categories:

* PERSON
* COMPANY
* POSITION
* COLLEGE

IMPORTANT: Categories are mutually exclusive.

An entity MUST appear in only one category.

Classification Rules:

1. PERSON

* The resume owner's full name.
* Extract only the candidate's name.
* Do not extract names of recruiters, references, professors, teammates, or other people.

2. COLLEGE

* Universities, colleges, schools, institutes, academies, and any educational institution.
* Examples:

  * IIT Bombay
  * Stanford University
  * University of California Berkeley
  * Narayana College
  * Times Public School

STRICT RULE:
If an entity is an educational institution, place it ONLY in COLLEGE.
NEVER place educational institutions in COMPANY.

3. COMPANY

* Organizations where the candidate worked, interned, freelanced, or held a professional role.
* Examples:

  * Infosys
  * Google
  * Microsoft
  * TCS

STRICT RULES:

* Do NOT include colleges, universities, schools, institutes, or academies.
* Do NOT include project names.
* Do NOT include certifications.
* Do NOT include learning platforms.
* Do NOT include training platforms.
* Do NOT include websites.
* Do NOT include communities.
* Do NOT include clubs unless the candidate explicitly worked there.

4. POSITION

* Job titles, internship titles, research titles, leadership positions, and professional roles.
* Examples:

  * Software Engineer
  * Data Analyst Intern
  * Machine Learning Engineer
  * Product Manager
  * Research Assistant

Validation Rules:

Before producing the final answer:

1. Remove duplicates.
2. An entity may appear in only one category.
3. If an entity is a college/school/university/institute, remove it from COMPANY and keep it only in COLLEGE.
4. If uncertain whether an organization is a COMPANY or COLLEGE, classify it as COLLEGE if it is an educational institution.
5. Return only entities explicitly present in the resume.
6.The positions must contain generic roles like software developer, python engineer, AI engineer, etc. It must not contain something like 'Worked on x project','Collected this value'. It has to be a proper position (JOB ROLE). If the position exceeds 4 words then summarize it down to 4 words or less.

Output format:

{
"PERSON": [],
"COMPANY": [],
"POSITION": [],
"COLLEGE": []
}

Return ONLY valid JSON.

Do not include explanations.
Do not include markdown.
Do not include code fences.
Do not include any text before or after the JSON.
CRITICAL EXTRACTION RULES

Only extract text that appears verbatim in the resume.

Do NOT infer.

Do NOT normalize.

Do NOT summarize.

Do NOT generate likely job titles.

Do NOT generate likely employers.

Do NOT generate likely educational institutions.

Every extracted entity must be an exact substring of the resume text.

If a value does not appear literally in the resume, do not output it.
POSITION MUST be a professional job role.

Do NOT include:
- project names
- repository names
- products
- publications
- research papers
- software systems
"""
   response = ollama.chat(
      model="qwen2.5",
      messages=[{"role": "user", "content": content+resume_text}],
         options={
         "temperature": 0.1,
      }
   )

   return(response["message"]["content"])

