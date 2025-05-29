from linkedin_scraper.scraper import setup_driver, scrape_jobs, login_to_linkedin
import csv
import os
from urllib.parse import quote

if __name__ == "__main__":
    driver = setup_driver()

    # 🔐 Log in to LinkedIn
    login_to_linkedin(driver)

    # Define multiple search terms and locations
    search_terms = ["Data Analyst",
                    "Business Analyst", "Junior Data Scientist"]
    locations = ["India", "Remote"]

    all_jobs = []

    for term in search_terms:
        for location in locations:
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={quote(term)}&location={quote(location)}"
            print(f"[INFO] Navigating to: {search_url}")
            driver.get(search_url)
            jobs = scrape_jobs(driver, job_limit=200)  # Adjust limit if needed
            all_jobs.extend(jobs)

    driver.quit()

    # Save all collected jobs to CSV
    os.makedirs("data", exist_ok=True)
    with open("data/linkedin_jobs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["Title", "Company", "Location", "Date Posted", "Skills", "Job Link"])
        writer.writeheader()
        writer.writerows(all_jobs)

    print(f"✅ Scraping complete. Total jobs collected: {len(all_jobs)}")
    print("📁 Data saved to data/linkedin_jobs.csv")
