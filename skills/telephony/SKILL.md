---
name: telephony
description: "Twilio numbers, SMS/MMS, and AI outbound calls (Bland/Vapi). Use for phone numbers, texts, or outbound AI calls. Not for email (google-workspace, email-inbox-triage) or calendar meetings."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    tags: [telephony, phone, sms, mms, voice, twilio, bland, vapi]
    category: Productivity
    related_skills: [google-workspace, email-inbox-triage]
    attribution: Adapted from Nous Research hermes-agent optional telephony skill (MIT)
---

# Telephony

Phone capabilities via `scripts/telephony.py` (stdlib HTTP — no extra pip deps).

**When to use:** buy/own a Twilio number · send/poll SMS/MMS · direct Twilio call ·
outbound AI call (Bland or Vapi).

**Do not use:** email triage → `email-inbox-triage` / `google-workspace`; meeting
notes → `meeting-action-items`. Not a real-time inbound call gateway.

## Safety (mandatory)

1. **Confirm before** any call or text.
2. Never dial emergency numbers.
3. No harassment, spam, impersonation, or illegal use.
4. Do not persist third-party phone numbers in memory/docs unless the user asks.
5. Agent-owned Twilio number may be saved in config.
6. VoIP may fail third-party 2FA — set expectations.

## Paths / state

Credentials and IDs in `$PIXIS_HOME/.env` (default `~/.pixis/.env`):

`TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`,
`TWILIO_PHONE_NUMBER_SID`, `BLAND_API_KEY`, `VAPI_API_KEY`,
`VAPI_PHONE_NUMBER_ID`, `PHONE_PROVIDER`

Skill state: `$PIXIS_HOME/telephony_state.json` (default number, inbox checkpoint).

```bash
SCRIPT="<skill-dir>/scripts/telephony.py"
python "$SCRIPT" diagnose   # always start here when resuming
```

Missing credentials → run `diagnose`, then guide provider signup — do not claim
sends/calls succeeded.

## Provider choice

| Need | Use |
|---|---|
| Own a number, SMS, inbound poll | **Twilio** |
| Fastest outbound AI call | **Bland.ai** |
| Best conversational AI voice | **Twilio + Vapi** |
| Prerecorded audio message | **Twilio** `--audio-url` |

## Setup commands

```bash
python "$SCRIPT" save-twilio AC... AUTH_TOKEN
python "$SCRIPT" twilio-search --country US --area-code 702 --limit 5
python "$SCRIPT" twilio-buy "+1..." --save-env   # confirm cost first
python "$SCRIPT" twilio-owned
python "$SCRIPT" twilio-set-default "+1..." --save-env

python "$SCRIPT" save-bland API_KEY --voice mason
python "$SCRIPT" save-vapi API_KEY
python "$SCRIPT" vapi-import-twilio --save-env
```

## Common workflows

```bash
# SMS / MMS (confirm recipient + body first)
python "$SCRIPT" twilio-send-sms "+1..." "Message" [--media-url URL]

# Poll inbound (no webhook server)
python "$SCRIPT" twilio-inbox --limit 20
python "$SCRIPT" twilio-inbox --since-last --mark-seen

# Direct call
python "$SCRIPT" twilio-call "+1..." --message "Hello" --voice Polly.Joanna
python "$SCRIPT" twilio-call "+1..." --audio-url "https://.../msg.mp3"
python "$SCRIPT" twilio-call "+1..." --message "..." --send-digits "ww1w2"

# AI call
python "$SCRIPT" ai-call "+1..." "Task instructions..." --provider bland --max-duration 3
python "$SCRIPT" ai-call "+1..." "..." --provider vapi --max-duration 4
python "$SCRIPT" ai-status CALL_ID --provider bland
```

## Agent procedure

1. Pick provider via the table above  
2. `diagnose` if state unclear  
3. Gather full task details  
4. **Confirm** before dial/text  
5. Run the command; poll status if needed  
6. Summarize without storing third-party numbers  

## Out of scope

Real-time inbound answering · webhook SMS push · guaranteed 2FA on VoIP.

## Completion criteria

- `diagnose` run when config unclear
- User confirmed before send/call
- Failures report provider errors honestly
- No emergency dialing; no secret keys printed
