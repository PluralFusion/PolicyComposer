#!/bin/bash
set -e

# --- Configuration Variables ---
CONFIG_FILE="conf/config.yaml"
HISTORY_SCRIPT="scripts/get_git_history.py"
BUILD_SCRIPT="scripts/process_policies.py"
RELEASE_VERSION_KEY="release_version:" # The YAML key to check for versions

# --- 1. Dependency Checks ---
echo "Checking dependencies..."
declare -A deps
deps=(
    [python3]="Python 3"
    [pip3]="Python Pip"
    [git]="Git"
    [pandoc]="Pandoc"
    [pdflatex]="LaTeX (for Pandoc PDF generation)"
)

missing_deps=()
for cmd in "${!deps[@]}"; do
    if ! command -v "$cmd" &> /dev/null; then
        missing_deps+=("${deps[$cmd]} (command: $cmd)")
    fi
done

if [ ${#missing_deps[@]} -gt 0 ]; then
    echo "------------------------------------------------------------"
    echo "ERROR: Missing system dependencies. Please install them."
    for dep in "${missing_deps[@]}"; do
        echo "  - $dep"
    done
    echo ""
    echo "Install hints:"
    echo "  - macOS:   brew install git pandoc mactex"
    echo "  - Ubuntu:  sudo apt-get install git pandoc texlive-latex-base"
    echo "------------------------------------------------------------"
    exit 1
fi

# --- 2. Python Package Checks ---
echo "Checking Python packages..."
# We check for the *modules*, not the package names
PY_DEPS=( "yaml" "jinja2" )
PY_DEPS_NAMES=( "PyYAML" "Jinja2" )
missing_py_deps=()

for i in "${!PY_DEPS[@]}"; do
    if ! python3 -c "import ${PY_DEPS[$i]}" &> /dev/null; then
        missing_py_deps+=("${PY_DEPS_NAMES[$i]}")
    fi
done

if [ ${#missing_py_deps[@]} -gt 0 ]; then
    echo "Missing Python packages: ${missing_py_deps[*]}"
    read -p "Install them now with pip3? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip3 install "${missing_py_deps[@]}"
    else
        echo "Aborting. Please install packages manually."
        exit 1
    fi
fi
echo "Dependencies OK."

# --- 3. Set Build Environment Variables (Mimic GitHub Action) ---

echo "Setting local build environment..."

# Get current commit info from local git
export CURRENT_COMMIT_SHA=$(git log -1 --pretty=format:%H)
export CURRENT_COMMIT_ACTOR=$(git log -1 --pretty=format:%an)
export CURRENT_COMMIT_MSG=$(git log -1 --pretty=format:%s)

# --- Check for Global Release ---
export IS_GLOBAL_RELEASE="false"

# Check if config.yaml was part of the last commit
# Use '|| true' to prevent failure on first commit (no HEAD~1)
if git diff --name-only HEAD~1 HEAD 2>/dev/null | grep -q "$CONFIG_FILE"; then
  echo "$CONFIG_FILE was changed in the last commit."
  
  # Get old and new version values from git
  # Use '|| echo "none"' to handle file not existing in HEAD~1
  OLD_VERSION=$(git show HEAD~1:"$CONFIG_FILE" 2>/dev/null | grep "$RELEASE_VERSION_KEY" | awk '{print $2}' | tr -d '"' || echo "none")
  NEW_VERSION=$(grep "$RELEASE_VERSION_KEY" "$CONFIG_FILE" | awk '{print $2}' | tr -d '"')
  
  if [ "$OLD_VERSION" != "$NEW_VERSION" ] && [ -n "$NEW_VERSION" ]; then
    echo "Global release detected! Version changed from $OLD_VERSION to $NEW_VERSION."
    export IS_GLOBAL_RELEASE="true"
  else
    echo "$CONFIG_FILE changed, but release_version is the same."
  fi
else
  echo "$CONFIG_FILE was not changed. This is not a global release."
fi
# --- End Check for Global Release ---


# --- 4. Run Build Scripts ---
echo "Running git history export..."
python3 "$HISTORY_SCRIPT"

echo "Running policy build process..."
python3 "$BUILD_SCRIPT"

echo "------------------------------------------------------------"
echo "Build complete."
echo "Your files are available in the 'md/' and 'pdf/' directories."
echo "------------------------------------------------------------"

