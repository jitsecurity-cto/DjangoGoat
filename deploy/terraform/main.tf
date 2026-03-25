# Terraform configuration with security misconfigurations

provider "aws" {
  region     = "us-east-1"
  access_key = "AKIAIOSFODNN7EXAMPLE"
  secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}

# S3 bucket with public access and no encryption
resource "aws_s3_bucket" "app_data" {
  bucket = "djangogoat-prod-data"
  acl    = "public-read-write"

  versioning {
    enabled = false
  }

  # No server-side encryption configured
  # No access logging configured
}

# Security group allowing all traffic
resource "aws_security_group" "web_sg" {
  name        = "djangogoat-web-sg"
  description = "Web security group"

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# RDS instance with public access and no encryption
resource "aws_db_instance" "prod_db" {
  identifier     = "djangogoat-prod"
  engine         = "postgres"
  engine_version = "13.4"
  instance_class = "db.t3.medium"

  username = "prod_admin"
  password = "Pr0d$uperS3cret!Key#99"

  publicly_accessible    = true
  skip_final_snapshot    = true
  storage_encrypted      = false
  deletion_protection    = false
  backup_retention_period = 0

  vpc_security_group_ids = [aws_security_group.web_sg.id]
}

# EC2 instance with IMDSv1 and no monitoring
resource "aws_instance" "web_server" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t3.medium"

  vpc_security_group_ids = [aws_security_group.web_sg.id]

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "optional"  # IMDSv1 enabled - should require IMDSv2
  }

  monitoring = false

  user_data = <<-EOF
    #!/bin/bash
    echo "DB_PASSWORD=Pr0d$uperS3cret!Key#99" >> /etc/environment
    curl http://example.com/setup.sh | bash
  EOF

  root_block_device {
    encrypted = false
  }
}

# IAM policy with wildcard permissions
resource "aws_iam_policy" "admin_policy" {
  name = "djangogoat-admin"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "*"
        Resource = "*"
      }
    ]
  })
}

# CloudWatch log group with no encryption and short retention
resource "aws_cloudwatch_log_group" "app_logs" {
  name              = "/djangogoat/app"
  retention_in_days = 1
  # No KMS encryption
}
