@echo off
echo 🚀 Multi-Agent Research Assistant
echo ====================================

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if OpenAI API key is set
if "%OPENAI_API_KEY%"=="" (
    echo ⚠️  WARNING: OPENAI_API_KEY environment variable not set!
    echo Please set your OpenAI API key:
    echo set OPENAI_API_KEY=your-api-key-here
    pause
    exit /b 1
)

echo ✅ OpenAI API key found
echo.
echo 🌐 Starting server...
echo API: http://localhost:8000
echo Frontend: http://localhost:8000/app  
echo Docs: http://localhost:8000/docs
echo.
echo ====================================

python server.py 