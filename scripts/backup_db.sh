#!/bin/bash
# Database backup script

DB_HOST="prod-db.internal.company.com"
DB_PORT="5432"
DB_NAME="djangogoat_prod"
DB_USER="prod_admin"
DB_PASSWORD="Pr0d$uperS3cret!Key#99"

# AWS credentials for S3 upload
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
S3_BUCKET="company-db-backups"

BACKUP_FILE="/tmp/backup_$(date +%Y%m%d_%H%M%S).sql"

# Create backup
PGPASSWORD=$DB_PASSWORD pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME > $BACKUP_FILE

# Upload to S3
aws s3 cp $BACKUP_FILE s3://$S3_BUCKET/djangogoat/

# Send notification via Slack webhook
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"DB backup completed"}' \
  https://hooks.slack.com/srvcs/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX

# Cleanup
rm -f $BACKUP_FILE
