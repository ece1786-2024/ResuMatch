# resume_parser/core.py

import re
import docx
import pdfplumber
from typing import Dict
from feature_extraction_agent.feature_extraction_agent import FeatureExtractionAgent

class ResumeParser:
    def __init__(self, file_path):        
        self.feature_extrator_agent = FeatureExtractionAgent(
            name="feature_extractor",
            # sys_prompt="You are a helpful assistant for parsing resume.",
            max_tokens=100
        )
        
        # Parse resume file to text - keep object var of text
        if file_path.endswith('.pdf'):
            self.text = self._extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            self.text = self._extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format")

    def extract_resume_features(self,) -> Dict:
        # Extract features
        formatted_data = self.feature_extrator_agent.extract_features(self.text)
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
