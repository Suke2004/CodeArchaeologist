'use client';

import React, { useMemo } from 'react';

interface CodeDiffProps {
  oldCode: string;
  newCode: string;
}

interface DiffLine {
  type: 'added' | 'removed' | 'unchanged';
  content: string;
  oldLineNumber?: number;
  newLineNumber?: number;
}

const CodeDiff: React.FC<CodeDiffProps> = ({ oldCode, newCode }) => {
  const diffLines = useMemo(() => {
    const oldLines = oldCode.split('\n');
    const newLines = newCode.split('\n');
    const result: DiffLine[] = [];
    
    let oldIndex = 0;
    let newIndex = 0;
    
    while (oldIndex < oldLines.length || newIndex < newLines.length) {
      const oldLine = oldLines[oldIndex];
      const newLine = newLines[newIndex];
      
      if (oldLine === newLine) {
        result.push({
          type: 'unchanged',
          content: oldLine || '',
          oldLineNumber: oldIndex + 1,
          newLineNumber: newIndex + 1,
        });
        oldIndex++;
        newIndex++;
      } else {
        // Check if line was removed
        if (oldIndex < oldLines.length && !newLines.includes(oldLine)) {
          result.push({
            type: 'removed',
            content: oldLine,
            oldLineNumber: oldIndex + 1,
          });
          oldIndex++;
        }
        // Check if line was added
        else if (newIndex < newLines.length && !oldLines.includes(newLine)) {
          result.push({
            type: 'added',
            content: newLine,
            newLineNumber: newIndex + 1,
          });
          newIndex++;
        }
        // Lines are different but might be modifications
        else {
          if (oldIndex < oldLines.length) {
            result.push({
              type: 'removed',
              content: oldLine,
              oldLineNumber: oldIndex + 1,
            });
            oldIndex++;
          }
          if (newIndex < newLines.length) {
            result.push({
              type: 'added',
              content: newLine,
              newLineNumber: newIndex + 1,
            });
            newIndex++;
          }
        }
      }
    }
    
    return result;
  }, [oldCode, newCode]);

  return (
    <div className="code-diff-wrapper">
      <div className="diff-header">
        <div className="diff-title left">🪦 Legacy Code</div>
        <div className="diff-title right">✨ Modernized Code</div>
      </div>
      <div className="diff-container">
        <div className="diff-pane left-pane">
          {diffLines.map((line, index) => (
            line.type !== 'added' && (
              <div
                key={`left-${index}`}
                className={`diff-line ${line.type}`}
              >
                <span className="line-number">
                  {line.oldLineNumber || ''}
                </span>
                <span className="line-marker">
                  {line.type === 'removed' ? '-' : ' '}
                </span>
                <pre className="line-content">{line.content || ' '}</pre>
              </div>
            )
          ))}
        </div>
        <div className="diff-pane right-pane">
          {diffLines.map((line, index) => (
            line.type !== 'removed' && (
              <div
                key={`right-${index}`}
                className={`diff-line ${line.type}`}
              >
                <span className="line-number">
                  {line.newLineNumber || ''}
                </span>
                <span className="line-marker">
                  {line.type === 'added' ? '+' : ' '}
                </span>
                <pre className="line-content">{line.content || ' '}</pre>
              </div>
            )
          ))}
        </div>
      </div>
      <style jsx>{`
        .code-diff-wrapper {
          border-radius: 8px;
          overflow: hidden;
          box-shadow: 
            0 4px 20px rgba(0, 0, 0, 0.5),
            0 0 40px var(--neon-amber-glow);
          border: 2px solid transparent;
          background: 
            linear-gradient(var(--bg-primary), var(--bg-primary)) padding-box,
            linear-gradient(135deg, var(--neon-amber), var(--neon-cyan)) border-box;
          position: relative;
        }

        .code-diff-wrapper::before {
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

        .diff-header {
          display: grid;
          grid-template-columns: 1fr 1fr;
          background: var(--bg-secondary);
          border-bottom: 2px solid var(--neon-amber);
        }

        .diff-title {
          padding: 12px 20px;
          font-size: 14px;
          font-weight: 600;
          font-family: var(--font-mono);
          text-transform: uppercase;
          letter-spacing: 1px;
        }

        .diff-title.left {
          color: var(--neon-amber);
          border-right: 1px solid var(--bg-tertiary);
          text-shadow: 0 0 10px var(--neon-amber-glow);
        }

        .diff-title.right {
          color: var(--neon-cyan);
          text-shadow: 0 0 10px var(--neon-cyan-glow);
        }

        .diff-container {
          display: grid;
          grid-template-columns: 1fr 1fr;
          max-height: 600px;
          overflow: auto;
        }

        .diff-container::-webkit-scrollbar {
          width: 10px;
          height: 10px;
        }

        .diff-container::-webkit-scrollbar-track {
          background: var(--bg-secondary);
        }

        .diff-container::-webkit-scrollbar-thumb {
          background: linear-gradient(180deg, var(--neon-amber), var(--neon-cyan));
          border-radius: 5px;
        }

        .diff-pane {
          background: var(--bg-primary);
        }

        .left-pane {
          border-right: 1px solid var(--bg-tertiary);
        }

        .diff-line {
          display: flex;
          align-items: flex-start;
          font-family: var(--font-mono);
          font-size: 13px;
          line-height: 1.6;
          min-height: 21px;
        }

        .diff-line.removed {
          background: rgba(255, 191, 0, 0.08);
          border-left: 3px solid var(--neon-amber);
        }

        .diff-line.added {
          background: rgba(0, 240, 255, 0.08);
          border-left: 3px solid var(--neon-cyan);
        }

        .diff-line.unchanged {
          background: var(--bg-primary);
        }

        .line-number {
          min-width: 50px;
          padding: 2px 10px;
          text-align: right;
          color: var(--text-dim);
          user-select: none;
          background: rgba(0, 0, 0, 0.3);
          font-variant-numeric: tabular-nums;
        }

        .diff-line.removed .line-number {
          background: rgba(255, 191, 0, 0.15);
          color: var(--neon-amber);
          text-shadow: 0 0 5px var(--neon-amber-glow);
        }

        .diff-line.added .line-number {
          background: rgba(0, 240, 255, 0.15);
          color: var(--neon-cyan);
          text-shadow: 0 0 5px var(--neon-cyan-glow);
        }

        .line-marker {
          min-width: 20px;
          padding: 2px 5px;
          text-align: center;
          font-weight: bold;
          user-select: none;
        }

        .diff-line.removed .line-marker {
          color: var(--neon-amber);
          text-shadow: 0 0 8px var(--neon-amber-glow);
        }

        .diff-line.added .line-marker {
          color: var(--neon-cyan);
          text-shadow: 0 0 8px var(--neon-cyan-glow);
        }

        .line-content {
          flex: 1;
          padding: 2px 10px 2px 0;
          margin: 0;
          color: var(--text-primary);
          white-space: pre-wrap;
          word-break: break-all;
        }

        .diff-line.removed .line-content {
          color: var(--neon-amber);
          text-shadow: 0 0 3px var(--neon-amber-glow);
        }

        .diff-line.added .line-content {
          color: var(--neon-cyan);
          text-shadow: 0 0 3px var(--neon-cyan-glow);
        }

        @media (max-width: 768px) {
          .diff-container {
            grid-template-columns: 1fr;
          }

          .left-pane {
            border-right: none;
            border-bottom: 2px solid var(--neon-amber);
          }

          .diff-header {
            grid-template-columns: 1fr;
          }

          .diff-title.left {
            border-right: none;
            border-bottom: 1px solid var(--bg-tertiary);
          }
        }
      `}</style>
    </div>
  );
};

export default CodeDiff;
