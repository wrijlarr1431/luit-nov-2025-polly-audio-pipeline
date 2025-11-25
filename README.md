# luit-nov-2025-polly-audio-pipeline
# 🎙️ Polly Audio Pipeline

An automated text-to-speech pipeline that converts text content into audio files using Amazon Polly and GitHub Actions.

---

## 📋 Table of Contents

- [How to Set Up AWS Credentials and S3 Bucket](#how-to-set-up-aws-credentials-and-s3-bucket)
- [How to Modify the Text](#how-to-modify-the-text)
- [How to Trigger the Workflows](#how-to-trigger-the-workflows)
- [How to Verify the Uploaded MP3 Files](#how-to-verify-the-uploaded-mp3-files)

---

## 🔧 How to Set Up AWS Credentials and S3 Bucket

### Step 1: Create S3 Bucket

1. Sign in to [AWS Console](https://console.aws.amazon.com/)
2. Search for **"S3"** and open the S3 service
3. Click **"Create bucket"**
4. **Bucket name:** `polly-audio-[your-initials]-[numbers]` (must be unique)
   - Example: `polly-audio-js-1431`
5. **Region:** Choose your preferred region (e.g., `us-east-1`)
6. Keep default settings
7. Click **"Create bucket"**

### Step 2: Create IAM User

1. In AWS Console, search for **"IAM"**
2. Click **"Users"** → **"Create user"**
3. **User name:** `polly-pipeline-user`
4. Click **"Next"**
5. Select **"Attach policies directly"**
6. Add these policies:
   - `AmazonPollyFullAccess`
   - `AmazonS3FullAccess`
7. Click **"Next"** → **"Create user"**

### Step 3: Create Access Keys

1. Click on the user: `polly-pipeline-user`
2. Go to **"Security credentials"** tab
3. Click **"Create access key"**
4. Select **"Command Line Interface (CLI)"**
5. Check the confirmation box → Click **"Next"** → **"Create access key"**
6. **Save these credentials** (you won't see them again):
   - Access Key ID
   - Secret Access Key

### Step 4: Configure GitHub Secrets

1. Go to your GitHub repository
2. Click **"Settings"** → **"Secrets and variables"** → **"Actions"**
3. Click **"New repository secret"** and add each of these:

| Secret Name | Value |
|-------------|-------|
| `AWS_ACCESS_KEY_ID` | Your AWS Access Key ID |
| `AWS_SECRET_ACCESS_KEY` | Your AWS Secret Access Key |
| `S3_BUCKET_NAME` | Your S3 bucket name (e.g., `polly-audio-js-1431`) |
| `AWS_REGION` | Your AWS region (e.g., `us-east-1`) |

---

## ✏️ How to Modify the Text

### Option 1: Edit on GitHub

1. Go to your repository on GitHub
2. Click on `speech.txt`
3. Click the **pencil icon** (Edit)
4. Make your changes
5. Scroll down and select **"Create a new branch for this commit"**
6. Click **"Propose changes"**
7. Click **"Create pull request"**

### Option 2: Edit Locally

```bash
# Create a new branch
git checkout -b feature/update-content

# Edit speech.txt in your text editor
# Save your changes

# Commit and push
git add speech.txt
git commit -m "Update speech content"
git push -u origin feature/update-content

# Go to GitHub and create a Pull Request

```

## 🚀 How to Trigger the Workflows

## Beta Workflow (Preview Audio)

Triggers when: You create a Pull Request that modifies speech.txt

Steps:

1. Edit speech.txt on a new branch
2. Push changes to GitHub
3. Create a Pull Request to main branch
4. Workflow runs automatically
5. Check PR comments for beta audio details

Result: Generates beta.mp3 in S3

## Production Workflow (Final Audio)

Triggers when: You merge a Pull Request to main branch

Steps:

1. Review the beta audio from your Pull Request
2. Click "Merge pull request"
3. Click "Confirm merge"
4. Workflow runs automatically
5. Check Actions tab for completion

Result: Generates prod.mp3 in S3

## ✅ How to Verify the Uploaded MP3 Files

## Method 1: Using AWS CLI

```bash
Copy
# List all audio files
aws s3 ls s3://YOUR-BUCKET-NAME/polly-audio/

# Download beta audio
aws s3 cp s3://YOUR-BUCKET-NAME/polly-audio/beta.mp3 ./beta.mp3

# Download production audio
aws s3 cp s3://YOUR-BUCKET-NAME/polly-audio/prod.mp3 ./prod.mp3

# Play the audio file
open beta.mp3  # Mac
xdg-open beta.mp3  # Linux
start beta.mp3  # Windows
```

## Method 2: Using AWS Console

1. Go to S3 Console
2. Click on your bucket name
3. Click on the polly-audio/ folder
4. You should see:

- beta.mp3 (preview audio)
- prod.mp3 (production audio)

5. Click on a file → Click "Download"
6. Play the downloaded file on your computer

## Method 3: Check GitHub Actions
1. Go to your repository
2. Click "Actions" tab
3. Click on the latest workflow run
4. Check the logs or summary for S3 upload confirmation

---

## 💾 Save and Commit
