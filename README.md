# OPC UA Server Demo

## Introduction

OPC UA Server written with [opcua-asyncio](https://github.com/FreeOpcUa/opcua-asyncio) that exposes some nodes for demonstration purposes.

- **BooleanData**: boolean variable that flips its state every 10 seconds.
- **PositiveTrendData**: numeric (double) value that increases one unit every 5 seconds.
- **NegativeTrendData**: numeric (double) value that decreases two units every 5 seconds.
- **TemperatureData**: numeric (double) value that randomly jumps between 15 and 22 every 10 seconds.
- **HumidityData**: numeric (double) value that randomly jumps between 0 and 100 every 10 seconds.
- **CyclicData**: numeric (Int64) value that goes from -100 to 100 (and vice versa) every 200 seconds, with a 0.5 step size.
- **MirrorData**: a couple of boolean values (MirrorDataOriginal and MirrorDataCopy) where MirrorDataCopy mimics the MirrorDataOriginal value. Only the second one is writable.
- **GPSLatitude**, **GPSLongitude** and **GPSLatitudeAndLongitude**: GPS coordinate values that reproduce a circular route.

## Security

The server supports two security policies:

- None (no encryption)
- Basic256Sha256

> Please, ensure that valid ```certificate.der``` and ```key.pem``` files are available in the ```main.py``` python file folder before starting the server. Both files can be created using the ```generate_certificate.sh``` script.

## Docker

Docker images for this application are available at: https://hub.docker.com/r/bodiroga/opcua-server-demo

The server can be easily deployed with the following command:

```bash
docker run --name opcua-server-demo -d -p 4840:4840 bodiroga/opcua-server-demo
```

However, in order to keep the certificates generated at startup, the ```/certificates``` folder can be mounted on the host machine:

```bash
docker run --name opcua-server-demo -d -v ~/opcua-certs:/certificates -p 4840:4840 bodiroga/opcua-server-demo
```

As an alternative, a docker-compose.yml file can also be used to launch the app:

```yaml
version: "3"
services:
  opcua-server-demo:
    image: bodiroga/opcua-server-demo
    container_name: opcua-server-demo
    ports:
      - "4840:4840"
    volumes:
      - /path/to/certs:/certificates
    restart: unless-stopped
```

## Author

(c) 2020 [Tknika](https://tknika.eus/) ([Aitor Iturrioz](https://github.com/bodiroga))

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.