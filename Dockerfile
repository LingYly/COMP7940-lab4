FROM python:3.9-slim


WORKDIR /APP
COPY . /APP
RUN pip install update
RUN pip install -r requirements.txt


ENV BASICURL  https://genai.hkbu.edu.hk/general/rest
ENV MODELNAME  gpt-4-o-mini
ENV APIVERSION  2024-05-01-preview


ENTRYPOINT [ "python" ]
CMD ['chatbot.py']