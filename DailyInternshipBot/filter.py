def rank_and_filter(jobs, skills):
    """
    Filters and ranks jobs based on user-defined skills.
    Calculates a match score based on keyword presence.
    """
    ranked_jobs = []
    skills_lower = [skill.lower() for skill in skills]
    
    for job in jobs:
        text_to_search = (job['title'] + " " + job['description']).lower()
        
        matches = 0
        for skill in skills_lower:
            if skill in text_to_search:
                matches += 1
                
        if matches > 0:
            match_score = int((matches / len(skills)) * 100)
            job['score'] = match_score
            ranked_jobs.append(job)
            
    # Sort by score descending
    ranked_jobs.sort(key=lambda x: x['score'], reverse=True)
    return ranked_jobs
