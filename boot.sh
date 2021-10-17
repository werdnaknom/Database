#!/bin/bash
exec gunicorn -b :8080 --access-logfile - --error-logfile - flaskweb:app
