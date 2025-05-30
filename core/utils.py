import PyPDF2
from pydantic import BaseModel

class Collect_score(BaseModel):
    category: str
    score: str
    improvement_tip: str

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


def trim_backticks(model_response: str):
    return model_response[8:-4]

def star_rating(n, out_of=5):
    return "★" * n + "☆" * (out_of - n)

def least_scores(scores):
    result = []
    for item in scores:
        # Find the category with the minimum score
        min_category = None
        min_score = float('inf')
        min_tip = ""
        
        for category, data in item.items():
            if data["score"] < min_score:
                min_score = data["score"]
                min_category = category
                min_tip = data["improvement_tip"]
        
        # Create Collect_score object for the minimum score
        result.append(Collect_score(
            category=min_category,
            score=str(min_score),
            improvement_tip=min_tip
        ))
    
    return result