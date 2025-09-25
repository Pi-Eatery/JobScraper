import os
from typing import List, Dict
from sqlalchemy.orm import Session
from .scraper_linkedin import scrape_linkedin_jobs
from .scraper_indeed import scrape_indeed_jobs
from .scraper_dice import scrape_dice_jobs
from ..services import job_service


def get_job_keywords() -> List[str]:
    keywords_str = os.getenv("JOB_KEYWORDS", "")
    return [keyword.strip() for keyword in keywords_str.split(",") if keyword.strip()]


def scrape_all_jobs(db: Session, user_id: int) -> None:
    keywords = get_job_keywords()
    if not keywords:
        print("No job keywords found in JOB_KEYWORDS environment variable.")
        return

    all_jobs_data = []
    seen_jobs = set()  # To store unique job identifiers (title, company)

    scraped_linkedin = scrape_linkedin_jobs(keywords)
    scraped_indeed = scrape_indeed_jobs(keywords)
    scraped_dice = scrape_dice_jobs(keywords)

    for job_list in [scraped_linkedin, scraped_indeed, scraped_dice]:
        for job_data in job_list:
            job_identifier = (job_data.get("title"), job_data.get("company"))
            if job_identifier not in seen_jobs:
                all_jobs_data.append(job_data)
                seen_jobs.add(job_identifier)

    for job_data in all_jobs_data:
        job_service.create_job(db, job_data, user_id)



