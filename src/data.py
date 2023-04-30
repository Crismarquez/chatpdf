from pathlib import Path

from config.config import PROEJECTS_DIR, logger


class DatasetManager:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_dir = PROEJECTS_DIR / self.project_name
        self._setup_dir()

    def get_pdf_files(self):
        pdf_files = [f for f in self.project_files["documents"] if f.suffix == ".pdf"]
        # sort by index
        pdf_files = sorted(pdf_files, key=lambda x: int(x.name.split("-")[0]) )
        return pdf_files

    def save_text(self, lines: list):
        text_dir = self.project_dir / "text_files"
        with open(str(text_dir / "all_lines.txt"), "w") as f:
            for line in lines:
                f.write(f"{line}\n")
        logger.info(f"Saved {len(lines)} lines in {text_dir / 'all_lines.txt'}")

    def pdf_to_process(self):
        """
        Find pdf that have not been processed
        """
        self._mapping()
        self.project_files["documents"]

    def _setup_dir(self):
        self._validate_dir()
        self._mapping()

    def _validate_dir(self):
        if self.project_dir.exists():
            logger.info(f"Project {self.project_name} already exists")
            if (self.project_dir / "documents").exists():
                logger.info(f"documents folder already has documents")
            else:
                logger.info(f"Creating documents folder")
                (self.project_dir / "documents").mkdir()
            if (self.project_dir / "text_files").exists():
                logger.info(f"text_files folder already has results")
            else:
                logger.info(f"Creating text_files folder")
                (self.project_dir / "text_files").mkdir()
        else:
            logger.info(f"Creating project {self.project_name}")
            self.project_dir.mkdir()
            (self.project_dir / "documents").mkdir()
            (self.project_dir / "text_files").mkdir()

    def _mapping(self):
        self.project_files = {
            "documents": [
                file
                for file in (self.project_dir / "documents").iterdir()
                if file.suffix == ".pdf"
            ],
            "text_files": [
                file
                for file in (self.project_dir / "text_files").iterdir()
                if file.suffix == ".txt"
            ],
        }

        logger.info(
            f"Project {self.project_name} has {len(self.project_files['documents'])} documents"
        )

    def _storage_conections(self):
        pass
