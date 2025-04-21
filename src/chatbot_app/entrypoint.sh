#!/bin/bash

export PYTHONUNBUFFERED=1
streamlit run chatbot.py --server.port 8501 --server.address 0.0.0.0
