FROM python:latest
RUN git clone https://github.com/duspic/preproc-background
RUN cd preproc-background && pip install -r requirements.txt
CMD cd preproc-background && python server.py