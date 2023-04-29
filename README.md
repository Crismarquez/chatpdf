# ChatPDF

Demo version of End-to-end service to analize pdf documents using LLMs.

This is a two stage solution, first, aplied robust ocr solution using *DocTR* to generate the dataset, and then fine tuning a LLM model using *LangChain* and *Open AI*

## Getting Started
1. Clone repo

2. create and activate virtual enviroment

<prev>

    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
    export PYTHONPATH="${PYTHONPATH}:${PWD}"
    
<prev>

3. setup keys

4. run with fastapi

<prev>

    uvicorn ....
<prev>

