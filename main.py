from typing import Optional
import typer
from doctr.io import DocumentFile

from src.engineering import OCREngineering
from src.recognition import Recognition
from src.data import DatasetManager
from config.config import DATA_DIR, logger

app = typer.Typer()
ocr_recognition = Recognition(det_arch="db_resnet50", reco_arch="crnn_vgg16_bn")

@app.command()
def showocr(pdf_file: Optional[str]):
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
def ocrengineering(project_name: Optional[str] = "anual_reports"):
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


if __name__ == "__main__":
    app()
