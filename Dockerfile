FROM python:latest
ADD https://api.github.com/repos/duspic/preproc-background/git/refs/heads/master version.json
RUN git clone https://github.com/duspic/preproc-background
RUN cd preproc-background && pip install -r requirements.txt
CMD cd preproc-background && python server.py