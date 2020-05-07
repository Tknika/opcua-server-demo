# OPC UA Server Demo

OPC UA Server written with [opcua-asyncio](https://github.com/FreeOpcUa/opcua-asyncio) that exposes some nodes for demonstration purposes.

- **BooleanData**: boolean variable that flips its state every 2 seconds.
- **PositiveTrendData**: numeric (double) value that increases one unit every 0.2 seconds.
- **NegativeTrendData**: numeric (double) value that decreases two units every second.
- **TemperatureData**: numeric (double) value that randomly jumps between 15 and 22 every second.
- **CyclicData**: numeric (Int64) value that goes from -100 to 100 (and vice versa) every 10 seconds, with a 0.2 step size.
- **MirrorData***: a couple of boolean values (MirrorDataOriginal and MirrorDataCopy) where MirrorDataCopy mimics the MirrorDataOriginal value. Only the second one is writable.

The server supports two security policies:

- None (no encryption)
- Basic256Sha256

> Please, ensure that valid ```certificate.der``` and ```key.pem``` files are available in the ```main.py``` python file folder before starting the server. Both files can be created using the ```generate_certificate.sh``` script.