# Contributing to NEXUS AI OS

Thank you for your interest in contributing to NEXUS AI OS! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and professional. We follow the Contributor Covenant.

## Getting Started

### Prerequisites

- Node.js 20+
- Python 3.12+
- PostgreSQL 15+
- Docker & Docker Compose
- Git

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/pushkarbalyan19ash/ai-operating-system.git
cd ai-operating-system

# Create development branch
git checkout -b feature/your-feature-name

# Setup with Docker
docker-compose up -d
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/descriptive-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `perf/` - Performance improvements
- `test/` - Test additions

### 2. Commit Guidelines

```bash
# Meaningful commit messages
git commit -m "type: description"
```

Commit types:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style
- `refactor:` Code refactoring
- `perf:` Performance improvement
- `test:` Test additions/updates
- `chore:` Build, dependencies, etc.

## Code Style

### Frontend (TypeScript/React)

- Use functional components with hooks
- Use TypeScript strict mode
- Keep components under 300 lines
- Add JSDoc comments for complex logic

### Backend (Python)

- Use type hints
- Follow PEP 8 style guide
- Add docstrings to functions
- Use async/await for I/O operations

## Testing

```bash
# Frontend
cd frontend
npm run test

# Backend
cd backend
pytest
```

## Pull Request Process

1. Create feature branch
2. Make changes with meaningful commits
3. Push branch and create PR
4. Address reviewer feedback
5. Merge after 2 approvals

## License

By contributing, you agree your contributions are licensed under MIT License.

Thank you for contributing! 🚀
