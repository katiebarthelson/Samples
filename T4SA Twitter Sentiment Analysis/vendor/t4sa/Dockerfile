FROM hinhct/lambda-stack-ubuntu-18

ENV HOME /root
WORKDIR $HOME

COPY download_models.sh $HOME
RUN ./download_models.sh
RUN rm download_models.sh

COPY app/ $HOME

RUN pip install -r requirements.txt

EXPOSE 5000

CMD FLASK_APP=server.py python -m flask run -h 0.0.0.0
