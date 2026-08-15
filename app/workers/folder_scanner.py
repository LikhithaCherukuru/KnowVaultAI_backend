import os
import mimetypes

from app.utils.hash_utils import generate_sha256
from app.utils.file_metadata import get_file_metadata


SUPPORTED_EXTENSIONS = {

    ".pdf",
    ".docx",
    ".pptx",
    ".txt",
    ".png",
    ".jpg",
    ".jpeg"

}


class IndexingWorker:

    def scan(self, folder_path: str):

        files = []

        for root, dirs, filenames in os.walk(folder_path):

            for filename in filenames:

                extension = os.path.splitext(filename)[1].lower()

                if extension not in SUPPORTED_EXTENSIONS:
                    continue

                full_path = os.path.join(root, filename)

                metadata = get_file_metadata(full_path)

                metadata["mime_type"] = mimetypes.guess_type(full_path)[0]

                metadata["file_hash"] = generate_sha256(full_path)

                files.append(metadata)

        return files