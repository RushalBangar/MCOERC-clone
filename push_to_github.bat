@echo off
title Push MCOERC Updates to GitHub
echo ======================================================================
echo                 Pushing MCOERC Updates to GitHub
echo ======================================================================
echo.

cd /d "%~dp0"

echo [1/3] Staging changes...
git add .
echo Done.
echo.

echo [2/3] Committing and standardizing codebase...
git commit -m "refactor: clean up legacy artifacts, fix blockquote nested footers, and standardize copyright year to 2026"
echo Done.
echo.

echo [3/3] Pushing changes to GitHub...
git push
echo.
echo ======================================================================
echo   SUCCESS: MCOERC changes have been successfully pushed to GitHub!
echo ======================================================================
echo.
pause

:: Delete itself
(goto) 2>nul & del "%~f0"
