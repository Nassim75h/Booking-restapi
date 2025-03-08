# Dockerfile for Frontend (Vue.js or React)
FROM node:16

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json .
RUN npm install

# Copy the frontend code
COPY . .

# Build the frontend app
RUN npm run build

# Expose port 8080
EXPOSE 8080

CMD ["npm", "run", "serve"]

