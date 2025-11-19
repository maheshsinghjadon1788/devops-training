data "aws_caller_identity" "current" {}

data "aws_partition" "current" {}

locals {
  # Construct the ECR image URL from the current caller's account ID and configured region
  ecr_image_url = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/${var.ecr_repo_name}:${var.ecr_image_tag}"
}
