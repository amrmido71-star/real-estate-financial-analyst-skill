# Contributing Guide

Thank you for considering contributing to `real-estate-financial-analyst-skill`!

## How to Contribute

### 1. Fork & Clone
```bash
git clone https://github.com/amrmido71-star/real-estate-financial-analyst-skill.git
cd real-estate-financial-analyst-skill
```

### 2. Create Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-fix-name
```

### 4. Make Changes
- Follow PEP 8
- Add docstrings to all functions
- Add tests for new logic
- Update documentation if needed

### 5. Run Tests
```bash
pytest -v
pytest --cov=skill/tools
```

### 6. Commit
```bash
git add .
git commit -m "feat: add sensitivity tornado chart"
```

Commit convention (Conventional Commits):
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `test:` tests
- `refactor:` refactoring
- `chore:` tooling

### 7. Push & PR
```bash
git push origin feature/your-feature-name
```
Then open a Pull Request on GitHub.

## Code Standards
- Python 3.9+
- Type hints required
- No division by zero — always guard
- No fabricated financial data — raise or return None with explanation
- All financial formulas must reference source in docstring

## Reporting Issues
Use GitHub Issues with:
- Description
- Steps to reproduce
- Expected vs Actual
- Screenshots / data sample (anonymized)

## Financial Logic Review
Any change to formulas in `skill/tools/` requires:
1. Reference to accounting / valuation standard
2. Unit test with known expected value
3. Review by second contributor

Thank you! 🙏
