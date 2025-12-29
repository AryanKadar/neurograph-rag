@echo off
REM ═══════════════════════════════════════════════════════════════
REM  🌌 COSMIC AI - Frontend Startup Script
REM ═══════════════════════════════════════════════════════════════

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║   ██████╗ ██████╗ ███████╗███╗   ███╗██╗ ██████╗              ║
echo ║  ██╔════╝██╔═══██╗██╔════╝████╗ ████║██║██╔════╝              ║
echo ║  ██║     ██║   ██║███████╗██╔████╔██║██║██║                   ║
echo ║  ██║     ██║   ██║╚════██║██║╚██╔╝██║██║██║                   ║
echo ║  ╚██████╗╚██████╔╝███████║██║ ╚═╝ ██║██║╚██████╗              ║
echo ║   ╚═════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝ ╚═════╝              ║
echo ║                                                               ║
echo ║         🎨 FRONTEND STARTUP SCRIPT                            ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0Frontend\\cosmic-chat-ai-main\\cosmic-chat-ai-main"

REM ─────────────────────────────────────────────────────────────
REM  Check if node_modules exists
REM ─────────────────────────────────────────────────────────────
echo [*] Checking node_modules...

if not exist "node_modules" (
    echo [!] node_modules not found. Installing dependencies...
    npm install --loglevel=error
    echo [+] Dependencies installed!
) else (
    echo [+] Dependencies OK
)

REM ─────────────────────────────────────────────────────────────
REM  Start the dev server
REM ─────────────────────────────────────────────────────────────
echo.
echo ═══════════════════════════════════════════════════════════════
echo   🎨 Starting Cosmic AI Frontend Server...
echo   🌐 App: http://localhost:3000
echo   ✨ Professional UI with markdown rendering
echo ═══════════════════════════════════════════════════════════════
echo.

npm run dev

pause
