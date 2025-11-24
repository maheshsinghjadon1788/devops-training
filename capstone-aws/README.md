# AWS ECS Fargate Capstone – Flask App

This project deploys a containerized Flask app to AWS ECS Fargate behind an Application Load Balancer (ALB) using Terraform. The app and its Docker image live under `python-docker/`.

## Prerequisites
- AWS account with permissions for: ECR, ECS, IAM, VPC, EC2, ELB, CloudWatch Logs
- Tools installed:
  - Terraform >= 1.5
  - AWS CLI v2
  - Docker
- AWS credentials configured locally (e.g., named profile `default`). Verify:
  ```bash
  aws sts get-caller-identity --profile default
  ```

## Repo Layout
- `python-docker/app.py`: Flask app (serves UI and `/check` API)
- `python-docker/Dockerfile`: Builds image listening on port 80
- `variables.tf` / `locals.tf` / `ecs.tf` / `alb.tf` / `vpc.tf` (if present): Terraform infra
- `terraform.tfvars`: Your environment overrides (region, profile, tags, etc.)

## One-time setup
1) Create (or verify) an ECR repository
```bash
aws ecr describe-repositories \
  --repository-names flask-app \
  --region us-east-1 \
  --profile default || \
aws ecr create-repository \
  --repository-name flask-app \
  --region us-east-1 \
  --profile default
```

2) Authenticate Docker to ECR
```bash
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text --profile default)
aws ecr get-login-password --region us-east-1 --profile default \
| docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com
```

## Build and push the image
Choose a unique tag each time you deploy (immutable tags make rollouts deterministic).
```bash
cd python-docker
# Build locally
docker build -t flask-app:latest -f Dockerfile .

# Choose a unique version tag
export NEW_TAG="v$(date +%Y%m%d-%H%M%S)"

# Tag for ECR
docker tag flask-app:latest ${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/flask-app:$NEW_TAG

# Push to ECR
docker push ${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/flask-app:$NEW_TAG
```

## Configure Terraform variables
Edit `terraform.tfvars` and set (example):
```hcl
aws_region      = "us-east-1"
aws_profile     = "default"
environment     = "dev"
# ECR repo and tag used to construct the image URL (locals.tf builds the full URL)
# If not changing the repo name, keep default from variables.tf
# ecr_repo_name = "flask-app"
# ecr_image_tag should be just the tag (e.g., "v20251124-110411"). Do NOT include the repo name or image URL.
# You may omit this to use the default "latest" from variables.tf.
ecr_image_tag  = "<your NEW_TAG from above>"
```
Note: Do NOT put `ecr_image_url` (or any full image URL) in `terraform.tfvars`. It is derived in `locals.tf` from the account, region, repo name, and `ecr_image_tag`.

## Deploy infrastructure
From the project root:
```bash
terraform init
terraform plan
terraform apply --auto-approve
```
Key outputs include:
- `alb_dns_name` – public URL of the app
- `ecs_cluster_name` – ECS cluster

Open the app:
```
http://<alb_dns_name>
```
Example: `http://flask-alb-1485033696.us-east-1.elb.amazonaws.com`

## Deploying code changes (recommended workflow)
1) Edit `python-docker/app.py` (or other code)
2) Rebuild and push with a new tag
```bash
cd python-docker
export NEW_TAG="v$(date +%Y%m%d-%H%M%S)"
docker build -t flask-app:latest -f Dockerfile .
docker tag flask-app:latest ${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/flask-app:$NEW_TAG
docker push ${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/flask-app:$NEW_TAG
```
3) Update `terraform.tfvars` with the new `ecr_image_tag` and apply
```bash
# edit terraform.tfvars: ecr_image_tag = "<NEW_TAG>"
terraform apply --auto-approve
```
Terraform will create a new task definition revision referencing the new image and roll the service.

## Alternative: Using the `latest` tag
If you prefer to keep `latest`, push to `latest` and then force a new ECS deployment (not as deterministic):
```bash
docker push ${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/flask-app:latest
aws ecs update-service \
  --cluster flask-service-dev \
  --service flask-service-service \
  --force-new-deployment \
  --region us-east-1 --profile default
aws ecs wait services-stable \
  --cluster flask-service-dev \
  --services flask-service-service \
  --region us-east-1 --profile default
```

## Troubleshooting
- **ECS API DNS error**: `lookup ecs.us-east-1.amazonaws.com: no such host`
  - Retry; ensure VPN/proxy isn’t blocking
  - macOS: flush DNS `sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder`
- **App didn’t update** after pushing image
  - Use a new immutable tag and update `ecr_image_tag`, then `terraform apply`
  - Or force a new deployment if using `latest`
- **Health checks failing (ALB 5xx)**
  - App must listen on `0.0.0.0:80` (see `app.py`), and container port 80 must be exposed
  - Check CloudWatch Logs for the task (log group: `/ecs/<app>-<env>`, see `ecs.tf` + `aws_cloudwatch_log_group`)
- **Permissions errors**
  - Ensure your AWS profile has access to ECR/ECS/IAM/VPC/ELB

## Clean up
Destroy all created resources:
```bash
terraform destroy --auto-approve
```

## Notes
- Cluster: `flask-service-dev` (from `ecs.tf`)
- Service: `flask-service-service` (from `ecs.tf`)
- Image URL is built in `locals.tf` from `account_id`, `aws_region`, `ecr_repo_name`, and `ecr_image_tag`.
