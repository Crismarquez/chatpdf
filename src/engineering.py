
from src.recognition import Recognition
from src.data import DatasetManager

class OCREngineering:
    def __init__(
            self,
            recognition: Recognition,
            dataset_manager: DatasetManager
            ):
        
        self.recognition = recognition
        self.dataset_manager = dataset_manager

    def process(self):
        pass

    def load_docs(self):
        pass