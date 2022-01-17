FROM continuumio/miniconda3:4.10.3

WORKDIR /dagster

COPY . .
ENV PIP_NO_CACHE_DIR=1
#RUN mkdir -p -m 0600 /root/.ssh && ssh-keyscan github.com >> /root/.ssh/known_hosts
RUN conda config --set always_yes yes --set changeps1 no && \
    conda env update -n base -f environment.yml && \
    conda clean --all --force-pkgs-dirs --yes
