# Integration Research Pack

## Research

When the brief names an external service, open its current official documentation and inspect a comparable real product flow. Link the exact API/SDK and user-experience pages in the generated prompt.

Common official starting points:

- WhatsApp Business Platform: https://developers.facebook.com/docs/whatsapp/
- Google Calendar API: https://developers.google.com/calendar/api
- Google Maps Platform: https://developers.google.com/maps
- ElevenLabs Agents: https://elevenlabs.io/docs/agents-platform/overview
- Stripe: https://docs.stripe.com/
- PayPal developer docs: https://developer.paypal.com/docs/
- Cal.com platform: https://cal.com/docs
- Calendly developer docs: https://developer.calendly.com/
- Supabase: https://supabase.com/docs
- Firebase: https://firebase.google.com/docs
- HubSpot APIs: https://developers.hubspot.com/docs/api/overview

Verify current names, endpoints, SDKs, scopes, pricing assumptions, and availability before using them.

## Prompt Requirements

For each integration, require the final builder to address:

- Authentication, authorization scopes, and secret storage
- Development, staging, and production environments
- Consent and privacy disclosures
- Data minimization, retention, export, and deletion where relevant
- Loading, empty, partial, timeout, rate-limit, denial, and outage states
- Idempotency and duplicate prevention for transactions or bookings
- Webhook verification and replay safety
- Accessibility and keyboard/screen-reader behavior
- Mobile and offline behavior
- Logging and observability without leaking sensitive data
- A safe fallback when credentials or capabilities are unavailable
- Clear distinction between live, sandbox, simulated, and mocked behavior

## Authorization Boundary

Research and local implementation do not authorize external side effects. Do not send messages, create events, charge accounts, publish data, contact customers, or mutate production systems unless the user explicitly requests and authorizes the action.

## Feature Comparisons

Select an actual product with an excellent implementation of the relevant user flow. Compare the completed integration at the interaction level, not merely by checking that an SDK call succeeds.

Examples:

- Scheduling: availability comprehension, timezone handling, conflict recovery, confirmation, cancellation, rescheduling
- Messaging: entry point, consent, conversation handoff, delivery failure, response expectations
- Voice: permission, disclosure, latency, interruption, transcript, escalation, failure fallback
- Payments: price clarity, validation, authentication, success, cancellation, refund, receipts, duplicate prevention
- Maps: consent, load failure, directions fallback, keyboard use, location privacy
