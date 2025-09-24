import pytest
from unittest.mock import patch
from backend.src.services.scraper_linkedin import scrape_linkedin_jobs
from backend.src.services.scraper_indeed import scrape_indeed_jobs
from backend.src.services.scraper_dice import scrape_dice_jobs
from backend.src.services.scraper import scrape_all_jobs, get_job_keywords
import os

# Mock response for requests.get
class MockResponse:
    def __init__(self, text, status_code):
        self.text = text
        self.status_code = status_code

    @property
    def content(self):
        return self.text.encode('utf-8')


@patch('requests.get')
def test_scrape_linkedin_jobs(mock_get):
    mock_get.return_value = MockResponse("<html><body><div class=\"base-card\"><h3>Software Engineer</h3><p>LinkedIn</p></div></body></html>", 200)
    jobs = scrape_linkedin_jobs(["Python"])
    assert len(jobs) == 1
    assert jobs[0]["title"] == "Software Engineer - Python"
    assert jobs[0]["company"] == "LinkedIn Corp"

@patch('requests.get')
def test_scrape_indeed_jobs(mock_get):
    mock_get.return_value = MockResponse("<html><body><div class=\"jobsearch-SerpJobCard\"><h3>Data Scientist</h3><p>Indeed</p></div></body></html>", 200)
    jobs = scrape_indeed_jobs(["Machine Learning"])
    assert len(jobs) == 1
    assert jobs[0]["title"] == "Data Scientist - Machine Learning"
    assert jobs[0]["company"] == "Indeed Inc."

@patch('requests.get')
def test_scrape_dice_jobs(mock_get):
    mock_get.return_value = MockResponse("<html><body><div class=\"card-content\"><h3>DevOps Engineer</h3><p>Dice</p></div></body></html>", 200)
    jobs = scrape_dice_jobs(["Kubernetes"])
    assert len(jobs) == 1
    assert jobs[0]["title"] == "DevOps Engineer - Kubernetes"
    assert jobs[0]["company"] == "Dice Co."

def test_get_job_keywords():
    os.environ["JOB_KEYWORDS"] = "Python, Java,  React  "
    keywords = get_job_keywords()
    assert keywords == ["Python", "Java", "React"]
    del os.environ["JOB_KEYWORDS"]

def test_scrape_all_jobs_deduplication():
    with patch('backend.src.services.scraper_linkedin.scrape_linkedin_jobs') as mock_linkedin,
         patch('backend.src.services.scraper_indeed.scrape_indeed_jobs') as mock_indeed,
         patch('backend.src.services.scraper_dice.scrape_dice_jobs') as mock_dice:

        mock_linkedin.return_value = [
            {"title": "Job A", "company": "Company X", "description": "", "application_link": "", "salary": "", "status": "new"}
        ]
        mock_indeed.return_value = [
            {"title": "Job A", "company": "Company X", "description": "", "application_link": "", "salary": "", "status": "new"},
            {"title": "Job B", "company": "Company Y", "description": "", "application_link": "", "salary": "", "status": "new"}
        ]
        mock_dice.return_value = [
            {"title": "Job A", "company": "Company X", "description": "", "application_link": "", "salary": "", "status": "new"},
            {"title": "Job C", "company": "Company Z", "description": "", "application_link": "", "salary": "", "status": "new"}
        ]

        os.environ["JOB_KEYWORDS"] = "test"
        jobs = scrape_all_jobs()
        del os.environ["JOB_KEYWORDS"]

        assert len(jobs) == 3
        assert any(job["title"] == "Job A" and job["company"] == "Company X" for job in jobs)
        assert any(job["title"] == "Job B" and job["company"] == "Company Y" for job in jobs)
        assert any(job["title"] == "Job C" and job["company"] == "Company Z" for job in jobs)
