from core.config.config import BOOKS_INDEX_RAW_PATH, WL_API_BOOKS_URL
from core.utils.common_utils import json_request, save_json_file


class BookIndexRawService:
    @staticmethod
    def download_books_index_raw_json(
        save_path=BOOKS_INDEX_RAW_PATH, url=WL_API_BOOKS_URL
    ) -> None:
        """
        Pobiera surowy indeks książek z API Wolnych Lektur i zapisuje go do pliku JSON.
        :param save_path:
        :param url:
        :return:
        """
        json_file = json_request(url)
        save_json_file(json_file, save_path)
