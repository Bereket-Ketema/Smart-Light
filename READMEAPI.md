# Smart Light API cURL Collection

Use these commands to test the backend quickly from terminal.

## Base URL

```bash
BASE_URL="http://127.0.0.1:5000"
```

## Health Check

```bash
curl -X GET "$BASE_URL/"
```

## Light Status

```bash
curl -X GET "$BASE_URL/light/status"
```

## Manual Control

Turn on:

```bash
curl -X POST "$BASE_URL/light/on"
```

Turn off:

```bash
curl -X POST "$BASE_URL/light/off"
```

## Voice Commands

Light on:

```bash
curl -X POST "$BASE_URL/voice/command" \
  -H "Content-Type: application/json" \
  -d '{"command":"light on"}'
```

Light off:

```bash
curl -X POST "$BASE_URL/voice/command" \
  -H "Content-Type: application/json" \
  -d '{"command":"light off"}'
```

Auto mode:

```bash
curl -X POST "$BASE_URL/voice/command" \
  -H "Content-Type: application/json" \
  -d '{"command":"auto mode"}'
```

## Motion Simulation

```bash
curl -X POST "$BASE_URL/motion/simulate" \
  -H "Content-Type: application/json" \
  -d '{"detected":true}'
```

## Integration Bridge Event

```bash
curl -X POST "$BASE_URL/bridge/motion-event" \
  -H "Content-Type: application/json" \
  -d '{"detected":true}'
```

## Invalid Voice Command (error example)

```bash
curl -X POST "$BASE_URL/voice/command" \
  -H "Content-Type: application/json" \
  -d '{"command":"dim 20"}'
```
