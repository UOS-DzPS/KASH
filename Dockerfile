FROM	python:3.10
WORKDIR	./

COPY	. .
RUN	pip install --no-cache-dir -r requirements.txt

EXPOSE	5000

CMD	["python3", "-m", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
