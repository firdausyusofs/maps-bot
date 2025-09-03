import schedule
import time
import datetime
import subprocess

def job():
    print(f"Running {datetime.datetime.now()}")
    subprocess.run(["python3", "final.py"])

# Definer tidsvindue
for hour in range(6, 24):  # 06:00 til 23:30
    schedule.every().hour.at(":00").do(job)
    schedule.every().hour.at(":30").do(job)

# Tilføj 00:00 og 00:30
schedule.every().day.at("00:00").do(job)
schedule.every().day.at("00:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(10)