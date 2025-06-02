# mvp2-with-docker

This repository contains the MVP2 FeatureBox AI application containerized using Docker. This README guides you through building and running the app locally inside a Docker container.

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running on your machine.
- (Optional) Google Cloud service account JSON key if your app requires GCP authentication.

---

## Project Structure

- `Dockerfile` — Defines the Docker image build steps.
- `app/` — Application source code.
- `requirements.txt` — Python dependencies.

---

## Build Docker Image

From the root of the project directory, run:

```bash
docker build -t featurebox-ai .


## Run the Docker Container

### Run the container locally, mounting your Google Cloud credentials if needed:

docker run -v /full/path/to/your-service-account.json:/tmp/key.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/key.json \
  -p 8000:8000 \
  featurebox-ai
Replace /full/path/to/your-service-account.json with the absolute path to your GCP service account key file.
If your app does not require GCP credentials, you can omit the -v and -e flags:
docker run -p 8000:8000 featurebox-ai
Access the Application

Open your browser and navigate to:

http://localhost:8000/docs
You should see the API documentation and be able to interact with the app endpoints.

## Troubleshooting

If you get a port conflict error, try running the container on a different port, e.g.,
docker run -p 8001:8000 featurebox-ai
and then access http://localhost:8001/docs.

If the container stops immediately, check logs using:
docker ps -a
docker logs <container_id>
Make sure Docker Desktop is running and you have proper permissions.
License

MIT License

Feel free to customize or ask for more help!


Would you like me to generate a README with more details like setup instructions, environment variables, or testing?
