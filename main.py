from doctr.io import DocumentFile

from src.recognition import Recognition
from src.data import DatasetManager
from config.config import DATA_DIR

ocr_recognition = Recognition(
    det_arch="db_resnet50",
    reco_arch="crnn_vgg16_bn"
)

project_dir = DATA_DIR / "projects" / "anual_reports"
pdf_file = "Amazon-2022-Annual-Report-2.pdf"
# pdf_file = "CM.pdf"

doc = DocumentFile.from_pdf(project_dir / "documents" / pdf_file)

results = ocr_recognition.recognize(doc)

json_result = results.export()

text = []
for block in json_result["pages"][0]["blocks"]:
    for lines in block["lines"]:
        for words in lines["words"]:
            print(words["value"], end=" ")
            text.append(words["value"] + " ")
        print("")


results.show(doc)

print("")