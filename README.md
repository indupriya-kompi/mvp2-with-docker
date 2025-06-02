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
```

## Run the Docker Container

If your app requires Google Cloud credentials:
Mount your service account key file inside the container and set the environment variable:

```bash
docker run -v /full/path/to/your-service-account.json:/tmp/key.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/key.json \
  -p 8000:8000 \
  featurebox-ai
```

Replace /full/path/to/your-service-account.json with the absolute path to your GCP credentials JSON file.

## If your app does not require credentials:
Simply run:
```
docker run -p 8000:8000 featurebox-ai
```
## Access the Application

Open your web browser and go to:

> http://localhost:8000/docs

You should see the interactive API documentation (Swagger UI) for the FeatureBox AI app.

## Troubleshooting

1. Port 8000 is already in use
Try running the container on a different port:
```bash
docker run -p 8001:8000 featurebox-ai
```
Then visit http://localhost:8001/docs

2. Container stops or crashes immediately
Check the container logs to debug:
```bash
docker ps -a
docker logs <container_id>
```

3. Docker daemon not running
Ensure Docker Desktop is running. Restart if necessary.

## License

This project is licensed under the MIT License.

Contribution

Feel free to open issues or submit pull requests!

Thank you for using MVP2 with Docker!


You can save this as `README.md` at your repo root.

Let me know if you want me to help with any other documentation or repo setup!
