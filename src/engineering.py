from doctr.io import DocumentFile
from src.recognition import Recognition
from src.data import DatasetManager
from config.config import DATA_DIR, logger


class OCREngineering:
    def __init__(self, recognition: Recognition, dataset_manager: DatasetManager):
        self.recognition = recognition
        self.dataset_manager = dataset_manager

    def process(self):
        pdf_files = self.dataset_manager.get_pdf_files()
        if len(pdf_files) == 0:
            logger.error(f"No pdf files found in documents folder")
            return {"msg": f"No pdf files found in documents folder"}

        logger.info(f"Found {len(pdf_files)} pdf files")
        all_lines = []
        for pdf_dir in pdf_files:
            doc = DocumentFile.from_pdf(pdf_dir)
            json_result = self.recognition.recognize(doc)
            lines = self.process_doc_result(json_result)
            all_lines.extend(lines)

        self.dataset_manager.save_text(all_lines)

        return {"msg": f"success processed {len(pdf_files)} pdf files"}

    def process_doc_result(self, json_result):
        lines = []
        for page in json_result["pages"]:
            for block in page["blocks"]:
                for line in block["lines"]:
                    words_line = []
                    for words in line["words"]:
                        words_line.append(words["value"])
                    lines.append(" ".join(words_line))
        return lines

    def load_docs(self):
        pass
