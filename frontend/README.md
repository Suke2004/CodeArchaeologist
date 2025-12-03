# CodeArchaeologist Frontend

Modern Next.js dashboard for resurrecting legacy code with AI.

## Features

- 🎨 Beautiful VS Code-inspired diff viewer
- 💻 Retro terminal with real-time logs
- ⚡ Real-time code transformation
- 🎭 Smooth animations and transitions
- 📱 Responsive design

## Tech Stack

- **Next.js 16** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS 4** - Styling
- **Custom Diff Viewer** - VS Code-style code comparison
- **Orbitron Font** - Futuristic title font
- **Fira Code** - Monospace font for code

## Getting Started

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Run development server:**
```bash
npm run dev
```

3. **Open browser:**
Navigate to http://localhost:3000

## Project Structure

```
frontend/
├── app/
│   ├── page.tsx          # Main dashboard page
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Global styles
├── components/
│   ├── CodeDiff.tsx      # VS Code-style diff viewer
│   └── Terminal.tsx      # Retro terminal component
└── public/               # Static assets
```

## Components

### CodeDiff
Side-by-side code comparison with syntax highlighting:
- VS Code color scheme
- Line numbers
- Add/remove indicators
- Responsive layout

**Props:**
- `oldCode: string` - Legacy code
- `newCode: string` - Modernized code

### Terminal
Retro terminal with auto-scrolling:
- Matrix-style green text
- Auto-scroll to bottom
- Blinking cursor
- macOS-style window controls

**Props:**
- `logs: string[]` - Array of log messages

## Main Page Features

### Input Section
- Large URL input field
- "Resurrect" button with loading state
- Error handling

### Loading State
- Animated terminal logs
- Simulated analysis steps
- Progress indication

### Results Display
- Side-by-side code comparison
- Summary message
- Smooth transitions

## Styling

The app uses a dark theme inspired by VS Code:
- Background: `#0f0f0f` to `#1a1a2e` gradient
- Primary color: `#00ff00` (Matrix green)
- Code background: `#1e1e1e`
- Accent colors: VS Code diff colors

## API Integration

The frontend connects to the FastAPI backend at `http://127.0.0.1:8000`:

**Endpoint:** `POST /analyze`

**Request:**
```json
{
  "url": "https://github.com/user/repo",
  "target_lang": "Python 3.11"
}
```

**Response:**
```json
{
  "original_code": "# Legacy code...",
  "modernized_code": "# Modern code...",
  "summary": "Code successfully modernized"
}
```

## Development

### Running the dev server
```bash
npm run dev
```

### Building for production
```bash
npm run build
npm start
```

### Linting
```bash
npm run lint
```

## Customization

### Changing Colors
Edit the CSS variables in `app/page.tsx` and component styles.

### Adding New Fonts
Update the Google Fonts import in `app/globals.css`.

### Modifying Terminal Logs
Edit the `logMessages` array in `app/page.tsx`.

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Performance

- Code splitting with Next.js
- Optimized fonts with `font-display: swap`
- Lazy loading for heavy components
- Efficient diff algorithm

## Future Enhancements

- [ ] Real repository cloning
- [ ] Multi-file diff view
- [ ] Download modernized code
- [ ] Share results via URL
- [ ] Dark/light theme toggle
- [ ] Syntax highlighting for multiple languages
- [ ] WebSocket for real-time updates
- [ ] Progress bar for long operations
