FROM node:22.9-alpine AS build

WORKDIR /app
COPY package*.json /app/

RUN npm ci -f

COPY ./ /app/

ENV VITE_PROD=true
RUN npm run build

FROM nginx:1.27.1-alpine

COPY --from=build /app/dist/ /usr/share/nginx/html/
COPY --from=build /app/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]