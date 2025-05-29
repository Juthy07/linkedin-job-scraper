from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from typing import List, Dict
import os
import time

load_dotenv()


def setup_driver() -> WebDriver:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver


def login_to_linkedin(driver):
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")

    driver.get("https://www.linkedin.com/login")
    time.sleep(3)
    try:
        driver.find_element(By.ID, "username").send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print("🔐 Logged into LinkedIn successfully.")
        time.sleep(5)
    except Exception as e:
        print(f"[!] Login failed: {e}")


def scrape_single_job(driver, wait, job, index):
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", job)
        job.click()
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".jobs-details__main-content")))

        content_container = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".jobs-details__main-content"))
        )

        job_title = content_container.find_element(By.TAG_NAME, "h1").text
        company_name = content_container.find_element(
            By.CSS_SELECTOR, ".t-14 > .relative > div > div > .display-flex"
        ).text.strip()
        location = content_container.find_element(
            By.CSS_SELECTOR,
            ".t-14 > div.relative.job-details-jobs-unified-top-card__container--two-pane > div > div.job-details-jobs-unified-top-card__primary-description-container > div > span > span:nth-child(1)"
        ).text.strip()

        job_link = driver.current_url

        # 🔍 Extract skills (improved: wait for modal header before collecting)
        skills = []
        try:
            skill_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "job-details-preferences-and-skills__pill"))
            )
            skill_button.click()

            # 🕒 Wait for modal header to confirm modal is fully loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "preferences-and-skills-modal__title"))
            )

            # 🕒 Wait for skills list to appear
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.ml2.flex-1 span.text-body-small"))
            )

            # ✅ Now fetch skill elements
            skill_elements = driver.find_elements(
                By.CSS_SELECTOR, "div.ml2.flex-1 span.text-body-small")
            skills = [el.text.strip()
                      for el in skill_elements if el.text.strip()]
        except Exception as e:
            print(f"[!] Skills not found or modal failed to load: {e}")

        # ❌ Close the modal (important!)
        try:
            close_button = driver.find_element(
                By.CLASS_NAME, "artdeco-modal__dismiss")
            close_button.click()
            time.sleep(1)
        except Exception:
            print("[!] Modal close button not found or already closed.")

        # 📅 Date posted
        try:
            all_spans = content_container.find_elements(
                By.CSS_SELECTOR, "span.tvm__text.tvm__text--low-emphasis"
            )
            for s in all_spans:
                if "ago" in s.text.lower():
                    date_posted = s.text.strip()
                    break
            else:
                date_posted = "Not found"
        except Exception:
            date_posted = "Not found"

        print(f"[{index+1}] ✅ {job_title} at {company_name} | {skills} | {job_link}")

        return {
            "Title": job_title,
            "Company": company_name,
            "Location": location,
            "Date Posted": date_posted,
            "Skills": ", ".join(skills),
            "Job Link": job_link
        }

    except Exception as e:
        print(f"[{index+1}] ❌ Failed to scrape job: {e}")
        return None


def scrape_jobs(driver: WebDriver, job_limit=1):
    wait = WebDriverWait(driver, 50)

    print("[INFO] Scrolling page...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    print("[INFO] Finding job cards...")
    job_list_container = driver.find_element(
        By.CSS_SELECTOR, ".scaffold-layout__list > div")
    job_elements: List[WebElement] = job_list_container.find_elements(
        By.CSS_SELECTOR, "li[id^='ember']:not([class*='pagination'])"
    )

    print(f"[DEBUG] Found {len(job_elements)} jobs")

    try:
        close_any_modal = driver.find_element(
            By.CLASS_NAME, "artdeco-modal__dismiss")
        close_any_modal.click()
        time.sleep(1)
    except Exception:
        pass

    jobs = []
    for index, job in enumerate(job_elements[:job_limit]):
        job_data = scrape_single_job(driver, wait, job, index)
        if job_data:
            jobs.append(job_data)

    print(f"✅ Scraped {len(jobs)} jobs successfully.")
    return jobs
