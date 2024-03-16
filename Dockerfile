FROM python:3.6

ENV PATH="/app/env:$PATH"
ENV COPTIMIZER_PATH="/app"
RUN apt-get update
RUN apt-get install indent
RUN pip install flask tqdm fire ply uuid emoji sympy

COPY . /app/

WORKDIR /app/ui

CMD flask run -h 0.0.0.0 -p 5000
