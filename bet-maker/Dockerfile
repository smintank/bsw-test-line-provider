FROM python:3.10
WORKDIR /app

RUN pip install uvicorn==0.34.0

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir && pip install --upgrade pip

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]