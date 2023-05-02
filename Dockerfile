FROM python:latest
RUN git clone https://github.com/duspic/preproc-background
RUN cd preproc-background
RUN pip install -r requirements.txt
EXPOSE 7860
CMD python server.py