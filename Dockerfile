FROM python:3.10-slim
WORKDIR /app

# Copy all files in this folder into /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5002
CMD ["python", "brute_force.py"]
