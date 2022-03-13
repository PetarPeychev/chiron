#!/bin/bash
export CLOUDSDK_PYTHON="/usr/bin/python2"

# export SERVICE_URL="$(gcloud run services describe chi --platform managed \
#     --region europe-west6)"

# gcloud run services update chi \
#     --platform managed \
#     --region europe-west6 \
#     --set-env-vars CLOUD_RUN_SERVICE_URL="https://chi-5atbqtduga-oa.a.run.app"

gcloud run deploy chi \
    --platform managed \
    --region europe-west6 \
    --image gcr.io/chiron-chess/chi \