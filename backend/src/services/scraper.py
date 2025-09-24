import os
from typing import List, Dict
from backend.src.services.scraper_linkedin import scrape_linkedin_jobs
from backend.src.services.scraper_indeed import scrape_indeed_jobs
from backend.src.services.scraper_dice import scrape_dice_jobs

def get_job_keywords() -> List[str]:
    keywords_str = os.getenv("JOB_KEYWORDS", "")
    return [keyword.strip() for keyword in keywords_str.split(",") if keyword.strip()]

def scrape_all_jobs() -> List[Dict]:
    keywords = get_job_keywords()
    if not keywords:
        print("No job keywords found in JOB_KEYWORDS environment variable.")
        return []

    all_jobs = []
    seen_jobs = set() # To store unique job identifiers (title, company)

    scraped_linkedin = scrape_linkedin_jobs(keywords)
    scraped_indeed = scrape_indeed_jobs(keywords)
    scraped_dice = scrape_dice_jobs(keywords)

    for job_list in [scraped_linkedin, scraped_indeed, scraped_dice]:
        for job in job_list:
            job_identifier = (job.get("title"), job.get("company"))
            if job_identifier not in seen_jobs:
                all_jobs.append(job)
                seen_jobs.add(job_identifier)

    return all_jobs

if __name__ == "__main__":
    # Example usage
    os.environ["JOB_KEYWORDS"] = "Python,FastAPI,React"
    jobs = scrape_all_jobs()
    for job in jobs:
        print(job)
