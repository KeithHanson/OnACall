FROM python:3.9 
# Or any preferred Python version.
ADD bot.py .
ADD .env .
ADD requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "-u", "./bot.py"] 
