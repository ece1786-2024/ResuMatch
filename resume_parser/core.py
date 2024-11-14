# resume_parser/core.py

import re
import docx
import pdfplumber
from typing import Dict
from .openai_api import OpenAIAPI

class ResumeParser:
    def __init__(self, api_key: str, model: str):
        self.openai_api = OpenAIAPI(api_key, model)
        self.default_json_structure = {
            "industry": "",
            "experience level": ""
        }

    def parse(self, file_path: str, json_structure: dict = None) -> Dict:
        if file_path.endswith('.pdf'):
            text = self._extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            text = self._extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format")

        if json_structure is None:
            json_structure = self.default_json_structure

        formatted_data = self.openai_api.format_text_to_json(text, json_structure)
        return formatted_data

    @staticmethod
    def _extract_text_from_pdf(file_path: str) -> str:
        with pdfplumber.open(file_path) as pdf:
            text = ''.join([page.extract_text() for page in pdf.pages])
        return text

    @staticmethod
    def _extract_text_from_docx(file_path: str) -> str:
        doc = docx.Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
        return text
