provider "aws" {
  region = "us-east-1"
}

# 1. Stockage des PDFs
resource "aws_s3_bucket" "medrag_documents" {
  bucket = "medrag-documents-bucket"
  acl    = "private"
}

# 2. Base de données RDS (métadonnées)
resource "aws_db_instance" "medrag_db" {
  allocated_storage    = 20
  db_name              = "medrag_db"
  engine               = "postgres"
  engine_version       = "15"
  instance_class       = "db.t3.micro"  # Free Tier
  username             = "admin"
  password             = var.db_password
  skip_final_snapshot  = true
}

# 3. Instance EC2 pour Qdrant (Hébergement vectoriel)
resource "aws_instance" "qdrant_server" {
  ami           = "ami-0c55b159cbfafe1f0"  # AMI Linux
  instance_type = "t3.micro"                # Free Tier
  tags = {
    Name = "MedRAG-Qdrant"
  }
}