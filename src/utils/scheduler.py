from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()


def schedule_func(func, **job_kwargs):
    scheduler.add_job(func=func, **job_kwargs)
