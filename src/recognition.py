from pathlib import Path
from doctr.models import ocr_predictor
from doctr.io import DocumentFile


class Recognition:
    """
    OCR Recognition class
    ---------------------
    args:
        det_arch: str = "db_resnet50" - detection architecture
        reco_arch: str = "crnn_vgg16_bn" - recognition architecture
    """
    # TODO: add more architectures, ex. docs not aligned 
    def __init__(self, det_arch: str = "db_resnet50", reco_arch: str = "crnn_vgg16_bn"):
        self.det_arch = det_arch
        self.reco_arch = reco_arch
        self._load_model()

    def _load_model(self):
        self.model = ocr_predictor(
            det_arch=self.det_arch, reco_arch=self.reco_arch, pretrained=True
        )

    def recognize(self, doc: DocumentFile):
        result = self._recognize(doc)
        json_result = result.export()
        return json_result

    def _recognize(self, doc: DocumentFile):
        return self.model(doc)
