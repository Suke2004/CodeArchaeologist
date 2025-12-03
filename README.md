# 🏛️ CodeArchaeologist

![Kiroween Hackathon](https://img.shields.io/badge/Kiroween-Hackathon-orange)
![Category](https://img.shields.io/badge/Category-Resurrection-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Next.js](https://img.shields.io/badge/Next.js-16-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)

**Resurrect Legacy Code with AI** ⚡

CodeArchaeologist brings abandoned repositories back to life by analyzing legacy code patterns, detecting security vulnerabilities, and using AI to modernize them into production-ready applications.

## ✨ Features

- 🤖 **AI-Powered Modernization** - Google Gemini transforms legacy code
- 🔍 **Pattern Detection** - Identifies Python 2, deprecated APIs, security issues
- 📊 **Technical Debt Analysis** - Calculates maintainability scores and estimates
- 🎨 **Cyber-Archaeology Theme** - Stunning neon UI with holographic effects
- ⚡ **Real-Time Feedback** - Live terminal logs during analysis
- 📝 **Side-by-Side Diff** - Visual comparison of legacy vs modern code

## 🚨 SECURITY NOTICE

**⚠️ IMPORTANT:** This repository previously contained exposed API keys in git history. These keys have been **REVOKED**. 

- **DO NOT use any API keys found in git history**
- **Generate your own keys** following the setup instructions below
- **NEVER commit `.env` files** with real credentials
- See `SECURITY_WARNING.md` for full details

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Automated Setup (Recommended)

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```bash
setup.bat
```

The setup script will:
- ✅ Check prerequisites
- ✅ Create virtual environments
- ✅ Install all dependencies
- ✅ Create `.env` files from templates
- ✅ Compile TypeScript
- ✅ Verify setup

### Manual Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd codearchaeologist
```

2. **Setup Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env from template
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

3. **Setup Frontend**
```bash
cd frontend
npm install

# Create .env from template (optional)
cp .env.example .env
```

4. **Setup MCP (Optional)**
```bash
cd mcp
npm install
npm run build

# Create .env from template (optional)
cp .env.example .env
```

5. **Verify Setup**
```bash
python setup_verify.py
```

6. **Run the Application**

Terminal 1 (Backend):
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn main:app --reload
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

7. **Open your browser**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

### Configuration

**Required:**
- `GEMINI_API_KEY` in `backend/.env` - Get from https://makersuite.google.com/app/apikey

**Optional:**
- `GITHUB_TOKEN` in `frontend/.env` or `mcp/.env` - For private repository access

**⚠️ Security Reminder:**
- Never commit `.env` files
- Use `.env.example` templates
- Rotate keys regularly
- See `SECURITY.md` for best practices

## 🧪 Testing

### Quick Connectivity Test
```bash
# Test frontend-backend connection
python test_connectivity.py
```

### Test AI Connection
```bash
# Test Gemini API connection
cd backend
python test_ai_connection.py
```

### Quick Backend Test
```bash
cd backend
python test_backend.py
```

### Full Test Suite
```bash
cd backend
pytest
```

### Interactive Test
```bash
cd backend
python test_detector.py
```

## 🐛 Troubleshooting

### HTTP 500 Error

If you get a 500 error when analyzing code:

1. **Check backend logs** - Look at the terminal running uvicorn
2. **Test AI connection**:
   ```bash
   cd backend
   python test_ai_connection.py
   ```
3. **Test the detector**:
   ```bash
   cd backend
   python test_backend.py
   ```
4. **Verify environment**:
   ```bash
   python setup_verify.py
   ```

**Common AI Errors:**
- `404 models/gemini-pro is not found` - API key issue or model name changed
- Run `python backend/test_ai_connection.py` to diagnose
- Check your API key at https://makersuite.google.com/app/apikey

### Backend Won't Start

```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
cd backend
pip install -r requirements.txt

# Test imports
python -c "import fastapi; print('OK')"
```

### Frontend Connection Error

```bash
# Check backend is running
curl http://localhost:8000/health

# Check CORS settings in backend/main.py
# Should include: http://localhost:3000
```

### Tests Failing

```bash
# Run with verbose output
cd backend
pytest -v

# Run specific test
pytest tests/test_legacy_detector.py -v

# Check for import errors
python -c "from services.legacy_detector import LegacyDetector; print('OK')"
```

## 🎯 Usage

1. Enter a repository URL or paste code directly
2. Click the "Resurrect" button
3. Watch the terminal as AI analyzes your code
4. View the side-by-side comparison of legacy vs modern code
5. Review technical debt metrics and recommendations

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **Google Gemini AI** - Code transformation engine
- **Pydantic** - Data validation and type safety
- **Python 3.11+** - Latest Python features

### Frontend
- **Next.js 16** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS 4** - Utility-first styling
- **Custom Components** - CodeDiff viewer, Terminal

## 📊 What It Detects

### Python 2 Patterns
- `print` statements → `print()` functions
- Old exception syntax → `except Exception as e:`
- `.iteritems()` → `.items()`
- `xrange()` → `range()`
- String formatting → f-strings

### Security Issues
- Unsafe `eval()` and `exec()` usage
- Insecure deserialization (pickle)
- Weak hash algorithms (MD5, SHA1)

### Code Quality
- Missing type hints
- Deprecated APIs
- Technical debt metrics
- Maintainability scores

## 🎨 Screenshots

[Add screenshots here]

## 🏆 Kiro Integration

This project showcases all 5 key Kiro features:

1. **Specs** - Formal requirements for code transformation
2. **Agent Hooks** - Auto-trigger tests on file changes
3. **MCP** - GitHub connector for repository analysis
4. **Steering** - Modernization rules per framework
5. **Vibe Coding** - Rapid prototyping with AI assistance

## 📖 Documentation

| Document | Description |
|----------|-------------|
| `README.md` | Project overview and quick start |
| `TESTING.md` | Comprehensive testing guide |
| `TROUBLESHOOTING.md` | Common issues and solutions |
| `SECURITY.md` | Security policy and best practices |
| `SECURITY_WARNING.md` | Exposed keys incident |
| `CONTRIBUTING.md` | Contribution guidelines |
| `CHANGELOG.md` | Version history |
| `QUICK_REFERENCE.md` | Quick reference card |

## 📝 Project Structure

```
codearchaeologist/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── services/
│   │   ├── ai_engine.py     # Gemini AI integration
│   │   └── legacy_detector.py  # Pattern detection
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── app/
│   │   ├── page.tsx         # Main dashboard
│   │   └── globals.css      # Cyber theme styles
│   ├── components/
│   │   ├── CodeDiff.tsx     # Diff viewer
│   │   └── Terminal.tsx     # Terminal component
│   └── package.json
└── README.md
```

## 🚧 Roadmap

- [ ] Real GitHub repository cloning
- [ ] Multi-file analysis
- [ ] Support for JavaScript/TypeScript
- [ ] Automated test generation
- [ ] Export as Pull Request
- [ ] CI/CD integration
- [ ] Batch processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **Kiro IDE** - For the amazing development experience
- **Google Gemini** - For AI-powered transformations
- **Kiroween Hackathon** - For the inspiration

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ for the Kiroween Hackathon**

*Bringing dead code back to life, one repository at a time* 🏛️⚡
