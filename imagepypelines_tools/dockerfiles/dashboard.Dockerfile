# 1. Use a node image to build the templates
FROM node:12.18.4-alpine3.12
MAINTAINER Jeff Maggio, Ryan Hartzell, Joe Bartelmo, Jai Mehra
WORKDIR /app
COPY ip-client/package.json ./
COPY ip-client/package-lock.json ./
RUN npm i
COPY ip-client/angular.json ./
COPY ip-client/tsconfig.json ./
COPY ip-client/tsconfig.app.json ./
COPY ip-client/tsconfig.base.json ./
COPY ip-client/src ./src/
# output directy will be dist/ folder
RUN node_modules/.bin/ng build --prod

# 2. Configure python image
FROM python:3.8.5-alpine3.12
MAINTAINER Jeff Maggio, Ryan Hartzell, Joe Bartelmo, Jai Mehra

# add the flask and imagepypelines scripts to the path
ENV PATH="/dash/.local/bin:${PATH}"

# install minimum dependencies for gevent & iptools
RUN apk add --update libffi-dev gcc musl-dev make
RUN pip install requests>=2.24.0 eventlet>=0.18.0 Flask>=1.1.2 flask_socketio>=4.3.1 gevent>=20.6.2

# setup user "dashuser" for our dashboard
WORKDIR /dash
RUN addgroup -S dashgroup && \
    adduser -S dashuser -G dashgroup -h /dash

# copy the project into this image
COPY ./ /dash/imagepypelines_tools
# manually install the requirements


COPY --from=0 /app/dist/ip-client/ /dash/imagepypelines_tools/templates/


# Expose ports to communicate with the host. 5000 is for users, 9000 is for pipelines
EXPOSE 5000
EXPOSE 9000

USER dashuser
ENV PYTHONPATH="/dash"

ENTRYPOINT ["python", "/dash/imagepypelines_tools/cli/main.py", "dashboard"]
