FROM public.ecr.aws/docker/library/python:3.12-slim

WORKDIR /app

# Install required packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user first
RUN useradd --create-home appuser

# Copy the application code and set ownership to appuser immediately
COPY --chown=appuser:appuser . .

# Create the log directory and set permissions
# This ensures that even if the volume isn't mounted, the app doesn't crash
RUN mkdir -p /tmp/logs && chown -R appuser:appuser /tmp/logs

USER appuser

# Expose the default FastAPI port
EXPOSE 8080

# Start the application
# Note: Ensure your FastAPI instance is named 'app' inside 'app.py'
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
