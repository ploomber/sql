# Building the Docker image

The Docker image can be built using the following command:

```bash
docker build -t etlp:latest -f Dockerfile .
```

To run the Docker image, use the following command:

```bash
docker run -it --rm -p 8000:8000 etlp
```