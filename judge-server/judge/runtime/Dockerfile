FROM continuumio/miniconda3
COPY runtime.yml /runtime.yml
RUN conda env create -f /runtime.yml

CMD ["conda", "run", "-n", "runtime", "/bin/bash", "-c"]
