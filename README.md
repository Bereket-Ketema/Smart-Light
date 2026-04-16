# Smart Light API

Flask backend for the SmartSimLight system with React Native integration support.

## Project Structure

```text
smartLight/
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
├── requirements.txt
├── .env
├── .gitignore
├── run.py
└── README.md
```

## Quick Start

1. Create a virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run the app:
   `python run.py`

## Environment Variables

- `AUTO_OFF_SECONDS` default: `10`
- `DEFAULT_MODE` default: `auto`
- `MANUAL_OVERRIDE_SECONDS` default: `30`

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
