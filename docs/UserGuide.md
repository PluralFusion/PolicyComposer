# PolicyComposer User Guide
This guide provides detailed instructions to set up, run, and customize PolicyComposer. The goal is to get you from a fresh repository to your first set of generated policy documents.

## Table of Contents
- [How It Works](#how-it-works)
- [Setup and Usage](#setup-and-usage)
  - [Method 1: The GitHub Action Workflow (Recommended)](#method-1-the-github-action-workflow-recommended)
  - [Method 2: Running the Build Locally (Advanced)](#method-2-running-the-build-locally-advanced)
- [Customizing Your Policies](#customizing-your-policies)
  - [Editing Configuration (`conf/config.yaml`)](#editing-configuration-confconfigyaml)
  - Editing Policy Content (`policies/*.md`)
- [Versioning Your Policies](#versioning-your-policies)
  - [Global Releases](#global-releases)
  - [Hotfixes](#hotfixes)

---

## How It Works
  - Global Releases
  - Hotfixes

## How It Works
The core workflow is simple:
1.  You edit text-based configuration files (`.yaml`) and policy templates (`.md`).
2.  You commit and push these changes to your private GitHub repository.
3.  A GitHub Action is automatically triggered, which uses your configuration to build the final Markdown and PDF documents.
4.  The finished documents are made available as downloadable `.zip` files (artifacts) in the GitHub Action results.

---

## Setup and Usage
There are two primary methods to use this project. We strongly recommend **Method 1** as it requires no local software installation (besides Git).

### Method 1: The GitHub Action Workflow (Recommended)
This is the easiest and most reliable method. You will use GitHub to do all the heavy lifting of document generation. This works on any operating system.

**IMPORTANT: To protect your company's sensitive configuration data, you must use a PRIVATE GitHub repository.**

#### Step 1: Create Your Private Repository from the Template

1.  Navigate to the [PolicyComposer repository on GitHub](https://github.com/PluralFusion/PolicyComposer).
2.  Click the green **"Use this template"** button.
3.  Select **"Create a new repository"**.
4.  Choose an owner and give your new repository a name (e.g., `my-company-policies`).
5.  **IMPORTANT: select `Private` for the visibility.** This is essential to protect your company's sensitive configuration data.
6.  Ensure **"Include all branches"** is checked.
7.  Click **"Create repository from template"**.

GitHub will create a new private repository for you, containing a copy of all the files from the template.

 
#### Step 2: Clone Your New Repository
On your local machine, open a terminal and clone the new private repository you just created.
```bash
# Replace with your details
git clone https://github.com/YOUR-USERNAME/YOUR-NEW-REPO.git
cd YOUR-NEW-REPO
```

#### Step 3: Configure Your Policies
This is where you'll customize the documents for your organization. All configuration files are in the `conf/` directory.

1.  **Create the Main Configuration:** Copy the example configuration file to create your own.
    ```bash
    cp conf/config-example.yaml conf/config.yaml
    ```
    Now, open `conf/config.yaml` in a text editor and fill in your company's specific information.

2.  **Set the Policy Order:** Open `conf/policy_order.yaml`. This file controls the exact order your policies will appear in the final combined PDF.

3.  **Map Usernames (Optional):** Open `conf/usermap.json`. This file maps Git usernames (like "todde") to a full name (like "Todd Emerson") for a cleaner look in the version history tables.

#### Step 4: Push Your Changes to GitHub
Commit your new configuration and push it to the `main` branch on GitHub.
```bash
git add conf/config.yaml
git commit -m "Initial policy configuration"
git push origin main
```

#### Step 5: Download Your Documents
Pushing to the `main` branch automatically triggers a GitHub Action.
1.  Go to your repository on GitHub and click the **"Actions"** tab.
2.  You will see a workflow running. Wait for it to complete (it will have a green checkmark).
3.  Click on the completed workflow run's title.
4.  Scroll down to the **"Artifacts"** section. You will find your generated documents in `.zip` files, ready to download.

---

### Method 2: Running the Build Locally (Advanced)
This method is for users who want to generate documents on their own machine without pushing changes to GitHub. It's faster for quick iterations but requires installing software on your system. This script is designed for **Linux and macOS**.

#### Step 1: Get the Project Code
First, you need to get the project files onto your local machine. It is **strongly recommended** that you create your own private repository from the template to prevent accidentally exposing sensitive configuration data.

1.  Follow "Step 1: Create Your Private Repository" from Method 1 above.
2.  On your local machine, open a terminal and clone the new private repository you just created.
    ```bash
    # Replace with your details
    git clone https://github.com/YOUR-USERNAME/YOUR-PRIVATE-REPO.git
    cd YOUR-PRIVATE-REPO
    ```

#### Step 2: Configure Your Policies
Follow "Step 3: Configure Your Policies" from Method 1 above to create and edit your `conf/config.yaml` and other configuration files.

#### Step 3: Install System Dependencies
The build script will check for these, but you must install them yourself using your system's package manager.
```bash
# On Debian/Ubuntu
sudo apt-get update
sudo apt-get install git pandoc texlive-latex-base python3-pip

# On macOS (using Homebrew)
brew install git pandoc mactex
```

#### Step 4: Run the Build Script
The `compose.sh` script will install the necessary Python packages and then build your documents.
```bash
# Make the script executable (you only need to do this once)
chmod +x scripts/compose.sh

# Run the script to generate your documents
./scripts/compose.sh
```

#### Step 5: Access Your Files
Once the script finishes, your generated documents will be available directly in the project folder:
-   Processed Markdown files are in the `md/` directory.
-   Generated PDF files are in the `pdf/` directory.
-   Processed Markdown files are in the `output/md/` directory.
-   Generated PDF files are in the `output/pdf/` directory.
-   Generated ODT files (for word processors) are in the `output/odt/` directory.

---

## Customizing Your Policies

### Editing Configuration (`conf/config.yaml`)
The `conf/config.yaml` file is the master control panel for all your policies. Open this file in a text editor to change company details, toggle compliance frameworks, manage vendors, and control document features.

The `conf/config-example.yaml` file is heavily commented to explain what each variable does. Use it as a reference when filling out your own `config.yaml`.

### Editing Policy Content (`policies/*.md`)
The policy documents themselves are Markdown files located in the `policies/` directory. You can edit these files directly to change wording, add sections, or remove content that doesn't apply to your organization.

These files use the **Jinja2 templating language** to insert variables and logic from your `config.yaml`. This allows the documents to be dynamic.

-   **Variables:** Use `{{ variable_name }}` to insert a value from your config. For example, `{{ company_name }}` will be replaced with "ACME LTD".
-   **Logic:** Use `{% if ... %}` statements to show or hide entire blocks of text. For example, a section wrapped in `{% if compliance_frameworks.hipaa %}` ... `{% endif %}` will only appear in the final document if `hipaa` is set to `true` in your config.

➡️ **For a detailed guide on using Jinja2, see the Templating Guide.**

---

## Versioning Your Policies
This system supports two types of versioning, controlled by your commits and your `config.yaml` file.

### Global Releases
This is the recommended method for major version changes. It stamps *all* documents with a new version number and creates an official GitHub Release.

*   **How to trigger:** Simply change the `release_version` variable in your `conf/config.yaml` (e.g., from `"v1.0.0"` to `"v1.1.0"`).
*   **What happens:** The build script detects the version change and adds a version entry to the history table of *every single policy document*.

### Hotfixes
This method adds a version history entry to *only* the specific file(s) you changed, without creating a global release. It's ideal for fixing typos or making minor clarifications.

*   **How to trigger:** Make a change to one or more policy files in the `policies/` directory.
*   **What to commit:** Commit the changed policy files with a message that **starts with** the `release_commit_prefix` from your config (e.g., `"RELEASE:"`).
    ```bash
    git commit -m "RELEASE: Fixed typo in Risk Management Policy"
    ```
*   **What happens:** The build script sees the commit prefix and adds this commit *only* to the history table of the file(s) you changed.
