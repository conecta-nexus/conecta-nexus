@echo off
setlocal EnableExtensions DisableDelayedExpansion

where git >nul 2>&1
if errorlevel 1 (
    echo Error: Git was not found in PATH. Install Git for Windows and try again.
    exit /b 1
)

set "ORG_NAME=conecta-nexus"
set "PREFERRED_BRANCH=develop"
set "FALLBACK_BRANCH=main"
set "PROTOCOL=https"
for %%I in ("%~dp0..") do set "WORKSPACE_DIR=%%~fI"
set /a CLONED=0
set /a UPDATED=0
set /a PROTECTED=0
set /a ERRORS=0

:parse_arguments
if "%~1"=="" goto arguments_done
if /i "%~1"=="--https" goto set_https
if /i "%~1"=="--ssh" goto set_ssh
if /i "%~1"=="--branch" goto set_branch
if /i "%~1"=="-b" goto set_branch
if /i "%~1"=="--help" goto show_help
if /i "%~1"=="-h" goto show_help

echo Error: Unknown option "%~1".
call :usage
exit /b 2

:set_https
set "PROTOCOL=https"
shift
goto parse_arguments

:set_ssh
set "PROTOCOL=ssh"
shift
goto parse_arguments

:set_branch
if "%~2"=="" (
    echo Error: --branch requires a branch name.
    call :usage
    exit /b 2
)
set "PREFERRED_BRANCH=%~2"
shift
shift
goto parse_arguments

:show_help
call :usage
exit /b 0

:arguments_done
echo ================================================================
echo             CONECTA NEXUS - WORKSPACE SETUP
echo ================================================================
echo Organization: github.com/%ORG_NAME%
echo Protocol:     %PROTOCOL%
echo Target branch: %PREFERRED_BRANCH% (fallback: %FALLBACK_BRANCH%)
echo Workspace:    %WORKSPACE_DIR%
echo ----------------------------------------------------------------

for %%R in (frontend gateway auth profile challenge application moderation notification infra) do call :process_repository "%%R"

echo.
echo ================================================================
echo                       FINAL SUMMARY
echo ================================================================
echo Repositories cloned:                 %CLONED%
echo Existing repositories updated:       %UPDATED%
echo Repositories skipped to protect work: %PROTECTED%
echo Repositories with errors:             %ERRORS%
echo ================================================================

if %ERRORS% equ 0 (
    echo All repositories are ready.
    exit /b 0
)

echo One or more repositories could not be processed. Review the messages above.
exit /b 1

:process_repository
set "REPOSITORY=%~1"
set "TARGET_DIR=%WORKSPACE_DIR%\%REPOSITORY%"

echo.
echo Processing repository: %REPOSITORY%

if not exist "%TARGET_DIR%\" goto clone_repository

if not exist "%TARGET_DIR%\.git\" goto invalid_repository

echo Repository directory exists. Fetching remote updates...
git -C "%TARGET_DIR%" fetch --all --prune
if errorlevel 1 (
    echo Error: Fetch failed for %REPOSITORY%.
    set /a ERRORS+=1
)

set "CURRENT_BRANCH="
for /f "delims=" %%B in ('git -C "%TARGET_DIR%" branch --show-current 2^>nul') do set "CURRENT_BRANCH=%%B"
if not defined CURRENT_BRANCH (
    echo Current local branch: detached HEAD
) else (
    echo Current local branch: %CURRENT_BRANCH%
)

set "STATUS_FILE=%TEMP%\conecta-nexus-setup-%RANDOM%-%RANDOM%.tmp"
git -C "%TARGET_DIR%" status --porcelain > "%STATUS_FILE%"
if errorlevel 1 goto status_error

set "HAS_CHANGES="
for /f "usebackq delims=" %%S in ("%STATUS_FILE%") do set "HAS_CHANGES=1"
del /q "%STATUS_FILE%" >nul 2>&1

if defined HAS_CHANGES goto protect_local_work

git -C "%TARGET_DIR%" pull --ff-only
if errorlevel 1 goto pull_error

echo Repository %REPOSITORY% updated successfully.
set /a UPDATED+=1
goto :eof

:clone_repository
if /i "%PROTOCOL%"=="ssh" (
    set "REPOSITORY_URL=git@github.com:%ORG_NAME%/%REPOSITORY%.git"
) else (
    set "REPOSITORY_URL=https://github.com/%ORG_NAME%/%REPOSITORY%.git"
)

echo Cloning from %REPOSITORY_URL%...
git clone "%REPOSITORY_URL%" "%TARGET_DIR%"
if errorlevel 1 goto clone_error

set "SELECTED_BRANCH="
git -C "%TARGET_DIR%" show-ref --verify --quiet "refs/remotes/origin/%PREFERRED_BRANCH%"
if not errorlevel 1 set "SELECTED_BRANCH=%PREFERRED_BRANCH%"

if not defined SELECTED_BRANCH (
    git -C "%TARGET_DIR%" show-ref --verify --quiet "refs/remotes/origin/%FALLBACK_BRANCH%"
    if not errorlevel 1 set "SELECTED_BRANCH=%FALLBACK_BRANCH%"
)

if not defined SELECTED_BRANCH goto clone_without_configured_branch

git -C "%TARGET_DIR%" checkout --quiet -B "%SELECTED_BRANCH%" "origin/%SELECTED_BRANCH%"
if errorlevel 1 goto clone_branch_error
git -C "%TARGET_DIR%" branch --set-upstream-to="origin/%SELECTED_BRANCH%" "%SELECTED_BRANCH%" >nul
if errorlevel 1 goto clone_branch_error

echo Branch configured and tracking origin/%SELECTED_BRANCH%.
set /a CLONED+=1
echo Repository %REPOSITORY% cloned successfully.
goto :eof

:clone_without_configured_branch
echo Warning: Neither "%PREFERRED_BRANCH%" nor "%FALLBACK_BRANCH%" exists on origin. Keeping the branch selected by git clone.
set /a CLONED+=1
echo Repository %REPOSITORY% cloned successfully.
goto :eof

:invalid_repository
echo Error: "%TARGET_DIR%" exists but does not contain a .git directory. It was not modified.
set /a ERRORS+=1
goto :eof

:protect_local_work
echo Warning: Local changes detected; skipping %REPOSITORY% to protect local work.
set /a PROTECTED+=1
goto :eof

:status_error
del /q "%STATUS_FILE%" >nul 2>&1
echo Error: Could not inspect the working tree for %REPOSITORY%.
set /a ERRORS+=1
goto :eof

:pull_error
echo Warning: Fast-forward-only pull failed for %REPOSITORY%. No merge, rebase, reset, or force operation was attempted.
set /a ERRORS+=1
goto :eof

:clone_error
echo Error: Could not clone %REPOSITORY%. Check network access and repository permissions.
set /a ERRORS+=1
goto :eof

:clone_branch_error
echo Error: %REPOSITORY% was cloned, but branch "%SELECTED_BRANCH%" could not be configured to track its origin branch.
set /a CLONED+=1
set /a ERRORS+=1
goto :eof

:usage
echo Usage: setup.bat [options]
echo.
echo Options:
echo   --https       Clone using HTTPS (default)
echo   --ssh         Clone using SSH
echo   --branch NAME Set the preferred branch (default: develop)
echo   -b NAME       Alias for --branch
echo   --help        Display this help message
echo   -h            Alias for --help
exit /b