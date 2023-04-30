import os
from doctr.io import DocumentFile
from langchain import OpenAI
from llama_index import SimpleDirectoryReader, LangchainEmbedding, GPTListIndex,GPTSimpleVectorIndex, PromptHelper
from llama_index import LLMPredictor, ServiceContext


from src.recognition import Recognition
from src.data import DatasetManager
from config.config import DATA_DIR, ENV_VARIABLES, logger


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
            logger.info(f"Processing ocr engineering in {pdf_dir.name}")
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

class LLMEngineering:
    def __init__(self, dataset_manager: DatasetManager):
        self.dataset_manager = dataset_manager
        self.model_intenced = False
        self._load_index()

    def train(self, model_name:str="text-davinci-002", num_outputs: int = 256):
        self._dataloader()
        llm_predictor = LLMPredictor(
            llm=OpenAI(temperature=0, model_name=model_name, max_tokens=num_outputs)
            )
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
        self.model = GPTSimpleVectorIndex.from_documents(
            self.documents, service_context=service_context
            )
        self.model_intenced = True
        self._save_index()

    def predict(self, query: str, response_mode: str = "compact"):
        if not self.model_intenced:
            logger.warning("No index found, please run train method")
            return None
        response = self._predict(query, response_mode)
        return response.response

    def _predict(self, query: str, response_mode: str = "compact"):
        response = self.model.query(query, response_mode=response_mode)
        return response

    def _load_index(self):
        if (self.dataset_manager.project_dir/ 'index.json').exists():
            logger.info("Loading existing index")
            self.model = GPTSimpleVectorIndex.load_from_disk(
                self.dataset_manager.project_dir/ 'index.json'
            )
            self.model_intenced = True
        else:
            logger.warning("No index found, please run train method")

    def _dataloader(self):
        self.documents = SimpleDirectoryReader(
            self.dataset_manager.project_dir / "text_files"
            ).load_data()
        
    def _save_index(self):
        self.model.save_to_disk(self.dataset_manager.project_dir/ 'index.json')