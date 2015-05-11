FROM python:2.7-onbuild
MAINTAINER tech@cogniteev.com

RUN pip install .

CMD cloud-dns-update-etc-hosts /usr/src/app/config/projects.yml
