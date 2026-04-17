import asyncio
import os
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from flask_cors import CORS

from crawlers.microsoft import run_crawler_for_microsoft
from crawlers.amazon_crawler import run_crawler_for_amazon
from crawlers.google_crawler import run_crawler_for_google
from crawlers.meta_crawler import run_crawler_for_meta
from crawlers.nvidia import run_crawler_for_nvidia
from crawlers.atlassian_crawler import run_crawler_for_atlassian
from crawlers.adobe_crawler import run_crawler_for_adobe
from crawlers.salesforce_crawler import run_crawler_for_salesforce
from crawlers.razorpay_crawler import run_crawler_for_razorpay
from crawlers.goldmanSachs import run_crawler_for_goldman_sachs
from crawlers.docusign import run_crawler_for_docusign
from crawlers.amd_crawler import run_crawler_for_amd

app = Flask(__name__)
CORS(app)


def check_new_job(receiverEmail=None):
    print("Starting job check for:", receiverEmail)

    # Big Tech - India / Global
    asyncio.run(run_crawler_for_google(receiverEmail))
    asyncio.run(run_crawler_for_microsoft(receiverEmail))
    asyncio.run(run_crawler_for_amazon(receiverEmail))
    asyncio.run(run_crawler_for_meta(receiverEmail))
    asyncio.run(run_crawler_for_nvidia(receiverEmail))

    # Workday-based - India
    asyncio.run(run_crawler_for_atlassian(receiverEmail))
    asyncio.run(run_crawler_for_adobe(receiverEmail))
    asyncio.run(run_crawler_for_salesforce(receiverEmail))
    asyncio.run(run_crawler_for_amd(receiverEmail))

    # India Startups / Fintech
    asyncio.run(run_crawler_for_razorpay(receiverEmail))

    # Others
    asyncio.run(run_crawler_for_goldman_sachs(receiverEmail))
    asyncio.run(run_crawler_for_docusign(receiverEmail))

    print("Job check complete.")


@app.route('/check_new_job', methods=['GET'])
def handle_check_new_job():
    check_new_job()
    return {"message": "Job check complete"}, 200


def schedule_job_checks(receiverEmail):
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_new_job, 'interval', minutes=15, args=[receiverEmail])
    scheduler.start()


@app.route('/main', methods=['POST'])
def handle_check_periodically():
    data = request.get_json()
    receiver_email = data.get("email")
    print("Received email:", receiver_email)

    if not receiver_email:
        return {"error": "Email is required"}, 400

    schedule_job_checks(receiver_email)
    return {"message": f"Scheduled job checks every 15 minutes for {receiver_email}"}, 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
