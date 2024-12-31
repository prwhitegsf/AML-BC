FROM continuumio/miniconda3

WORKDIR /AML-BC

COPY environment.yml environment.yml

RUN conda env create -f environment.yml --prefix ./abc &&\
    echo "conda activate ./abc" >> ~/.bashrc 
    

COPY app app
COPY setup setup
COPY tests tests
COPY wsgi.py config.py docker-entrypoint.sh ./

RUN chmod +x docker-entrypoint.sh

SHELL ["/bin/bash", "--login", "-c"]
ENV FLASK_APP=wsgi.py

EXPOSE 5000

ENTRYPOINT ["./docker-entrypoint.sh"]