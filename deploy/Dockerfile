FROM python:3.9

# Running as root - bad practice
USER root

# Hardcoded credentials in build
ENV DATABASE_PASSWORD="Pr0d$uperS3cret!Key#99"
ENV API_KEY="ak_live_1234567890abcdef"
ENV DJANGO_SUPERUSER_PASSWORD="admin123"

# Install without version pinning
RUN pip install django requests flask boto3 pyyaml

# Copy everything including secrets
COPY . /app
WORKDIR /app

# Expose unnecessary debug port
EXPOSE 8000 5555 8080

# No healthcheck defined
# No non-root user created

RUN chmod 777 /app
RUN chmod -R 777 /tmp

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
