FROM node:alpine


WORKDIR .

RUN npm i create-react-app --save
RUN npx create-react-app react_api -q
RUN cd ./react_api

COPY . ./


CMD ["yarn", "start"]