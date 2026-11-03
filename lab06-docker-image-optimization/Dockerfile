
# Stage: builder
FROM python:3.9-slim AS builder

WORKDIR /src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app

# Stage: stage-1
FROM python:3.9-alpine

WORKDIR /app

# Copy only necessary artifacts
COPY --from=builder /src/app /app

RUN ls -R /app

CMD ["python3", "app.py"]
