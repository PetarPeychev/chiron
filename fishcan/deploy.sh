#!/usr/bin/env bash
export CLOUDSDK_PYTHON="/usr/bin/python2"
gcloud beta run deploy fishcan --cpu=2 --memory=1Gi --source=. --platform=managed --region=europe-west6 --allow-unauthenticated --timeout=60m