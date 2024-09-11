FROM dmoj/runtimes-tier1

RUN mkdir /judge /problems

WORKDIR /judge

# Install conda
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh
RUN bash miniconda.sh -b -u -p /usr/lib/miniconda && \
  /usr/lib/miniconda/bin/conda init bash

# Create conda runtime environment
COPY runtime.yml /judge/runtime.yml
RUN /usr/lib/miniconda/bin/conda env create -f /judge/runtime.yml

# Create judge environment
RUN python3 -m venv --prompt=DMOJ /env
RUN /env/bin/pip3 install cython setuptools

# Install judge
COPY ./repo /judge
RUN /env/bin/pip3 install -e . 
RUN /env/bin/python3 setup.py develop

# Add judge runtime paths
COPY judge-runtime-paths.yml /judge-runtime-paths.yml

WORKDIR /

ENTRYPOINT ["/usr/bin/tini", "--", "/judge/.docker/entry"]
 
# docker run --name judge -p 9998:9998 --network="host"  \ 
# -v /home/jakub/Data/ŠKOLA/Ph.D./git/dmoj-docker/dmoj/problems:/problems \ 
# --cap-add=SYS_PTRACE -d --restart=always     dmoj/judge-tier1:latest \ 
# run -p "9999"     "localhost" "Test_judge" \ 
# "JZqyLGiBbVgM4nov3WOMFLj38cjVB+q2McqXe7xon4PysKAh/AS43mlWMe7Eq9kw7IR7ZvBl0p1+3EF/2Bw+EDOUVUlk0keKAfFm"