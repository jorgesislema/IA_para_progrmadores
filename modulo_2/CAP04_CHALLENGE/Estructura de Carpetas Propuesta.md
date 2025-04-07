room-reservation-system/
├── frontend/
│   ├── web/
│   │   ├── public/
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── pages/
│   │   │   ├── services/
│   │   └── package.json
│   └── mobile/
│       ├── assets/
│       ├── src/
│       └── package.json
├── backend/
│   ├── authentication-service/
│   │   ├── src/
│   │   ├── tests/
│   │   └── Dockerfile
│   ├── reservations-service/
│   │   ├── src/
│   │   ├── tests/
│   │   └── Dockerfile
│   ├── payments-service/
│   │   ├── src/
│   │   ├── tests/
│   │   └── Dockerfile
│   ├── availability-service/
│   │   ├── src/
│   │   ├── tests/
│   │   └── Dockerfile
│   ├── notifications-service/
│   │   ├── src/
│   │   ├── tests/
│   │   └── Dockerfile
│   └── gateway/
│       ├── src/
│       └── Dockerfile
├── infrastructure/
│   ├── database/
│   │   ├── migrations/
│   │   ├── seeds/
│   │   └── scripts/
│   ├── deployment/
│   │   ├── docker-compose.yml
│   │   ├── kubernetes/
│   │   │   └── deployment.yaml
│   └── scripts/
└── docs/
    ├── diagrams/
    └── architecture.md