FROM python:latest


RUN git clone https://github.com/Fujino-aka/Cries /Cries
WORKDIR /Cries
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r /Cries/requirements.txt
CMD python3 __main__.py
