from response_evaluator import Collect_score

def sample_scores():
    return [
        Collect_score(category="structure_star", score="4", improvement_tip="Add more section headers to improve organization"),
        Collect_score(category="depth", score="3", improvement_tip="Provide more concrete examples from your experience"),
        Collect_score(category="clarity", score="5", improvement_tip="Continue using clear and concise language"),
        Collect_score(category="correctness", score="4", improvement_tip="Double-check technical specifications in your response"),
        Collect_score(category="structure_star", score="3", improvement_tip="Consider using bullet points for key highlights")
    ]