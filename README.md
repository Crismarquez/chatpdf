# ChatPDF

![Fastapi](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)

Chat whith your own pdf files :) 

Demo version of End-to-end service to analize pdf documents using LLMs.

This is a two stage solution, first, aplied robust ocr engineering using *DocTR* to generate the dataset, and then fine tuning a LLM model using *LangChain* and *Open AI*
Finally expose chat with FastAPI

**OCR Engineering**

![image](https://github.com/crismarquez/chatpdf/blob/main/assets/ocr_show.png?raw=true)

**Chat using FastAPI**

![image](https://github.com/crismarquez/chatpdf/blob/main/assets/post.png?raw=true)
![image](https://github.com/crismarquez/chatpdf/blob/main/assets/response.png?raw=true)


## System requirements
- Ubuntu 20
- Python >=3.10

## Getting Started
1. Clone repo

2. create and activate virtual enviroment

<prev>

    python3 -m venv .venv
    source .venv/bin/activate

<prev>

3. Install dependences

<prev>

    python3 -m pip install --upgrade pip setuptools wheel
    pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117
    pip install "python-doctr[torch]"
    pip install langchain
    pip install -r requirements.txt
    export PYTHONPATH="${PYTHONPATH}:${PWD}"
<prev>

4. setup keys for open ai, into .env file:
    OPENAI_API_KEY="your-open-ai-key"


## Run Demo 

## Run Demo OCR - Engineering
<prev>

    python3 main.py showocr

<prev>

OCR engineering in default project (Amazon report - 2022)

<prev>

    python3 src/main.py ocrengineering

<prev>

Run FasAPI for chat enpoind
<prev>

    uvicorn app.main:app --port 5000

<prev>


## Use with your own pdf file

Put manualy your pdf files into this structure:

    chatpdf

        +--data/
            +--projects/
                +--project_name/
                    +--documents/
                        1-file.pdf
                        ....
                        n-file.pdf
                    +--text_files/

    OCR dataloaders will search pdf files in documents folder and then generate text files into text_files folder