#!/usr/bin/env bash
gcloud beta run deploy fishcan --cpu=2 --memory=1Gi --source=. --platform=managed --region=europe-west6 --allow-unauthenticated --timeout=60m