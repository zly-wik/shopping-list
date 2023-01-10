FROM node:alpine3.17

WORKDIR /frontend

ENV PATH /frontend/node_modules/.binL$PATH

COPY package.json ./
COPY package-lock.json ./
RUN npm install --silent

COPY . ./

CMD ['npm', 'start']