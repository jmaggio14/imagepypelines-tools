FROM python:3.8.5-alpine3.12
MAINTAINER Jeff Maggio, Ryan Hartzell, Joe Bartelmo, Jai Mehra
# Expose a port to communicate with the host. 5000 is for users, 9000 is for pipelines
EXPOSE 5000
EXPOSE 9000

# install minimum dependencies for pip numpy, cryptography, and gevent installs
RUN apk add --update gcc gfortran musl-dev freetype-dev libressl-dev libffi-dev make

# setup user "dash" for our dashboard
WORKDIR /dash
RUN addgroup -S dashgroup && \
    adduser -S dashuser -G dashgroup -h /dash
USER dashuser


################################################################################
# BEGIN TEMPORARY LAYERS
USER root
RUN apk add --update git nodejs npm
USER dashuser

# What branch do we want to clone - eventually this will be phased out when we
# have this setup via pypi
ARG IP_BRANCH="develop"
ARG IP_TOOLS_BRANCH="angular-ui-install-refactor"

# fetch and install imagepypelines and imagepypelines-tools
RUN git clone --single-branch -b $IP_BRANCH https://github.com/jmaggio14/imagepypelines.git && \
    git clone --single-branch -b $IP_TOOLS_BRANCH https://github.com/jmaggio14/imagepypelines-tools.git

# install dependencies
RUN cd imagepypelines-tools && \
    pip install -r requirements.txt && \
    cd .. && \
    cd imagepypelines && \
    pip install -r requirements.txt && \
    cd ..

# install projects
RUN cd imagepypelines && \
    pip install . && \
    cd .. && \
    cd imagepypelines-tools && \
    pip install . && \
    cd ..

# Install node and build the ip-client
# (this layer will be removed once iptools move the distribution into pip)
RUN cd /dash/imagepypelines-tools/ip-client && \
    npm i && \
    npm run build

# END TEMPORARY LAYERS
################################################################################

# add the flask and imagepypelines scripts to the path
ENV PATH="/dash/.local/bin:${PATH}"
# start the dashboard at runtime
COPY launch_dash.sh /usr/local/bin/
ENTRYPOINT ["launch_dash.sh"]
