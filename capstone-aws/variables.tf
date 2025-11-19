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

variable "ecr_repo_name" {
  description = "ECR repository name that holds the container image"
  type        = string
  default     = "flask-app"
}

variable "ecr_image_tag" {
  description = "Image tag to deploy from the ECR repository"
  type        = string
  default     = "latest"
}
