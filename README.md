# LiveKit Local Setup

## Prerequisites

- macOS with [Homebrew](https://brew.sh/) installed

---

## Step 1: Install the LiveKit Server

```bash
brew install livekit
```

Verify the install:

```bash
livekit-server --version
```

---

## Step 2: Install the LiveKit CLI

```bash
brew install livekit-cli
```

Verify the install:

```bash
lk --version
```

---

## Step 3: Start LiveKit Server Locally

Run the server in **dev mode** (uses fixed default credentials, no config file needed):

```bash
livekit-server --dev
```

The server starts on `ws://localhost:7880` with the following default credentials:

| Key | Value |
|-----|-------|
| API Key | `devkey` |
| API Secret | `secret` |

> Keep this terminal open. The server runs in the foreground and must stay running while your agent is active.

---

## Step 4: Set Environment Variables

In your project `.env` file, use the local dev credentials:

```env
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
```

---

## Step 5: Run Your Agent in Console Mode

Open a new terminal tab (keep the server running in the previous one), then:

```bash
python agent_v1.py console
```

This starts the agent in terminal console mode — your Mac's mic and speakers are used directly, no browser needed.

---

### Notes

- Dev mode is for **local testing only**. Do not use `devkey`/`secret` in production.
- The `--dev` flag auto-generates a self-signed certificate and skips auth checks.
- To stop the server, press `Ctrl+C` in the terminal where it is running.
