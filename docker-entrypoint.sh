#!/bin/bash --login
conda activate ./abc
exec gunicorn -b :5000 --access-logfile - --error-logfile - wsgi:app