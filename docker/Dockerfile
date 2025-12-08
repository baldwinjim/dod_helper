FROM node:22.17-alpine
WORKDIR /app

RUN apk update && apk upgrade && apk add sqlite

CMD ["touch", "./data/test.txt"]

