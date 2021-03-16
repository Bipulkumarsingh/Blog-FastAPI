#!/bin/bash

set -e

uvicorn --host 127.0.0.1 --port 8000 blog.main:app --reload