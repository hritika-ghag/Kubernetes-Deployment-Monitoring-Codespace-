FROM python:3.11-slim

WORKDIR /app

# Copy app (no pip installs required)
COPY app.py .

# Make the script executable
RUN chmod +x /app/app.py

ENV PORT=8080
EXPOSE 8080

CMD ["python", "/app/app.py"]
