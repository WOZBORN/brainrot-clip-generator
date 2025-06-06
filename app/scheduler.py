from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import pipeline_task

# один-единственный BackgroundScheduler на всё приложение
scheduler = BackgroundScheduler()

def start_scheduler():
    if not scheduler.running:
        # добавляем задачу с нужным интервалом, здесь — каждый час
        print("Starting scheduler")
        scheduler.add_job(
            pipeline_task,
            trigger="interval",
            hours=12,
            id="brainrot_pipeline",
            next_run_time=datetime.now(),
            max_instances=1,
            coalesce=True
        )
        scheduler.start()
        print("Scheduler started")

def stop_scheduler():
    if scheduler.running:
        scheduler.remove_job("brainrot_pipeline")
        scheduler.shutdown(wait=False)
