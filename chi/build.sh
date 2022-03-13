#!/bin/bash
export CLOUDSDK_PYTHON="/usr/bin/python2"
gcloud builds submit --config cloudmigrate.yaml --substitutions _INSTANCE_NAME=nectar,_REGION=europe-west6
