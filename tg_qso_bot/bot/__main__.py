import asyncio
import sentry_sdk
import pyrogram
from .handlers import *
from .app import app, watchdog


async def main():
    sentry_sdk.init()
    await app.start()
    await asyncio.wait(
        (
            asyncio.create_task(pyrogram.idle()),
            asyncio.create_task(watchdog.run())
        ),
        return_when=asyncio.FIRST_COMPLETED
    )
    await app.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

