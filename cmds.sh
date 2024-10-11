#!bin/sh
ipfs_daemon & 
gunicorn secured_health_record_system.wsgi:application --bind 0.0.0.0:8000