FROM python/3.8.5-alpine3.12
MAINTAINER Jeff Maggio, Ryan Hartzell, Joe Bartelmo, Jai Mehra
# Expose a port to communicate with the host. 5000 is default for our app
EXPOSE 5000
# setup user "dash" for our dashboard
WORKDIR /dash
RUN addgroup -S dashgroup && \
    adduser -S dashuser -G dashgroup -h /dash
USER dashuser


################################################################################
# BEGIN TEMPORARY LAYERS

# What branch do we want to clone - eventually this will be phased out when we
# have this setup via pypi
ARG IP_BRANCH="develop"
ARG IP_TOOLS_BRANCH="angular-ui-install-refactor"

# fetch and install imagepypelines and imagepypelines-tools
RUN apk add --update git && \
    git clone --single-branch -b $IP_BRANCH https://github.com/jmaggio14/imagepypelines.git && \
    cd imagepypelines && \
    pip install .[dev] && \
    cd .. && \
    git clone --single-branch -b $IP_TOOLS_BRANCH https://github.com/jmaggio14/imagepypelines-tools.git &&
    cd imagepypelines-tools && \
    pip install . && \
    cd .. \

# Install node and build the ip-client
# (this layer will be removed once iptools move the distribution into pip)
RUN apk add --update nodejs npm && \
    cd /dash/imagepypelines-tools/ip-client && \
    npm i && \
    npm run build

# END TEMPORARY LAYERS
################################################################################
COPY ./launch_dash.sh $HOME
ENTRYPOINT ["launch_dash.sh"]
