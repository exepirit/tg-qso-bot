FROM python:3-slim

WORKDIR /app
COPY . .

RUN python3 -m pip install --upgrade pip \
 && python3 -m pip install .

CMD ["python3", "-m", "tg_qso_bot.bot"]