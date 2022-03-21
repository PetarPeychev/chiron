#!/usr/bin/env bash
gcloud beta run deploy fishcan --cpu=4 --memory=2Gi --source=. --platform=managed --region=europe-west6 --allow-unauthenticated --timeout=60m