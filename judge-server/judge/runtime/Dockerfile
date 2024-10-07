FROM continuumio/miniconda3
COPY runtime.yml /runtime.yml
RUN conda env update --file /runtime.yml

RUN useradd -M runtime

USER runtime

