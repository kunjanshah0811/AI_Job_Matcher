import streamlit as st
import PyPDF2
from typing import Tuple, Dict, Any

class FileProcessor:
    @staticmethod
    def read_resume(file) -> str:
        """Process resume PDF file"""
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()

    @staticmethod
    def read_job_description_pdf(file) -> str:
        """Process job description PDF file"""
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()

    @staticmethod
    def read_job_description_txt(file) -> str:
        """Process job description TXT file"""
        return file.read().decode("utf-8").strip()
