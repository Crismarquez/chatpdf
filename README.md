# ChatPDF

Chat whith your own pdf files :) 

Demo version of End-to-end service to analize pdf documents using LLMs.

This is a two stage solution, first, aplied robust ocr solution using *DocTR* to generate the dataset, and then fine tuning a LLM model using *LangChain* and *Open AI*

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
    pip install "python-doctr[torch]"
    pip install -r requirements.txt
    export PYTHONPATH="${PYTHONPATH}:${PWD}"
<prev>

4. setup keys

5. Estructure of dataser directory

    chatpdf

        +--data/
            +--projects/
                +--project_name/
                    +--documents/
                    +--text_files/

    OCR dataloaders will search pdf files in documents folder and then generate text files into text_files folder


## Run Demo
to run with fastapi

<prev>

    uvicorn ....

<prev>

to run some interaction funtions use main.py from CLI:

<prev>

    main.app ...
    
<prev>