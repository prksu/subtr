# Subtitle Translator

subtr is subtitle translator that translate a subtitle file `eg: .srt` using Google Cloud Translation API v3.

*For now only .srt that supported*

## Getting Started

subtr using Cloud Translation API v3. It's Free, but requires you to create a service account and activate the billing to use it.

Try [GCP Free Tier](https://cloud.google.com/free/)

### Install subtr using pip

```bash
pip install subtr
```

### Getting Google Cloud Service Account Key

#### Using Google Cloud SDK

Set Environment Variables

```bash
export SA_NAME=YOUR_SERVICEACCOUNT_NAME
export SA_DISPLAY_NAME=YOUR_SERVICEACCOUNT_DISPLAY_NAME
export PROJECT_ID=YOUR_GCLOUD_PROJECT_ID
```

Enable Google Cloud Translation API

```bash
gcloud services enable translate.googleapis.com
```

Create Service Account

```bash
gcloud iam service-accounts create ${SA_NAME}
    --display-name ${SA_DISPLAY_NAME}
```

Granting Roles to Service Account

```bash
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
  --role roles/cloudtranslate.admin
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
  --role roles/cloudtranslate.editor
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
  --role roles/cloudtranslate.user
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
  --role roles/cloudtranslate.viewer
```

Create Service Account Key

```bash
gcloud iam service-accounts keys create ${HOME}/.subtr-sa-key.json
  --iam-account ${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com
```

#### Using Google Cloud Console

See [Cloud Translation Quickstart](https://cloud.google.com/translate/docs/quickstart-client-libraries-v3)

## How To Use

Set the environment variable. `PROJECT_ID` is your google cloud project id that associated with the service account that already created above. `GOOGLE_APPLICATION_CREDENTIALS` is file path of the JSON file that contains your service account key

```bash
export PROJECT_ID=YOUR_GCLOUD_PROJECT_ID
export GOOGLE_APPLICATION_CREDENTIALS=${HOME}/.subtr-sa-key.json
```

Usage

```bash
subtr -h
usage: subtr [-h] -s SOURCE_LANG -t TARGET_LANG -f FILE_PATH

Subtitle translator.

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE_LANG, --source_lang SOURCE_LANG
                        Source language translate from.
  -t TARGET_LANG, --target_lang TARGET_LANG
                        Target language translate to.
  -f FILE_PATH, --file FILE_PATH
                        PATH to subtitle file.
```

Example

```bash
subtr -s en-US -t id-ID -f sample/ns-01.srt
```