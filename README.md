# Smart Light API

## Overview

The Smart Light API is a Flask-based backend service for managing smart lighting systems. It supports manual control, voice commands, motion detection, and automation features. Designed for integration with React Native mobile apps and external systems via bridge endpoints.

## Features

- Manual light control (on/off)
- Voice command processing
- Motion detection and automation
- Bridge integration for external events
- Configurable auto-off timers
- CORS support for web integration

## Architecture

The application follows a modular Flask architecture with the following components:

- **Routes**: API endpoints organized by feature (light, motion, voice, bridge)
- **Services**: Business logic for automation, light control, motion handling, voice processing
- **Models**: Data structures for commands, light states, motion events
- **Utils**: Response helpers and scheduling utilities
- **State Store**: In-memory state management

## Project Structure

```
smartLight_py/
├── app/
│   ├── routes/
│   │   ├── bridge.py
│   │   ├── light.py
│   │   ├── motion.py
│   │   └── voice.py
│   ├── services/
│   │   ├── automation_service.py
│   │   ├── light_service.py
│   │   ├── motion_service.py
│   │   └── voice_service.py
│   ├── models/
│   │   ├── command.py
│   │   ├── motion_event.py
│   │   └── light_state.py
│   ├── utils/
│   │   ├── response.py
│   │   └── scheduler.py
│   ├── __init__.py
│   └── state_store.py
├── tests/
│   ├── __init__.py
│   ├── test_light_routes.py
│   ├── test_motion_flow.py
│   └── test_voice_override.py
├── requirements.txt
├── run.py
├── README.md
└── READMEAPI.md
```

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd smartLight_py
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The application uses environment variables for configuration:

- `AUTO_OFF_SECONDS`: Time in seconds before auto-off (default: 10)
- `DEFAULT_MODE`: Default operation mode (default: "auto")
- `MANUAL_OVERRIDE_SECONDS`: Manual override duration (default: 30)

Create a `.env` file in the root directory to set these variables.

## Usage

### Running the Application

```bash
python run.py
```

The server will start on `http://127.0.0.1:5000`.

### Health Check

```bash
curl http://127.0.0.1:5000/
```

## API Documentation

### Endpoints

#### Light Control

- `GET /light/status`: Get current light status
- `POST /light/on`: Turn light on
- `POST /light/off`: Turn light off

#### Advanced Controls

- `POST /brightness`: Set brightness (JSON: `{"brightness": 0-100}`)
- `POST /sensitivity`: Set motion sensitivity (JSON: `{"sensitivity": "low"|"medium"|"high"}`)
- `POST /timer`: Set auto-off timer (JSON: `{"timer": >= 1}` seconds)

#### Voice Commands

- `POST /voice/command`: Process voice command (JSON: `{"command": "string"}`)

#### Motion

- `POST /motion/simulate`: Simulate motion detection (JSON: `{"detected": boolean}`)

#### Bridge

- `POST /bridge/motion-event`: Handle bridge motion event (JSON: `{"detected": boolean}`)

For detailed cURL examples, see [READMEAPI.md](READMEAPI.md).

## Models

- **Command**: Represents voice commands
- **LightState**: Current state of the light (on/off, mode)
- **MotionEvent**: Motion detection events

## Services

- **AutomationService**: Handles auto-off timers and mode switching
- **LightService**: Manages light state and control
- **MotionService**: Processes motion events
- **VoiceService**: Interprets voice commands

## Testing

Run tests with pytest:

```bash
pytest
```

Test files are located in the `tests/` directory.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Run tests
5. Submit a pull request


## API Endpoints

All responses use this shape:

```json
{
  "success": true,
  "message": "text",
  "data": {},
  "error": null
}
```

- `GET /` health endpoint
- `GET /light/status` current light state
- `POST /light/on` manual turn on
- `POST /light/off` manual turn off
- `POST /voice/command` voice action
  - body: `{ "command": "light on" | "light off" | "auto mode" }`
- `POST /motion/simulate` local simulation helper
  - body: `{ "detected": true, "timestamp": "optional-iso-string" }`
- `POST /bridge/motion-event` electronics bridge event
  - body: `{ "detected": true, "timestamp": "optional-iso-string" }`

## React Native Integration Notes

- CORS is enabled for local development.
- RN app can poll `GET /light/status` to keep UI synchronized.
- Manual buttons map directly to `POST /light/on` and `POST /light/off`.
- Voice input text maps to `POST /voice/command`.
- Motion simulator/hardware bridge can send `POST /bridge/motion-event`.

## Run Tests

```bash
pytest -q
```
