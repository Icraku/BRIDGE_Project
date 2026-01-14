#### Create a requirements.txt file ---> ***pip freeze > requirements.txt***

#### To TEST THE SCHEMAS: python -m Tests.test_schema


### TO DO: FIX THE VALIDATION FOR EAC SCHEMA, CHECK THE VARIABLES AND THE STRUCTURE

### Project Pipeline:
1) Pdf ---> Png {converter.py} [Input 00]
2) Png ---> RedCAP for image storage [Final Input]
3) RedCAP {main.py} ---> MedGemma [Output 00]
4) MedGemma ---> RedCAP [Final output]



-----------------------------------------------------------------------------
### Step 1: Pdf to Png
Library used: **pdf2image import convert_from_path**
- Convert to Png then saved to a folder called ***converted_images***
- Each pdf has a unique filename ie ***[1700000005_NAR_15445_AAbCjIT.pdf](../../data/bridge/11-11-2025-12-35-52_files_list/1700000005_NAR_15445_AAbCjIT.pdf)*** therefore we use the filename that is ***...1700000005...*** to differentiate the file images later on.

### Step 2: Upload to REdCAP
Library used: **python**
- Dynamically store the images in the folder to RedCAP
- 

### Step 3: Extraction
#### Step 3a: Extract using segmentation
- use small screenshots of the whole file. (will produce too many files to work with, how to map the files to the original pdf??)
#### Step 3a: Extract as a whole
- need structured outputs and more of prompting


-----------------------------------------------------------------------------
#### Month 4 Update
1) Model that is currently being used is QWen instead of MedGemma
2) Converted pdf to images --- Awaiting how to store images or dynamically getting them from RedCAP
3) Can run prompts with 0.442 overall accuracy --- Will improve on this during the preprocessing stage
4) To compare accuracy of true and predicted values in json style (key-value) format
5) 