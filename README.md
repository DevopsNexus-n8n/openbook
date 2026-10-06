# Openbook

Booking and client management for salons, clinics and wellness studios. (Working name.)

## Run locally

    cp .env.example .env
    docker compose up --build

- API: http://localhost:8000 (docs at /docs)
- Landing page: http://localhost:8080

## Tests

    cd backend && pip install -r requirements.txt && pytest -q

## Branches

- `main`: production, deploys on merge (added in Stage 4)
- `dev`: integration branch; open PRs into `dev`

## Stages

1. Foundation: repo, Docker, CI, landing page and waitlist (this commit)
2. Multi-tenancy, auth, billing
3. Clients, services, staff, appointments, reminders
4. Production infrastructure
