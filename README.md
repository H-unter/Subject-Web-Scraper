# Subject Web Scraper
Did this because I thought it would be fun - not for any real application.

## Files
 - `main.py` the python app that did all the data gathering
 - `subjects.json` the output
 - `subject_codes.txt` list of *all* subject codes
 - `cse_subject_codes.txt` list of all *college of science and engineering* subject codes


## Info

The data was scraped from [JCU Subject Search](https://apps.jcu.edu.au/subjectsearch/#/subjectlist/2024/ug)

scraped data: [`subjects.json`](/subjects.json)
I tried to keep the data comprehensive, whilst keeping it easy for myself. 
For example, I didn't really want to bother with all of the ORs and brackets in the prerequisite subject string, so the prerequisites_subjects list just contains each code that was mentioned in that string. In the example below, SC1102 and SC1109 aren't both required, but I just made it so that they're both chucked in the list because my monkey program reads a subject and just adds it.

Also the assesment section could do with some work, as the title is pretty jank and often doens't capture all of the information it could. An example is Circuit theory where one assesment actually contains multiple: 
```json
"title": "On-course assessment: Consisting of two assignments worth 10% each and Practicals worth 5% - (25%) - Individual"
```
This would be pretty hard to fix as I doubt the formatting is that consistent

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
            "Cairns Nguma-bada, Study Period 1, Internal",
            "Cairns Nguma-bada, Study Period 2, Internal",
            "JCU Singapore, Study Period 51, Internal",
            "JCU Singapore, Trimester 3, Internal",
            "Townsville Bebegu Yumba, Study Period 1, Internal",
            "Townsville Bebegu Yumba, Study Period 2, Internal"
        ],
        "assessment": [
            {
                "title": "Written > Examination (centrally administered) - (50%) - Individual",
                "percent_weighting": 50
            },
            {
                "title": "Written > Test/Quiz 1 - (30%) - Individual",
                "percent_weighting": 30
            },
            {
                "title": "Written > Problem task - (20%) - Individual",
                "percent_weighting": 20
            }
        ]
    }
