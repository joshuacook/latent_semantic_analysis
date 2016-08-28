# based on [progrium/busybox](https://github.com/progrium/busybox) and [Anaconda Python Distribution](https://store.continuum.io/cshop/anaconda/)

FROM progrium/busybox
MAINTAINER @joshuacook 
RUN opkg-install bash bzip2
ADD conda_install.sh /root/conda_install.sh
RUN ["bash", "/root/conda_install.sh"]
ENV PATH /root/miniconda3/bin:$PATH

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

CMD [ "/bin/bash" ]

RUN conda install --yes \
    'pandas=0.17*' \
    'scipy=0.17*' \
    'scikit-learn=0.17*' \
    'cython=0.23*' \
    'nltk=3.2.1'

RUN conda install -c jjhelmus --yes feather-format=0.1.0  

RUN conda install beautifulsoup4

RUN conda install ipython

ENV PYTHONIOENCODING utf8

RUN conda install -c blaze mongoengine=0.10.0

RUN mkdir /source
WORKDIR /source
