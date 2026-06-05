A simple project to perform

Data extraction,
Data parsing,
Data cleaning.

Upload resume, get output in dataframes.

DF cols:

Caandidate_Name, Candidate_mail, candidate_phone_number, candidate_address, Candidate_education

#STOPPING ATP
# Resume Data Extractor

A hybrid resume parsing system using:

- PDF extraction
- OCR support
- Regex-based metadata extraction
- Custom SpaCy NER model

## Dataset

- 96 manually collected resumes
- 79 training samples
- 7 validation samples
- 10 test samples

### Named Entities

- PERSON
- COMPANY
- COLLEGE
- POSITION

## Model

Framework: SpaCy 3.8

Pipeline:

tok2vec -> ner

## Evaluation Results

| Entity | Precision | Recall | F1 |
|----------|----------|----------|----------|
| PERSON | 83.33 | 41.67 | 55.56 |
| COMPANY | 20.00 | 2.78 | 4.88 |
| COLLEGE | 46.67 | 33.33 | 38.89 |
| POSITION | 63.64 | 57.14 | 60.22 |

### Overall

| Metric | Score |
|----------|----------|
| Precision | 58.57 |
| Recall | 34.75 |
| F1 Score | 43.62 |

## Challenges

- Small dataset (96 resumes)
- High variability in resume layouts
- Limited company-name coverage
- Distinguishing colleges from companies
- OCR and PDF extraction inconsistencies

## Future Improvements

- Larger annotated dataset
- Transformer-based NER
- Resume section classification
- Organization disambiguation (Company vs College)
