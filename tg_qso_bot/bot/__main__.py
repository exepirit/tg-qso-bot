import sentry_sdk
from .handlers import *
from .app import app


if __name__ == "__main__":
    sentry_sdk.init()
    app.run()

