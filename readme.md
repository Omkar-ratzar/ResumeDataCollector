A simple project to perform

Data extraction,
Data parsing,
Data cleaning.

Upload resume, get output in dataframes.

DF cols:

Caandidate_Name, Candidate_mail, candidate_phone_number, candidate_address, Candidate_education

Hope so this turns into:

                ingestion pipeline (currently building)
                      |
        -----------------------------------
        |                                 |
        v                                 v
PostgreSQL (operational)          DuckDB + Parquet (analytics)
candidate profiles               intelligence marts
contact info                     clustering
identity graph refs              trend analysis
dedupe records                   skill analytics
                                 BI parsing
