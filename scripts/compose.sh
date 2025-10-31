#!/bin/bash
# A script to run the PolicyComposer build process locally.
# Includes dependency checking.

# --- 1. Dependency Checking ---
echo "--- Checking Dependencies ---"

# Arrays to hold missing dependencies
MISSING_COMMANDS=()
MISSING_COMMAND_HINTS=()
MISSING_PY_PKGS=()

# Function to check for a command-line tool
check_command() {
    COMMAND=$1
    INSTALL_HINT=$2
    if ! command -v $COMMAND &> /dev/null
    then
        MISSING_COMMANDS+=("$COMMAND")
        MISSING_COMMAND_HINTS+=("$INSTALL_HINT")
    fi
}

# Function to check for a Python package
check_python_package() {
    PACKAGE_NAME=$1
    IMPORT_NAME=$2
    python3 -c "import $IMPORT_NAME" &> /dev/null
    if [ $? -ne 0 ]; then
        MISSING_PY_PKGS+=("$PACKAGE_NAME")
    fi
}

# Check all system commands
check_command "python3" "Debian/Ubuntu: sudo apt-get install python3  |  macOS: brew install python"
check_command "pip3"    "Debian/Ubuntu: sudo apt-get install python3-pip |  macOS: brew install python"
check_command "git"     "Debian/Ubuntu: sudo apt-get install git     |  macOS: brew install git"
check_command "pandoc"  "Debian/Ubuntu: sudo apt-get install pandoc  |  macOS: brew install pandoc"
check_command "pdflatex" "Debian/Ubuntu: sudo apt-get install texlive-latex-base | macOS: brew install --cask mactex"

# Check all Python packages
check_python_package "PyYAML" "yaml"
check_python_package "Jinja2" "jinja2"

# --- 2. Report Missing Dependencies ---
# Check if any dependencies are missing
if [ ${#MISSING_COMMANDS[@]} -ne 0 ] || [ ${#MISSING_PY_PKGS[@]} -ne 0 ]; then
    echo "ERROR: Missing required dependencies. Please install the following:"
    echo ""
    
    # Print missing system commands
    if [ ${#MISSING_COMMANDS[@]} -ne 0 ]; then
        echo "Missing system commands:"
        for (( i=0; i<${#MISSING_COMMANDS[@]}; i++ )); do
            echo "  - Command: '${MISSING_COMMANDS[$i]}'"
            echo "    Install hint: ${MISSING_COMMAND_HINTS[$i]}"
        done
        echo ""
    fi
    
    # Print missing Python packages
    if [ ${#MISSING_PY_PKGS[@]} -ne 0 ]; then
        echo "Missing Python packages:"
        echo "  - Run the following command to install them:"
        echo "    pip3 install ${MISSING_PY_PKGS[*]}"
        echo ""
    fi
    
    exit 1
else
    echo "All dependencies satisfied."
    echo ""
fi

# --- 3. Get Current Commit Info ---
# This mimics the environment variables set by the GitHub Action.
echo "Getting latest commit info..."
export CURRENT_COMMIT_SHA=$(git rev-parse HEAD)
export CURRENT_COMMIT_ACTOR=$(git log -1 --pretty=format:'%an')
export CURRENT_COMMIT_MSG=$(git log -1 --pretty=format:'%s')

# --- 4. Run the Git History Script ---
echo "--- Running get_git_history.py ---"
python3 scripts/get_git_history.py
if [ $? -ne 0 ]; then
    echo "ERROR: get_git_history.py failed."
    exit 1
fi

# --- 5. Run the Main Build Script ---
echo "--- Running process_policies.py ---"
python3 scripts/process_policies.py
if [ $? -ne 0 ]; then
    echo "ERROR: process_policies.py failed."
    exit 1
fi

echo "---"
echo "Build complete. Output is in 'md/' and 'pdf/' directories."
