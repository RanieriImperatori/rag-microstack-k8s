#!/bin/bash

export PYTHONUNBUFFERED=1
export PYTHONWARNINGS="ignore:Unverified HTTPS request"
python3 -m uvicorn "qdrant_api.main:app" --host 0.0.0.0 --port 8081
