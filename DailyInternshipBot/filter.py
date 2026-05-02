import re

def rank_and_filter(jobs, skills):
    """
    Filters and ranks jobs based on user-defined skills.
    Calculates a match score based on keyword presence.
    """
    ranked_jobs = []
    
    # Pre-compile regex patterns for each skill to match whole words
    skill_patterns = []
    for skill in skills:
        skill_lower = skill.lower()
        # Use word boundaries only for alphanumeric characters to handle skills like C++ or .NET safely
        start_bound = r'\b' if skill_lower[0].isalnum() else r'(?<!\w)'
        end_bound = r'\b' if skill_lower[-1].isalnum() else r'(?!\w)'
        pattern = re.compile(start_bound + re.escape(skill_lower) + end_bound)
        skill_patterns.append(pattern)
    
    for job in jobs:
        text_to_search = (job['title'] + " " + job['description']).lower()
        
        matches = 0
        for pattern in skill_patterns:
            if pattern.search(text_to_search):
                matches += 1
                
        if matches > 0:
            match_score = int((matches / len(skills)) * 100)
            job['score'] = match_score
            ranked_jobs.append(job)
            
    # Sort by score descending
    ranked_jobs.sort(key=lambda x: x['score'], reverse=True)
    return ranked_jobs
