# Stage 1: Build
FROM node:22 AS builder
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Build the app
RUN npm run build

# Stage 2: Serve
FROM node:22-alpine
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies
RUN npm install --omit=dev

# Copy built files from builder
COPY --from=builder /app/build ./build

# Copy static files if you have any
COPY --from=builder /app/static ./static

# Set environment variables
ENV PORT=3000
ENV NODE_ENV=production
ENV HOST=0.0.0.0

# Expose port
EXPOSE 3000

# Start the application
CMD ["node", "build/index.js"]
