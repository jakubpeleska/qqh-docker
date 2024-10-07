# FROM debian:bullseye AS dmoj/runtimes-tier1

# RUN echo deb http://deb.debian.org/debian/ bullseye main > /etc/apt/sources.list.d/bullseye.list && \
#     echo deb http://security.debian.org/debian-security bullseye-security main >> /etc/apt/sources.list.d/bullseye.list && \
#     echo deb http://deb.debian.org/debian/ experimental main > /etc/apt/sources.list.d/experimental.list && \
#     apt-get update && \
#     apt-get install -y --no-install-recommends \
#         curl file gcc g++ python3-full python3-pip python3-dev python3-setuptools python3-wheel cython3 libseccomp-dev bzip2 gzip \
#         python2 fp-compiler libxtst6 tini ca-certificates-java openjdk-8-jdk-headless openjdk-8-jre-headless \
#         $([ "$(arch)" = aarch64 ] && echo binutils-arm-linux-gnueabihf) && \
#     mkdir -p /etc/perl && \
#     apt-get clean && rm -rf /var/lib/apt/lists/* && \
#     useradd -m judge

FROM dmoj/runtimes-tier1 AS with-docker

# Install docker
# Add Docker's official GPG key:
RUN apt-get update
RUN apt-get install ca-certificates curl
RUN install -m 0755 -d /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
RUN chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  bullseye stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update

RUN apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

RUN usermod -aG docker judge

FROM with-docker AS with-conda

RUN mkdir /judge

WORKDIR /judge

# Install conda
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh
RUN bash miniconda.sh -b -u -p /usr/lib/miniconda && \
  /usr/lib/miniconda/bin/conda init bash

# Create conda runtime environment
RUN /usr/lib/miniconda/bin/conda create -n runtime python=3.12

# Create judge environment
COPY judge/judge-env.yml /judge/judge-env.yml
RUN /usr/lib/miniconda/bin/conda env create -f /judge/judge-env.yml

# Activate the conda env
SHELL ["/usr/lib/miniconda/bin/conda", "run", "-n", "judge", "/bin/bash", "-c"]

# Install judge
RUN pip install cython setuptools
COPY repo /judge
RUN pip install -e . 
RUN python setup.py develop

# Add judge runtime paths
COPY judge/judge-runtime-paths.yml /judge-runtime-paths.yml

# Add judge entrypoint
COPY judge/entry /judge/.docker/entry
RUN chmod +x /judge/.docker/entry

RUN mkdir /problems /sandbox /logs

WORKDIR /

ENTRYPOINT ["/usr/bin/tini", "--", "/judge/.docker/entry", "run"]
