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

# Or setup manually
# Frontend
cd frontend
npm install
npm run dev

# Backend (in another terminal)
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
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

### 2. Make Changes

- Write clean, readable code
- Follow project style guides
- Add tests for new functionality
- Update documentation as needed

### 3. Commit Guidelines

```bash
# Meaningful commit messages
git commit -m "type: description"
```

Commit types:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style (formatting, etc.)
- `refactor:` Code refactoring
- `perf:` Performance improvement
- `test:` Test additions/updates
- `chore:` Build, dependencies, etc.

Example:
```bash
git commit -m "feat: add browser automation agent"
git commit -m "fix: resolve memory leak in particle system"
```

### 4. Push and Create Pull Request

```bash
# Push your branch
git push origin feature/your-feature-name

# Create PR on GitHub
# Fill out the PR template with:
# - Description of changes
# - Related issues
# - Testing done
# - Screenshots (if UI changes)
```

## Code Style

### Frontend (TypeScript/React)

```typescript
// Use functional components with hooks
const MyComponent: React.FC<Props> = ({ prop1, prop2 }) => {
  const [state, setState] = useState<string>('');
  
  return (
    <div className="component">
      {/* Component JSX */}
    </div>
  );
};

export default MyComponent;
```

- Use TypeScript strict mode
- Use descriptive variable names
- Add JSDoc comments for complex logic
- Keep components under 300 lines
- Use custom hooks for reusable logic

### Backend (Python)

```python
# Use type hints
from typing import Optional, List
from pydantic import BaseModel

class AgentResponse(BaseModel):
    """Agent response model."""
    status: str
    data: Optional[dict] = None
    error: Optional[str] = None

async def process_request(
    request: AgentRequest,
    timeout: int = 30
) -> AgentResponse:
    """Process agent request."""
    # Implementation
    pass
```

- Use type hints for all functions
- Follow PEP 8 style guide
- Add docstrings to functions
- Use async/await for I/O operations
- Keep functions focused and testable

## Testing

### Frontend Tests

```bash
cd frontend
npm run test
npm run test:coverage
```

### Backend Tests

```bash
cd backend
pytest
pytest --cov=app  # With coverage
```

### Test Requirements

- Write tests for new features
- Maintain >80% code coverage
- All tests must pass before PR merge
- Use descriptive test names

## Documentation

- Update README.md for new features
- Add API documentation for new endpoints
- Document agent behaviors and tools
- Update CHANGELOG.md
- Add inline comments for complex logic

## Pull Request Process

1. **Before submitting:**
   - Run tests locally
   - Check code style
   - Update documentation
   - Add meaningful commit messages

2. **PR Requirements:**
   - Link related issues
   - Provide clear description
   - Add screenshots for UI changes
   - Ensure CI/CD passes
   - Request reviews from maintainers

3. **Review Process:**
   - Address reviewer feedback
   - Make requested changes
   - Re-request review after updates
   - PR requires 2 approvals to merge

4. **Merging:**
   - Squash commits for clarity
   - Use meaningful merge commit message
   - Delete feature branch after merge

## Performance Guidelines

### Frontend
- Keep components under 300 lines
- Memoize expensive computations
- Lazy load components and routes
- Optimize images and assets
- Target 60 FPS animations
- Lighthouse score 95+

### Backend
- Use async/await for I/O
- Implement caching where appropriate
- Use database indexes for queries
- Monitor response times
- Optimize AI model inference

## Security

- Never commit API keys or secrets
- Use environment variables
- Validate all inputs
- Implement rate limiting
- Follow OWASP guidelines
- Regular security audits

## Issue Reporting

### Bug Reports

Include:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Screenshots/logs if applicable

### Feature Requests

Include:
- Clear description of feature
- Use cases and benefits
- Potential implementation approach
- Links to related discussions

## Getting Help

- Check existing issues and discussions
- Read documentation in `/docs`
- Review code comments and examples
- Ask in GitHub Discussions
- Contact maintainers for guidance

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- README.md Contributors section
- Release notes
- GitHub contributors page

Thank you for contributing! 🚀
