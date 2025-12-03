'use client';

import { useState } from 'react';
import CodeDiff from '../components/CodeDiff';
import Terminal from '../components/Terminal';

interface AnalysisResult {
  original_code: string;
  modernized_code: string;
  summary?: string;
}

export default function Home() {
  const [repoUrl, setRepoUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const simulateLogs = async () => {
    const logMessages = [
      'Initializing CodeArchaeologist...',
      'Cloning repository...',
      'Scanning file structure...',
      'Detecting legacy patterns...',
      'Analyzing dependencies...',
      'Identifying Python 2 syntax...',
      'Checking for deprecated APIs...',
      'Building Abstract Syntax Tree...',
      'Rewriting AST nodes...',
      'Applying modernization rules...',
      'Optimizing code structure...',
      'Adding type hints...',
      'Finalizing transformation...',
      'Resurrection complete! 🎉',
    ];

    for (const message of logMessages) {
      await new Promise(resolve => setTimeout(resolve, 500));
      setLogs(prev => [...prev, message]);
    }
  };

  const handleResurrect = async () => {
    if (!repoUrl.trim()) {
      setError('Please enter a repository URL');
      return;
    }

    setIsLoading(true);
    setLogs([]);
    setResult(null);
    setError(null);

    try {
      // Start simulating logs
      const logsPromise = simulateLogs();

      // Fetch from backend
      const response = await fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: repoUrl,
          target_lang: 'Python 3.11',
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Wait for logs to finish
      await logsPromise;

      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze repository');
      setLogs(prev => [...prev, `❌ Error: ${err instanceof Error ? err.message : 'Unknown error'}`]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !isLoading) {
      handleResurrect();
    }
  };

  return (
    <main className="container">
      <div className="header">
        <h1 className="title">
          <span className="icon">🏛️</span>
          CodeArchaeologist
        </h1>
        <p className="subtitle">Resurrect Legacy Code with AI</p>
      </div>

      <div className="input-section">
        <div className="input-wrapper">
          <input
            type="text"
            className="url-input"
            placeholder="Enter repository URL (e.g., https://github.com/user/repo)"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
          />
          <button
            className="resurrect-button"
            onClick={handleResurrect}
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <span className="spinner"></span>
                Resurrecting...
              </>
            ) : (
              <>
                <span className="button-icon">⚡</span>
                Resurrect
              </>
            )}
          </button>
        </div>
        {error && <div className="error-message">{error}</div>}
      </div>

      {logs.length > 0 && (
        <div className="terminal-section">
          <Terminal logs={logs} />
        </div>
      )}

      {result && (
        <div className="results-section">
          <div className="results-header">
            <h2>Transformation Complete</h2>
            {result.summary && <p className="summary">{result.summary}</p>}
          </div>
          <CodeDiff
            oldCode={result.original_code}
            newCode={result.modernized_code}
          />
        </div>
      )}

      <style jsx>{`
        .container {
          min-height: 100vh;
          padding: 40px 20px;
          position: relative;
        }

        .container::before {
          content: '';
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: 
            repeating-linear-gradient(
              0deg,
              rgba(255, 191, 0, 0.03) 0px,
              transparent 1px,
              transparent 2px,
              rgba(255, 191, 0, 0.03) 3px
            );
          pointer-events: none;
          z-index: 1;
        }

        .header {
          text-align: center;
          margin-bottom: 60px;
          position: relative;
          z-index: 2;
        }

        .title {
          font-family: var(--font-display);
          font-size: 4rem;
          font-weight: 900;
          background: linear-gradient(135deg, var(--neon-amber) 0%, var(--neon-cyan) 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          margin: 0;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 20px;
          filter: drop-shadow(0 0 30px var(--neon-amber-glow));
        }

        .icon {
          font-size: 4rem;
          filter: drop-shadow(0 0 20px var(--neon-amber-glow)) 
                  drop-shadow(0 0 40px var(--neon-cyan-glow));
          animation: pulse-amber 3s ease-in-out infinite;
        }

        .subtitle {
          font-size: 1.2rem;
          color: var(--neon-cyan);
          margin-top: 10px;
          font-weight: 400;
          letter-spacing: 3px;
          text-transform: uppercase;
          text-shadow: 0 0 10px var(--neon-cyan-glow);
        }

        .input-section {
          max-width: 900px;
          margin: 0 auto 40px;
          position: relative;
          z-index: 2;
        }

        .input-wrapper {
          display: flex;
          gap: 15px;
          margin-bottom: 15px;
        }

        .url-input {
          flex: 1;
          padding: 18px 24px;
          font-size: 16px;
          background: var(--bg-secondary);
          border: 2px solid var(--neon-amber);
          border-radius: 8px;
          color: var(--neon-amber);
          font-family: var(--font-mono);
          transition: all 0.3s ease;
          box-shadow: inset 0 0 20px rgba(255, 191, 0, 0.05);
        }

        .url-input:focus {
          outline: none;
          border-color: var(--neon-cyan);
          color: var(--neon-cyan);
          box-shadow: 
            inset 0 0 20px rgba(0, 240, 255, 0.1),
            0 0 20px var(--neon-cyan-glow);
        }

        .url-input::placeholder {
          color: var(--neon-amber-dim);
          opacity: 0.5;
        }

        .url-input:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .resurrect-button {
          padding: 18px 40px;
          font-size: 16px;
          font-weight: 700;
          background: var(--bg-secondary);
          color: var(--neon-cyan);
          border: 2px solid var(--neon-cyan);
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.3s ease;
          display: flex;
          align-items: center;
          gap: 10px;
          text-transform: uppercase;
          letter-spacing: 2px;
          font-family: var(--font-mono);
          position: relative;
          overflow: hidden;
          box-shadow: 
            0 0 20px var(--neon-cyan-glow),
            inset 0 0 20px rgba(0, 240, 255, 0.1);
        }

        .resurrect-button::before {
          content: '';
          position: absolute;
          top: -2px;
          left: -2px;
          right: -2px;
          bottom: -2px;
          background: linear-gradient(45deg, var(--neon-amber), var(--neon-cyan), var(--neon-amber));
          border-radius: 8px;
          opacity: 0;
          transition: opacity 0.3s ease;
          z-index: -1;
        }

        .resurrect-button:hover:not(:disabled) {
          transform: translateY(-2px);
          box-shadow: 
            0 0 30px var(--neon-cyan-glow),
            0 5px 40px var(--neon-cyan-glow),
            inset 0 0 30px rgba(0, 240, 255, 0.2);
          color: var(--bg-primary);
          background: var(--neon-cyan);
        }

        .resurrect-button:hover:not(:disabled)::before {
          opacity: 1;
        }

        .resurrect-button:active:not(:disabled) {
          transform: translateY(0);
        }

        .resurrect-button:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .button-icon {
          font-size: 20px;
          filter: drop-shadow(0 0 5px currentColor);
        }

        .spinner {
          width: 16px;
          height: 16px;
          border: 2px solid var(--neon-cyan);
          border-top-color: transparent;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }

        .error-message {
          color: #ff5555;
          background: rgba(255, 85, 85, 0.1);
          padding: 12px 20px;
          border-radius: 6px;
          border: 1px solid #ff5555;
          font-size: 14px;
          font-family: var(--font-mono);
          box-shadow: 0 0 20px rgba(255, 85, 85, 0.2);
        }

        .terminal-section {
          max-width: 1200px;
          margin: 0 auto 40px;
          position: relative;
          z-index: 2;
        }

        .results-section {
          max-width: 1400px;
          margin: 0 auto;
          position: relative;
          z-index: 2;
        }

        .results-header {
          text-align: center;
          margin-bottom: 30px;
        }

        .results-header h2 {
          font-size: 2rem;
          color: var(--neon-cyan);
          margin: 0 0 10px 0;
          font-family: var(--font-display);
          text-shadow: 0 0 20px var(--neon-cyan-glow);
        }

        .summary {
          color: var(--neon-amber);
          font-size: 1rem;
          margin: 0;
          font-family: var(--font-mono);
          text-shadow: 0 0 10px var(--neon-amber-glow);
        }

        @media (max-width: 768px) {
          .title {
            font-size: 2.5rem;
            flex-direction: column;
            gap: 10px;
          }

          .icon {
            font-size: 3rem;
          }

          .input-wrapper {
            flex-direction: column;
          }

          .resurrect-button {
            width: 100%;
            justify-content: center;
          }
        }
      `}</style>
    </main>
  );
}
