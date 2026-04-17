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
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[role="list"] > li')))
        time.sleep(3)

        job_elements = driver.find_elements(By.CSS_SELECTOR, 'ul[role="list"] > li')[:num_job]

        for job_element in job_elements:
            try:
                # Workday stable automation ID
                title_elem = job_element.find_element(By.CSS_SELECTOR, '[data-automation-id="jobTitle"]')
                job_url = title_elem.get_attribute("href")
                job_title = title_elem.text.strip()

                try:
                    job_id = job_element.find_element(By.CSS_SELECTOR, 'dl dd').text.strip()
                except Exception:
                    job_id = job_url.rstrip('/').split('/')[-1].split('_')[-1] if job_url else "N/A"

                if job_title and job_url:
                    list_of_jobs.append({
                        "company": "Atlassian",
                        "title": job_title,
                        "number": job_id,
                        "link": job_url
                    })
            except Exception as e:
                print(f"Error parsing Atlassian job: {e}")
                continue

    except Exception as e:
        print(f"Atlassian crawler error: {e}")
    finally:
        driver.quit()

    return list_of_jobs


async def async_run_crawler(executor, url, num_jobs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, run_crawler, url, num_jobs)


async def run_crawler_for_atlassian(receiverEmail=None):
    file_path = "urls/urls.json"
    ensure_company_document("Atlassian")

    with open(file_path, 'r') as file:
        position_urls = json.load(file)

    urls = position_urls.get("Atlassian", [])
    all_jobs = []
    num_jobs = 20

    with ThreadPoolExecutor() as executor:
        tasks = [async_run_crawler(executor, url, num_jobs) for url in urls]
        for task in asyncio.as_completed(tasks):
            jobs = await task
            if jobs:
                all_jobs.extend(jobs)
                added_jobs = add_jobs_if_not_exists(jobs)
                print("New Atlassian jobs:", added_jobs)
                if added_jobs:
                    send_email(added_jobs, receiverEmail)

    return all_jobs
