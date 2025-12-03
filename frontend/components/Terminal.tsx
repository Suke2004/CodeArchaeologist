import React, { useEffect, useRef } from 'react';

interface TerminalProps {
  logs: string[];
}

const Terminal: React.FC<TerminalProps> = ({ logs }) => {
  const terminalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Auto-scroll to bottom when new logs are added
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="terminal-container">
      <div className="terminal-header">
        <div className="terminal-buttons">
          <span className="terminal-button close"></span>
          <span className="terminal-button minimize"></span>
          <span className="terminal-button maximize"></span>
        </div>
        <div className="terminal-title">CodeArchaeologist Terminal</div>
      </div>
      <div className="terminal-body" ref={terminalRef}>
        {logs.map((log, index) => (
          <div key={index} className="terminal-line">
            <span className="terminal-prompt">$</span>
            <span className="terminal-text">{log}</span>
            {index === logs.length - 1 && (
              <span className="terminal-cursor">_</span>
            )}
          </div>
        ))}
      </div>
      <style jsx>{`
        .terminal-container {
          background: var(--bg-primary);
          border-radius: 8px;
          overflow: hidden;
          box-shadow: 
            0 8px 32px var(--neon-amber-glow),
            inset 0 0 40px rgba(255, 191, 0, 0.05);
          border: 2px solid var(--neon-amber);
          font-family: var(--font-mono);
          margin: 20px 0;
          position: relative;
        }

        .terminal-container::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: 
            repeating-linear-gradient(
              0deg,
              rgba(255, 191, 0, 0.02) 0px,
              transparent 1px,
              transparent 2px,
              rgba(255, 191, 0, 0.02) 3px
            );
          pointer-events: none;
        }

        .terminal-header {
          background: var(--bg-secondary);
          padding: 10px 15px;
          display: flex;
          align-items: center;
          border-bottom: 2px solid var(--neon-amber);
          box-shadow: 0 2px 10px var(--neon-amber-glow);
        }

        .terminal-buttons {
          display: flex;
          gap: 8px;
          margin-right: 15px;
        }

        .terminal-button {
          width: 12px;
          height: 12px;
          border-radius: 50%;
          display: inline-block;
          box-shadow: 0 0 5px currentColor;
        }

        .terminal-button.close {
          background: #ff5f56;
        }

        .terminal-button.minimize {
          background: var(--neon-amber);
        }

        .terminal-button.maximize {
          background: var(--neon-cyan);
        }

        .terminal-title {
          color: var(--neon-amber);
          font-size: 12px;
          font-weight: 600;
          letter-spacing: 1px;
          text-transform: uppercase;
          text-shadow: 0 0 10px var(--neon-amber-glow);
        }

        .terminal-body {
          padding: 20px;
          min-height: 300px;
          max-height: 500px;
          overflow-y: auto;
          background: var(--bg-primary);
          position: relative;
        }

        .terminal-body::-webkit-scrollbar {
          width: 8px;
        }

        .terminal-body::-webkit-scrollbar-track {
          background: var(--bg-secondary);
        }

        .terminal-body::-webkit-scrollbar-thumb {
          background: linear-gradient(180deg, var(--neon-amber), var(--neon-cyan));
          border-radius: 4px;
        }

        .terminal-line {
          color: var(--neon-amber);
          font-size: 14px;
          line-height: 1.8;
          margin-bottom: 8px;
          display: flex;
          align-items: center;
        }

        .terminal-prompt {
          color: var(--neon-cyan);
          margin-right: 10px;
          font-weight: bold;
          text-shadow: 0 0 10px var(--neon-cyan-glow);
        }

        .terminal-text {
          color: var(--neon-amber);
          text-shadow: 0 0 8px var(--neon-amber-glow);
        }

        .terminal-cursor {
          display: inline-block;
          width: 8px;
          height: 16px;
          background: var(--neon-cyan);
          margin-left: 4px;
          animation: blink 1s infinite;
          box-shadow: 0 0 10px var(--neon-cyan-glow);
        }

        @keyframes blink {
          0%, 50% {
            opacity: 1;
          }
          51%, 100% {
            opacity: 0;
          }
        }
      `}</style>
    </div>
  );
};

export default Terminal;
