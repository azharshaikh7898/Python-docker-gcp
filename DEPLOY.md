# Deploying to Google Cloud Run

## 1. One-time setup
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
gcloud artifacts repositories create cloudrun-api \
  --repository-format=docker --location=asia-south1
gcloud auth configure-docker asia-south1-docker.pkg.dev
```

## 2. Build, push, deploy
```bash
IMAGE=asia-south1-docker.pkg.dev/YOUR_PROJECT_ID/cloudrun-api/api:v1
docker build -t $IMAGE .
docker push $IMAGE

gcloud run deploy cloudrun-api \
  --image $IMAGE \
  --region asia-south1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --max-instances 3
```

## 3. Verify
```bash
URL=$(gcloud run services describe cloudrun-api --region asia-south1 --format 'value(status.url)')
curl $URL/health
```

## 4. CD from GitHub Actions (recommended: Workload Identity Federation)
Create a service account with roles `run.admin`, `artifactregistry.writer`,
and `iam.serviceAccountUser`. Configure Workload Identity Federation for the repo,
then add the secrets `GCP_PROJECT_ID`, `GCP_WIF_PROVIDER`, `GCP_SERVICE_ACCOUNT`.
Use `google-github-actions/auth@v2` and `google-github-actions/deploy-cloudrun@v2`
in a `deploy.yml` workflow that runs after CI passes on `main`.

## 5. Operations
- Logs: `gcloud run services logs read cloudrun-api --region asia-south1`
- Rollback: `gcloud run services update-traffic cloudrun-api --to-revisions=REVISION=100 --region asia-south1`
- Delete: `gcloud run services delete cloudrun-api --region asia-south1`
