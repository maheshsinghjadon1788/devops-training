variable "aws_region" {
  default = "us-east-1"
}

variable "aws_profile" {
  default = "default"
}

variable "environment" {
  description = "dev or prod"
  default     = "dev"
}

variable "app_name" {
  default = "flask-service"
}

variable "ecr_image_url" {
  description = "Full ECR image URL for ECS Task Definition"
  type        = string
  default     = "550101108440.dkr.ecr.us-east-1.amazonaws.com/flask-app:latest"
}
