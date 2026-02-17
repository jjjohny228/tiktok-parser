from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()


def schedule_func(func, **job_kwargs):
    scheduler.add_job(func=func, **job_kwargs)


def async_schedule_func(func, **job_kwargs):
    async def wrapper():
        await func()

    scheduler.add_job(func=wrapper, **job_kwargs)
