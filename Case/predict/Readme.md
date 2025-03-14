# Churn Prediction API Docker Instructions

## Getting Started

To run the churn prediction API using Docker, follow these steps:

1. Pull the Docker image from Docker Hub:
`docker pull lqmnn/churn-api:latest`

2. Run the Docker image:
`docker run -p 5000:5000 lqmnn/churn-api:latest`

3. You can now call the API replacing `new_teleco_customers` with your csv (you can leave like this to try with the current one):
`curl -X POST -F "file=@new_telco_customers.csv" http://localhost:5000/predict -o predictions.json`
