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
        time.sleep(5)  # Meta careers is React-heavy, needs extra time

        # Meta careers renders job rows with role="row" or a[href*="/jobs/"]
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="/jobs/"]')))

        job_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/jobs/"]')

        seen = set()
        for link_elem in job_links[:num_job * 2]:  # grab extra to dedupe
            try:
                job_link = link_elem.get_attribute('href')
                if not job_link or job_link in seen or '/jobs/' not in job_link:
                    continue
                seen.add(job_link)

                # Title is usually the text of the anchor or a child element
                job_title = link_elem.text.strip()
                if not job_title:
                    title_elem = link_elem.find_element(By.CSS_SELECTOR, 'span, div')
                    job_title = title_elem.text.strip()

                job_id = job_link.rstrip('/').split('/')[-1]

                if job_title and job_link and len(list_of_jobs) < num_job:
                    list_of_jobs.append({
                        "company": "Meta",
                        "title": job_title,
                        "number": job_id,
                        "link": job_link
                    })
            except Exception as e:
                print(f"Error parsing Meta job card: {e}")
                continue

    except Exception as e:
        print(f"Meta crawler error: {e}")
    finally:
        driver.quit()

    return list_of_jobs


async def async_run_crawler(executor, url, num_jobs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, run_crawler, url, num_jobs)


async def run_crawler_for_meta(receiverEmail=None):
    file_path = "urls/urls.json"
    ensure_company_document("Meta")

    with open(file_path, 'r') as file:
        position_urls = json.load(file)

    meta_urls = position_urls.get("Meta", [])
    all_jobs = []
    num_jobs = 20

    with ThreadPoolExecutor() as executor:
        tasks = [async_run_crawler(executor, url, num_jobs) for url in meta_urls]
        for task in asyncio.as_completed(tasks):
            jobs = await task
            if jobs:
                all_jobs.extend(jobs)
                added_jobs = add_jobs_if_not_exists(jobs)
                print("New Meta jobs:", added_jobs)
                if added_jobs:
                    send_email(added_jobs, receiverEmail)

    return all_jobs
