cd ..
cd test
gunicorn -w4 -b0.0.0.0:8002 test:defaultapp