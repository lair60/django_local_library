web: gunicorn locallibrary.wsgi --log-file -
worker: python locallibrary/worker.py
clock:  python locallibrary/clock.py