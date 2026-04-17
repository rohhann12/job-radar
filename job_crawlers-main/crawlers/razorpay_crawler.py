import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from email_config.email_setup import send_email
from database.mongo import ensure_company_document, add_jobs_if_not_exists


def run_crawler(url, num_job):
    list_of_jobs = []
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        # Lever-based careers pages
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.posting, [class*="posting"]')))
        time.sleep(2)

        job_cards = driver.find_elements(By.CSS_SELECTOR, '.posting')
        if not job_cards:
            job_cards = driver.find_elements(By.CSS_SELECTOR, '[class*="posting-title"]')

        for job_card in job_cards[:num_job]:
            try:
                title_elem = job_card.find_element(By.CSS_SELECTOR, 'h5, .posting-title h5, [class*="title"]')
                job_title = title_elem.text.strip()

                link_elem = job_card.find_element(By.CSS_SELECTOR, 'a[href*="/jobs/"]')
                job_link = link_elem.get_attribute('href')

                job_id = job_link.rstrip('/').split('/')[-1] if job_link else "N/A"

                if job_title and job_link:
                    list_of_jobs.append({
                        "company": "Razorpay",
                        "title": job_title,
                        "number": job_id,
                        "link": job_link
                    })
            except Exception as e:
                print(f"Error parsing Razorpay job: {e}")
                continue

    except Exception as e:
        print(f"Razorpay crawler error: {e}")
    finally:
        driver.quit()

    return list_of_jobs


async def async_run_crawler(executor, url, num_jobs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, run_crawler, url, num_jobs)


async def run_crawler_for_razorpay(receiverEmail=None):
    file_path = "urls/urls.json"
    ensure_company_document("Razorpay")

    with open(file_path, 'r') as file:
        position_urls = json.load(file)

    urls = position_urls.get("Razorpay", [])
    all_jobs = []
    num_jobs = 20

    with ThreadPoolExecutor() as executor:
        tasks = [async_run_crawler(executor, url, num_jobs) for url in urls]
        for task in asyncio.as_completed(tasks):
            jobs = await task
            if jobs:
                all_jobs.extend(jobs)
                added_jobs = add_jobs_if_not_exists(jobs)
                print("New Razorpay jobs:", added_jobs)
                if added_jobs:
                    send_email(added_jobs, receiverEmail)

    return all_jobs
