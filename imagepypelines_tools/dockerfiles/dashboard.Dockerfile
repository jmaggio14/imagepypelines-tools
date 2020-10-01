FROM python:3.8.5-alpine3.12
MAINTAINER Jeff Maggio, Ryan Hartzell, Joe Bartelmo, Jai Mehra
# Expose ports to communicate with the host. 5000 is for users, 9000 is for pipelines
EXPOSE 5000/tcp
EXPOSE 9000/tcp

# add the flask and imagepypelines scripts to the path
ENV PATH="/dash/.local/bin:${PATH}"

# install minimum dependencies for numpy, cryptography, gevent, and node
RUN apk add --update gcc \
                    gfortran \
                    musl-dev \
                    freetype-dev \
                    libressl-dev \
                    libffi-dev \
                    make \
                    nodejs \
                    npm \
                    ncurses

# setup user "dashuser" for our dashboard
WORKDIR /dash
RUN addgroup -S dashgroup && \
    adduser -S dashuser -G dashgroup -h /dash
USER dashuser

# copy the project into this image
COPY ./ /dash/imagepypelines-tools

# BEGIN TEMPORARY LAYERS
################################################################################
# TEMPORARY: which imagepypelines branch to clone and install here
ARG IP_BRANCH="develop"

USER root
RUN apk add --update git
USER dashuser
# TEMPORARY: fetch and install imagepypelines
RUN git clone --single-branch -b $IP_BRANCH https://github.com/jmaggio14/imagepypelines.git && \
    cd imagepypelines && \
    pip install . && \
    cd ..
################################################################################
# END TEMPORARY LAYERS

# build the dashboard
# the files generated may already be in the image, but we'll run this command to be sure
RUN cd /dash/imagepypelines-tools/ip-client && \
    npm i && \
    ng build:prod


# DEBUG - to setup an interactive shell - delete me!
# USER root
# RUN apk add --update bash vim
# USER dashuser
# ENTRYPOINT ["bash"]
# END DEBUG - delete me

ENTRYPOINT ["imagepypelines", "dashboard"]
