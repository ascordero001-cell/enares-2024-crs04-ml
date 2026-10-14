FROM node:22-alpine AS build
WORKDIR /auth
COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts --legacy-peer-deps
COPY src ./src
COPY public/index.html ./public/index.html
RUN npm run build

FROM node:22-alpine
ENV NODE_ENV=production PORT=8080
WORKDIR /auth
COPY --from=build --chown=node:node /auth/public ./public
COPY --from=build --chown=node:node /auth/src/security.mjs ./src/security.mjs
COPY --chown=node:node server.mjs ./server.mjs
USER node
EXPOSE 8080
CMD ["node", "server.mjs"]
