# resume_parser/core.py

import re
import docx
import pdfplumber
from typing import Dict
from feature_extraction_agent.feature_extraction_agent import FeatureExtractionAgent


class ResumeParser:
    def __init__(self, ):        
        self.feature_extrator_agent = FeatureExtractionAgent(
            name="feature_extractor",
            sys_prompt="You are a helpful assistant for parsing resume.",
            max_tokens=100
        )

    def parse(self, file_path: str, json_structure: dict = None) -> Dict:
        if file_path.endswith('.pdf'):
            text = self._extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            text = self._extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format")

        if json_structure is None:
            json_structure = self.default_json_structure

        formatted_data = self.feature_extrator_agent.extract_features(text, json_structure)
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
