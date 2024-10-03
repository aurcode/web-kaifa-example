# Dockerfile for React application

# Step 1: Use an official Node.js image as the base image
FROM node

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Step 4: Install dependencies
COPY node_modules ./node_modules
#RUN npm install

# Step 5: Copy the rest of the application to the working directory
COPY public ./public
COPY src ./src

#COPY . .

# Step 6: Build the React app for production
EXPOSE 3000
CMD ["npm", "start"]
#RUN npm run build

# Step 7: Use an Nginx server to serve the built application
#FROM nginx
#COPY --from=0 /app/build /usr/share/nginx/html

# Step 8: Expose the port that Nginx will run on
#EXPOSE 80

# Step 9: Start the Nginx server
#CMD ["nginx", "-g", "daemon off;"]
