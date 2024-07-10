# Subject Web Scraper
Did this because I thought it would be fun - not for any real application. The best solution for a subject database would be to just get access to the API that JCU has.

> [!TIP]
> - `main.py`: the Python app that did all the data gathering
> - `subjects.json`: the output
> - `subject_codes.txt`: list of *all* subject codes
> - `cse_subject_codes.txt`: list of all *College of Science and Engineering* subject codes

## Info

The data was scraped from [JCU Subject Search](https://apps.jcu.edu.au/subjectsearch/#/subjectlist/2024/ug)

scraped data: [`subjects.json`](/subjects.json)
I tried to keep the data comprehensive, whilst keeping it easy for myself. 
For example, I didn't really want to bother with all of the ORs and brackets in the prerequisite subject string, so the prerequisites_subjects list just contains each code that was mentioned in that string. In the example below, SC1102 and SC1109 aren't both required, but I just made it so that they're both chucked in the list because my monkey program reads a subject and just adds it.

Full Example:
```json
"SC2202": {
        "name": "Quantitative Methods in Science",
        "college": "College of Science and Engineering",
        "prerequisites_string": "SC1102 OR SC1109 OR ADMISSION TO BACHELOR OF BUSINESS AND ENVIRONMENTAL SCIENCE OR ADMISSION TO BACHELOR OF ENGINEERING (HONOURS)",
        "prerequisites_subjects": [
            "SC1109",
            "SC1102"
        ],
        "description": "An introduction to experimental and survey design and analysis. Topics include the principles of sampling design; hypothesis generation for experiments; collection of data; manipulations and interpretation of data; statistical methods used in science; and the use of data in scientific reports.",
        "learning_outcomes": "demonstrate sound knowledge of the basic principles that underpin sample selection, experimental design, data management, statistical theories, exploratory data analysis, and statistical analysis using basic linear modellingeffectively integrate and execute statistical theories and processes using R and RStudiocreate, retrieve, analyse, synthesise, and evaluate outputs produced from R and RStudio, including demonstrating rigorous workflow documentationintegrate statistical principles, methods, techniques and tools covered in this subject to plan and execute a statistical analysis",
        "availabilities": [
            {
                "availability": "Cairns Nguma-bada, Study Period 1, Internal",
                "census_date": "Thursday, 21 Mar 2024",
                "study_period_dates": "Monday, 19 Feb 2024 to Friday, 14 Jun 2024",
                "coordinator(s)": [
                    "Professor Yvette Everingham"
                ],
                "lecturer(s)": [
                    "DR Glenn Fulford",
                    "Professor Yvette Everingham"
                ],
                "workload_expectations": "The student workload for this 3 credit point subject is approximately 130 hours. 26 Hours - Lectures 26 Hours - Workshops 13 Hours - Online Seminarsassessment and  self-directed study"
            },
            {
                "availability": "Cairns Nguma-bada, Study Period 2, Internal",
                "census_date": "Thursday, 22 Aug 2024",
                "study_period_dates": "Monday, 22 Jul 2024 to Friday, 15 Nov 2024",
                "coordinator(s)": [
                    "Assoc. Professor Shaun Belward",
                    "Professor Yvette Everingham"
                ],
                "lecturer(s)": [
                    "MR Marc KOH",
                    "Professor Yvette Everingham"
                ],
                "workload_expectations": "The student workload for this 3 credit point subject is approximately 130 hours. 26 Hours - Lectures 26 Hours - Workshops 13 Hours - Online Seminarsassessment and  self-directed study"
            },
            {
                "availability": "JCU Singapore, Study Period 51, Internal",
                "census_date": "Thursday, 07 Mar 2024",
                "study_period_dates": "Thursday, 15 Feb 2024 to Friday, 26 Apr 2024",
                "coordinator(s)": [
                    "Professor Yvette Everingham"
                ],
                "lecturer(s)": [
                    "DR Jusak Jusak"
                ],
                "workload_expectations": "The student workload for this 3 credit point subject is approximately 130 hours. 26 Hours - Lectures 13 Hours - Workshops 13 Hours - Online Seminarsassessment and  self-directed study"
            },
            {
                "availability": "JCU Singapore, Trimester 3, Internal",
                "census_date": "Thursday, 10 Oct 2024",
                "study_period_dates": "Monday, 16 Sep 2024 to Saturday, 14 Dec 2024",
                "workload_expectations": "The student workload for this 3 credit point subject is approximately 130 hours. 26 Hours - Lectures 13 Hours - Workshops 13 Hours - Online Seminarsassessment and  self-directed study"
            },
            {
                "availability": "Townsville Bebegu Yumba, Study Period 1, Internal",
                "census_date": "Thursday, 21 Mar 2024",
                "study_period_dates": "Monday, 19 Feb 2024 to Friday, 14 Jun 2024",
                "coordinator(s)": [
                    "Professor Yvette Everingham"
                ],
                "lecturer(s)": [
                    "DR Glenn Fulford",
                    "Professor Yvette Everingham"
                ],
                "workload_expectations": "The student workload for this 3 credit point subject is approximately 130 hours. 26 Hours - Lectures 26 Hours - Workshops 13 Hours - Online Seminarsassessment and  self-directed study"
            },
            {
                "availability": "Townsville Bebegu Yumba, Study Period 2, Internal",
                "census_date": "Thursday, 22 Aug 2024",
                "study_period_dates": "Monday, 22 Jul 2024 to Friday, 15 Nov 2024",
                "coordinator(s)": [
                    "Assoc. Professor Shaun Belward"
                ],
                "lecturer(s)": [
                    "MR Marc KOH"
                ],
                "workload_expectations": "The student workload for this 3 credit point subject is approximately 130 hours. 26 Hours - Lectures 26 Hours - Workshops 13 Hours - Online Seminarsassessment and  self-directed study"
            }
        ],
        "assessment": [
            {
                "title": "Written > Examination (centrally administered) - (50%) - Individual",
                "percent_weighting": 50
            },
            {
                "title": "Written > Examination - In class - (10%) - Individual",
                "percent_weighting": 10
            },
            {
                "title": "Written > Test/Quiz 1 - (10%) - Individual",
                "percent_weighting": 10
            },
            {
                "title": "Written > Problem task - (30%) - Individual",
                "percent_weighting": 30
            }
        ]
    }
```