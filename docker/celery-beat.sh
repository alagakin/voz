#!/bin/bash
celery -A celery_config:app beat --loglevel=debug