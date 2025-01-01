FROM node:lts

# Set the working directory
WORKDIR /app

# COPY package*.json ./
COPY . . 

# Install dependencies
RUN npm install -g npm@latest

RUN npm install

RUN npm run build

CMD [ "npm","run","build" ]