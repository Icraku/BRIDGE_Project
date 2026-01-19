#### Install the reuirements of this project ---> ***pip install -r requirements.txt***



### TO DO: FIX THE VALIDATION FOR EAC SCHEMA, CHECK THE VARIABLES AND THE STRUCTURE

### Project Pipeline:
1) Pdf ---> Png {converter.py} [Input 00]
2) Png ---> RedCAP or temporatry storage for image storage [Final Input]
3) RedCAP or temporary storage {main.py} ---> LLM (Qwen) [Output 00]
4) MedGemma ---> RedCAP in the RedCAP data format [Final output]



-----------------------------------------------------------------------------
### Step 1: Pdf to Png
Library used: **pdf2image import convert_from_path**
- Convert to Png then saved to a folder called ***converted_images***
- Each pdf has a unique filename as a differentiator ie ***[1700000005_NAR_15445_AAbCjIT.pdf](../../data/bridge/11-11-2025-12-35-52_files_list/1700000005_NAR_15445_AAbCjIT.pdf)***.

### Step 2: Upload to REdCAP/ Temporary storage/ Database
Library used: **python**
- Dynamically store the images
- 

### Step 3: Extraction
#### Step 3a: Extract using segmentation
- use segmeted screenshots of the whole file.
#### Step 3b: Extract as a whole
- need structured outputs and more of prompting


-----------------------------------------------------------------------------
#### To Do
1) Converted pdf to images --- store images or dynamically getting them from RedCAP instead of keeping them locally
3) Can run prompts with 0.442 overall accuracy --- Will improve on this during the preprocessing stage
4) To compare accuracy of true and predicted values in json style (key-value) format
5) 
