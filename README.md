# 🚀 Deep Research System - Proper UV Setup Guide

A modern setup guide using UV's native commands and best practices.

---

## 📋 Quick Start (The UV Way)

```bash
# 1. Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# OR
irm https://astral.sh/uv/install.ps1 | iex      # Windows PowerShell

# 2. Create project
mkdir DeepResearchSystem && cd DeepResearchSystem
uv init --python 3.11

# 3. Add dependencies (updates pyproject.toml automatically)
uv add google-generativeai python-dotenv

# 4. Configure API key
echo "GEMINI_API_KEY=AIzaSy_your_actual_key_here" > .env

# 5. Copy the 5 Python agent files here

# 6. Run the system (no 'python' needed!)
uv run deep_research_system.py
```

---

## 📦 Step 1: Install UV

### macOS/Linux
```bash
# Recommended: Official installer
curl -LsSf https://astral.sh/uv/install.sh | sh

# Alternative: Homebrew
brew install uv
```

### Windows
```powershell
# PowerShell (Run as Administrator)
irm https://astral.sh/uv/install.ps1 | iex

# Alternative: Scoop
scoop install uv
```

### Verify Installation
```bash
uv --version  # Should show 0.4.0 or higher
```

---

## 🏗️ Step 2: Project Initialization (The UV Way)

### Create Project with Python Version
```bash
# Create project directory
mkdir DeepResearchSystem
cd DeepResearchSystem

# Initialize with specific Python version
uv init --python 3.11

# OR let UV pick the best Python
uv init
```

This creates:
- `pyproject.toml` - Project configuration
- `.python-version` - Python version lock
- `README.md` - Project description
- `.gitignore` - Git ignore rules

### Create Required Directories
```bash
# Create cache and output directories
mkdir -p research_cache synthesis_cache report_cache research_reports
```

---

## 📥 Step 3: Add Dependencies (The Proper UV Way)

### Using `uv add` (Recommended)
```bash
# Add project dependencies (automatically updates pyproject.toml)
uv add google-generativeai python-dotenv

# Add development dependencies (optional)
uv add --dev pytest black ruff ipython

# The dependencies are automatically added to pyproject.toml!
```

### Why `uv add` is Better:
- ✅ Automatically updates `pyproject.toml`
- ✅ Resolves dependency conflicts
- ✅ Locks versions in `uv.lock`
- ✅ Ensures reproducible installs
- ✅ Faster than pip

### Your pyproject.toml Will Look Like:
```toml
[project]
name = "deepresearchsystem"
version = "0.1.0"
description = "AI-powered research system using Google Gemini"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "google-generativeai>=0.8.3",
    "python-dotenv>=1.0.1",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.3.3",
    "black>=24.10.0",
    "ruff>=0.7.2",
    "ipython>=8.29.0",
]
```

---

## 🔑 Step 4: Configure Environment

### Create .env File
```bash
# Create .env with your API key
cat > .env << 'EOF'
# Google Gemini API Key (REQUIRED)
GEMINI_API_KEY=AIzaSy_your_actual_key_here

# Optional: Tavily API Key for web search
# TAVILY_API_KEY=tvly-your-key-here
EOF
```

### Get Your Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Get API Key" or "Create API Key"
4. Copy the entire key (starts with `AIzaSy`)

---

## 📄 Step 5: Add Agent Files

Copy these 5 Python files to your project:

```bash
# Your project structure should be:
DeepResearchSystem/
├── pyproject.toml          # Created by uv init
├── .python-version         # Created by uv init
├── uv.lock                 # Created by uv add
├── .env                    # Your API key
├── planning_agent.py       # Agent 1
├── research_agents.py      # Agent 2
├── synthesis_agent.py      # Agent 3
├── report_writer.py        # Agent 4
├── deep_research_system.py # Main system
├── research_cache/         # Cache directory
├── synthesis_cache/        # Cache directory
├── report_cache/          # Cache directory
└── research_reports/      # Output directory
```

---

## ✅ Step 6: Verify Setup (UV Native Commands)

### Check Installation
```bash
# Show UV version
uv version

# Show Python version UV will use
uv python list

# Show installed packages
uv pip list

# Verify specific package
uv pip show google-generativeai
```

### Quick API Test (Direct UV Run)
```bash
# Test API connection (one-liner)
uv run -c "import google.generativeai as genai; from dotenv import load_dotenv; import os; load_dotenv(); genai.configure(api_key=os.getenv('GEMINI_API_KEY')); model = genai.GenerativeModel('gemini-1.5-flash'); print('✅ API Test:', model.generate_content('Say OK').text)"
```

---

## 🚀 Step 7: Run the System (UV Native)

### Main System (No 'python' needed!)
```bash
# UV automatically detects it's a Python script
uv run deep_research_system.py
```

### Test Individual Components
```bash
# Test each agent directly
uv run planning_agent.py
uv run research_agents.py
uv run synthesis_agent.py
uv run report_writer.py
```

### Create Run Shortcuts in pyproject.toml

Add this to your `pyproject.toml`:
```toml
[project.scripts]
research = "deep_research_system:main"
test-planning = "planning_agent:test_planning_agent"
test-research = "research_agents:test_research_agents"
test-synthesis = "synthesis_agent:test_synthesis_agent"
test-report = "report_writer:test_report_writer"
```

Then run with:
```bash
uv run research              # Run main system
uv run test-planning        # Test planning agent
uv run test-research        # Test research agents
```

---

## 🎯 Advanced UV Usage

### Create a UV Script for Common Tasks

Create `research.py`:
```python
#!/usr/bin/env python
"""Quick research script with argument support."""
import sys
from deep_research_system import DeepResearchSystem

def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Enter research question: ")
    
    system = DeepResearchSystem()
    system.run_research(query)

if __name__ == "__main__":
    main()
```

Run it directly:
```bash
# Make it executable (macOS/Linux)
chmod +x research.py

# Run with UV (no 'python' needed)
uv run research.py "How has AI changed healthcare?"

# Or without arguments (will prompt)
uv run research.py
```

### Use UV's Tool Management

UV can manage Python tools globally:
```bash
# Install tools globally with UV
uv tool install ruff
uv tool install black

# Run tools
uv tool run ruff check .
uv tool run black *.py
```

---

## 🔄 Dependency Management (The UV Way)

### Add New Dependencies
```bash
# Add to project
uv add pandas numpy

# Add dev dependency
uv add --dev jupyter notebook

# Add with version constraints
uv add "requests>=2.28.0"
```

### Update Dependencies
```bash
# Update all dependencies
uv sync

# Update specific package
uv add --upgrade google-generativeai

# Lock dependencies
uv lock
```

### Remove Dependencies
```bash
# Remove package
uv remove pandas

# Remove dev dependency
uv remove --dev jupyter
```

---

## 📊 UV vs Traditional Commands

| Task | Old Way | UV Way |
|------|---------|---------|
| Install package | `pip install package` | `uv add package` |
| Install dev package | `pip install -e .[dev]` | `uv add --dev package` |
| Run script | `python script.py` | `uv run script.py` |
| List packages | `pip list` | `uv pip list` |
| Create venv | `python -m venv .venv` | `uv venv` (automatic) |
| Activate venv | `source .venv/bin/activate` | Not needed! |
| Install from file | `pip install -r requirements.txt` | `uv sync` |
| Freeze deps | `pip freeze > requirements.txt` | `uv lock` (automatic) |

---

## 🔧 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| `uv: command not found` | Restart terminal or check PATH |
| Module not found | Run `uv sync` to install from pyproject.toml |
| API key not found | Check .env file exists |
| Can't run script | Use `uv run script.py` not `python script.py` |
| Dependencies out of sync | Run `uv sync` to update |

### Reset Project
```bash
# Clean everything
uv clean
rm -rf uv.lock

# Reinstall
uv sync

# Or fresh install
uv add google-generativeai python-dotenv
```

---

## 💡 UV Best Practices

### 1. **Always use `uv add` for dependencies**
```bash
# Good ✅
uv add google-generativeai

# Avoid ❌
uv pip install google-generativeai
```

### 2. **Run scripts directly with `uv run`**
```bash
# Good ✅
uv run deep_research_system.py

# Unnecessary ❌
uv run python deep_research_system.py
```

### 3. **Let UV manage the virtual environment**
```bash
# UV handles this automatically ✅
uv add package  # Creates venv if needed

# Don't manually activate ❌
source .venv/bin/activate  # Not needed!
```

### 4. **Use `uv sync` for reproducible installs**
```bash
# After cloning a project
git clone <repo>
cd <repo>
uv sync  # Installs exact versions from uv.lock
```

### 5. **Commit both pyproject.toml and uv.lock**
```bash
git add pyproject.toml uv.lock
git commit -m "Lock dependencies"
```

---

## 📚 UV Power Features

### Python Version Management
```bash
# List available Pythons
uv python list

# Install specific Python
uv python install 3.12

# Pin project to Python version
uv python pin 3.11
```

### Global Tool Management
```bash
# Install tools globally
uv tool install poetry
uv tool install pipx
uv tool install pre-commit

# Update all tools
uv tool upgrade --all
```

### Workspace Support (Monorepos)
```bash
# Create workspace
uv init --workspace

# Add packages to workspace
uv add --workspace shared-lib
```

---

## 🎉 You're Ready!

Your Deep Research System is now properly set up with UV. Run your first research:

```bash
# The UV-native way
uv run deep_research_system.py
```

---

## 📋 Quick Reference Card

```bash
# Project Setup
uv init                     # Create project
uv add <package>           # Add dependency
uv add --dev <package>     # Add dev dependency
uv sync                    # Install all dependencies
uv lock                    # Lock versions

# Running Code
uv run script.py           # Run Python script
uv run -c "code"          # Run Python code
uv run <command>          # Run project command

# Management
uv pip list               # List packages
uv pip show <package>     # Package details
uv python list            # List Pythons
uv tool list              # List tools
uv clean                  # Clean cache
```