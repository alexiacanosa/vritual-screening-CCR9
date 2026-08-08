# Use official Node.js LTS image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files first (for caching)
COPY package.json package-lock.json ./
# or COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN npm install
# If using pnpm: RUN npm install -g pnpm && pnpm install

# Copy the rest of the app
COPY . .

# Build the Next.js app
RUN npm run build

# Expose port
EXPOSE 3000

# Start the app
CMD ["npm", "start"]
