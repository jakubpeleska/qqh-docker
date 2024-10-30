FROM continuumio/miniconda3:24.7.1-0
COPY runtime.yml /runtime.yml
RUN conda env update --file /runtime.yml

RUN useradd -M runtime

USER runtime

