from typing import Optional
from pathlib import Path
import typer
from doctr.io import DocumentFile
import gdown

from src.engineering import OCREngineering, LLMEngineering
from src.recognition import Recognition
from src.data import DatasetManager
from config.config import DATA_DIR, DEFAULT_FILES, PROEJECTS_DIR, logger

app = typer.Typer()
ocr_recognition = Recognition(det_arch="db_resnet50", reco_arch="crnn_vgg16_bn")

@app.command()
def showocr(pdf_file: Optional[str]=None):
    if pdf_file is None:
        logger.info("Downloading sample pdf file")
        url = DEFAULT_FILES["ocr_show"]
        gdown.download_folder(url, output = str(DATA_DIR / "ocr_show"), quiet=False)
        pdf_file = "Ownership_DeedRecording-1.pdf"

        pdf_dir = Path(DATA_DIR, "ocr_show" , pdf_file)

    else:
        pdf_dir = DATA_DIR / pdf_file

    if not pdf_dir.exists():
        logger.error(f"File {pdf_dir} does not exist")
        raise FileNotFoundError(f"File {pdf_dir} does not exist")

    if pdf_dir.is_dir():
        pdf_files = [f for f in pdf_dir.iterdir() if f.suffix == ".pdf"]
        for pdf_file in pdf_files:
            doc = DocumentFile.from_pdf(pdf_file)
            results = ocr_recognition._recognize(doc)
            results.show(doc)
    else:
        doc = DocumentFile.from_pdf(pdf_dir)
        results = ocr_recognition._recognize(doc)
        results.show(doc)

@app.command()
def ocrengineering(project_name: Optional[str] = None):
    if project_name is None:
        logger.info("Project name not provided, using default project name 'anual_report'")
        logger.info("Downloading sample pdf file")
        url = DEFAULT_FILES["anual_report"]
        gdown.download_folder(url, output = str(PROEJECTS_DIR/"anual_report"), quiet=False)
        project_name = "anual_report"

    data_manager = DatasetManager(project_name=project_name)

    ocr_engineering = OCREngineering(
        recognition=ocr_recognition, dataset_manager=data_manager
    )

    ocr_engineering.process()

    logger.info("Done!")

@app.command()
def pdftotext(pdf_file: Optional[str]):
    pdf_dir = DATA_DIR / pdf_file

    if not pdf_dir.exists():
        logger.error(f"File {pdf_dir} does not exist")
        raise FileNotFoundError(f"File {pdf_dir} does not exist")

    if pdf_dir.is_dir():
        pdf_files = [f for f in pdf_dir.iterdir() if f.suffix == ".pdf"]
        for pdf_file in pdf_files:
            doc = DocumentFile.from_pdf(pdf_file)
            results = ocr_recognition.recognize(doc)
            json_result = results.export()

            lines = []
            for block in json_result["pages"][0]["blocks"]:
                for line in block["lines"]:
                    words_line = []
                    for words in line["words"]:
                        words_line.append(words["value"])
                    lines.append(" ".join(words_line))
        # save .txt file
        for pdf_file in pdf_files:
            with open(pdf_file.with_suffix(".txt"), "w") as f:
                f.write("\n".join(lines))

    else:
        doc = DocumentFile.from_pdf(pdf_dir)
        results = ocr_recognition.recognize(doc)
        json_result = results.export()

        lines = []
        for block in json_result["pages"][0]["blocks"]:
            for line in block["lines"]:
                words_line = []
                for words in line["words"]:
                    words_line.append(words["value"])
                lines.append(" ".join(words_line))

    # save .txt file

@app.command()
def chatpdf(project_name: str, query: str):
    data_manager = DatasetManager(project_name=project_name)

    llm_engineering = LLMEngineering(
        dataset_manager=data_manager    
    )

    response = llm_engineering.predict(query, response_mode="compact")

    return response


if __name__ == "__main__":
    app()
