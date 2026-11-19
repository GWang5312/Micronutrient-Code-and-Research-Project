# Micronutrient Code and Research Project
An analysis between the micronutrient density of plant/animal based foods using Python

# Project Overview
This is an independent high school research project crossing over my passions of data science and health/nutrition. While exploring nutriiton, I've seen many debates and comparisons on whether plant or animal foods are superior, and one of the main topics always mentioned is micronutrient density. Combined with my belief that micronutrients are severely underemphasized in the modern nutrition space, I set out to explore whether one side was truly favored in this debate. This research project compares how micronutrient dense both categories are using both 100g and 100cal to account for different contexts of people.

# Methodology
- 40 foods were selected from both plant and animals\
- 22 micronutrients were analyzed\
- Extracted data from USDA FoodData Central's SR Legacy\
- Compared with DV Score, measuring how much a food contributed to a person's daily micronutrient requirements

NOTE: This project was primarily intended to be a data science and programming project to show my skills in analyzing datasets with Python and Matplotlib. Therefore, some of the methodology definitely took some shortcuts that shifted the emphasis of the project towards data processing and analysis, which could be refined if this were to be done again.

# Files
**Python Code**\
Main Code - fooddataproject.py\
Code with Data Lists - fdplists.py\
NOTE: Both need to be downloaded, as well as downloading SR Legacy at https://fdc.nal.usda.gov/download-datasets

**Data Sets**\
Plant (100g) - gplant.csv\
Animal (100g) - ganimal.csv\
Plant (100cal) - calplant.csv\
Animal (100cal) - calanimal.csv\
NOTE: A Google Sheets version that's cleaner can be found at https://docs.google.com/spreadsheets/d/1XkVJxp2-eBz7ruPb3HISYa2xu3Pqu9DGKn58niw-uho/edit?usp=sharing

**Research Paper**\
Found under fdppaper.pdf\
NOTE: A better version with links can be found at https://docs.google.com/document/d/1B3NNyyb9D7lK_fVPTJ63Us4PxYJAdD3LskAySpK72fk/edit?usp=sharing
