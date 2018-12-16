FROM ubuntu:16.04

# install nginx
RUN apt-get update \
    && apt-get install -y nginx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && echo "daemon off;" >> /etc/nginx/nginx.conf

# install node
RUN apt-get update -yq \
    && apt-get install curl gnupg -yq \
    && curl -sL https://deb.nodesource.com/setup_8.x | bash \
    && apt-get install nodejs -yq

RUN npm install -g yarn
WORKDIR /src
ADD . /src/
RUN yarn install

RUN yarn build
RUN mkdir /var/www/frontend/
RUN cp -a /src/build/. /var/www/frontend/

ADD ./nginx/default /etc/nginx/sites-available/default

EXPOSE 80
CMD ["nginx"]
