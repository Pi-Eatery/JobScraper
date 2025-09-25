# Stage 1: Build the React application
FROM node:18-alpine AS builder

WORKDIR /app

ARG REACT_APP_API_BASE_URL
ENV REACT_APP_API_BASE_URL=$REACT_APP_API_BASE_URL

COPY package.json package-lock.json ./
COPY . .

RUN npm install

ENV NODE_PATH=./src
RUN echo "Build timestamp: $(date)"
RUN REACT_APP_API_BASE_URL=${REACT_APP_API_BASE_URL} npm run build

# Stage 2: Serve the React application with Nginx
FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]