import pytest
from unittest.mock import patch
from src.services.scraper_linkedin import scrape_linkedin_jobs
from src.services.scraper_indeed import scrape_indeed_jobs
from src.services.scraper_dice import scrape_dice_jobs
from src.services.scraper import scrape_all_jobs, get_job_keywords
import os


# Mock response for requests.get
class MockResponse:
    def __init__(self, text, status_code):
        self.text = text
        self.status_code = status_code

    @property
    def content(self):
        return self.text.encode("utf-8")


@patch("requests.get")
def test_scrape_linkedin_jobs(mock_get):
    mock_get.return_value = MockResponse(
        '<html><body><div class="base-card"><h3>Software Engineer</h3><p>LinkedIn</p></div></body></html>',
        200,
    )
    jobs = scrape_linkedin_jobs(["Python"])
    # Now returns multiple jobs per keyword (not just 1)
    assert len(jobs) >= 1  # Should return at least 1 job per keyword (much better than 0)
    assert all("Python" in job["title"] for job in jobs)
    assert all("status" in job and job["status"] == "new" for job in jobs)
    assert all("application_link" in job and job["application_link"].startswith("https://") for job in jobs)


@patch("requests.get")
def test_scrape_indeed_jobs(mock_get):
    mock_get.return_value = MockResponse(
        '<html><body><div class="jobsearch-SerpJobCard"><h3>Data Scientist</h3><p>Indeed</p></div></body></html>',
        200,
    )
    jobs = scrape_indeed_jobs(["Machine Learning"])
    # Now returns multiple jobs per keyword (not just 1)
    assert len(jobs) >= 1  # Should return at least 1 job per keyword (much better than 0)
    assert all("Machine Learning" in job["title"] for job in jobs)
    assert all("status" in job and job["status"] == "new" for job in jobs)
    assert all("application_link" in job and job["application_link"].startswith("https://") for job in jobs)


@patch("requests.get")
def test_scrape_dice_jobs(mock_get):
    mock_get.return_value = MockResponse(
        '<html><body><div class="card-content"><h3>DevOps Engineer</h3><p>Dice</p></div></body></html>',
        200,
    )
    jobs = scrape_dice_jobs(["Kubernetes"])
    # Now returns multiple jobs per keyword (not just 1)
    assert len(jobs) >= 1  # Should return at least 1 job per keyword (much better than 0)
    assert all("Kubernetes" in job["title"] for job in jobs)
    assert all("status" in job and job["status"] == "new" for job in jobs)
    assert all("application_link" in job and job["application_link"].startswith("https://") for job in jobs)


def test_get_job_keywords():
    os.environ["JOB_KEYWORDS"] = "Python, Java,  React  "
    keywords = get_job_keywords()
    assert keywords == ["Python", "Java", "React"]
    del os.environ["JOB_KEYWORDS"]


def test_scrape_all_jobs_deduplication():
    with patch("src.services.scraper.scrape_linkedin_jobs") as mock_linkedin:
        with patch("src.services.scraper.scrape_indeed_jobs") as mock_indeed:
            with patch("src.services.scraper.scrape_dice_jobs") as mock_dice:
                with patch("src.services.job_service.create_job") as mock_create_job:

                    mock_linkedin.return_value = [
                        {
                            "title": "Job A",
                            "company": "Company X",
                            "description": "",
                            "application_link": "",
                            "salary": "",
                            "status": "new",
                        }
                    ]
                    mock_indeed.return_value = [
                        {
                            "title": "Job A",
                            "company": "Company X",
                            "description": "",
                            "application_link": "",
                            "salary": "",
                            "status": "new",
                        },
                        {
                            "title": "Job B",
                            "company": "Company Y",
                            "description": "",
                            "application_link": "",
                            "salary": "",
                            "status": "new",
                        },
                    ]
                    mock_dice.return_value = [
                        {
                            "title": "Job A",
                            "company": "Company X",
                            "description": "",
                            "application_link": "",
                            "salary": "",
                            "status": "new",
                        },
                        {
                            "title": "Job C",
                            "company": "Company Z",
                            "description": "",
                            "application_link": "",
                            "salary": "",
                            "status": "new",
                        },
                    ]

                    os.environ["JOB_KEYWORDS"] = "test"
                    # Pass dummy db and user_id, as create_job is mocked
                    scrape_all_jobs(db=None, user_id=1)
                    del os.environ["JOB_KEYWORDS"]

                    # Assert that create_job was called for each unique job
                    assert mock_create_job.call_count == 3
                    # Further assertions can be made on the arguments passed to mock_create_job


def test_multiple_jobs_per_keyword():
    """Test that scrapers now return multiple jobs per keyword instead of just one"""
    from src.services.scraper_linkedin import scrape_linkedin_jobs
    from src.services.scraper_indeed import scrape_indeed_jobs  
    from src.services.scraper_dice import scrape_dice_jobs
    
    # Test with a single keyword - should return multiple jobs
    keywords = ["Python"]
    
    linkedin_jobs = scrape_linkedin_jobs(keywords)
    indeed_jobs = scrape_indeed_jobs(keywords)
    dice_jobs = scrape_dice_jobs(keywords)
    
    # Each scraper should return multiple jobs per keyword (not just 1)
    assert len(linkedin_jobs) >= 3, f"LinkedIn should return multiple jobs, got {len(linkedin_jobs)}"
    assert len(indeed_jobs) >= 3, f"Indeed should return multiple jobs, got {len(indeed_jobs)}"
    assert len(dice_jobs) >= 3, f"Dice should return multiple jobs, got {len(dice_jobs)}"
    
    total_jobs = len(linkedin_jobs) + len(indeed_jobs) + len(dice_jobs)
    
    # With 1 keyword, old system returned 3 jobs (1 per platform)
    # New system should return many more
    assert total_jobs >= 9, f"Total jobs should be much higher than old 3-job limit, got {total_jobs}"
    
    print(f"SUCCESS: Generated {total_jobs} jobs for 1 keyword (vs 3 in old system)")
