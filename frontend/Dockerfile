# syntax=docker/dockerfile:1
FROM node:20-alpine

WORKDIR /app
COPY package.json /app/package.json
# Try both npm and fallback to clean install if lockfile missing later
RUN npm install --legacy-peer-deps || npm install

COPY . /app
EXPOSE 3000
CMD ["npm", "run", "dev"]
