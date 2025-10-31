# PolicyComposer: A Company Policy Document Engine

This repository provides a complete build system for creating, managing, and versioning company policies. It uses a [Jinja2](https://jinja.palletsprojects.com/en/stable/) templating engine, a Python build script, and GitHub Actions to automatically generate versioned MD and PDF policy documents.

## Original Content Attribution

The policy templates in the `policies/` directory were originally based on the Catalyze HIPAA Compliance Policies by Catalyze, Inc. which [were originally available on GitHub](https://github.com/catalyzeio/policies/) -- and [apparently live on in forks](https://github.com/globerhofer/HIPAA-policies). These are licensed under a  Creative Commons Attribution-ShareAlike 4.0 International License.

## How to Use This Project
There are two ways to generate your policy documents:

1. **GitHub Action (Recommended):** This is the easiest method. You push your changes to GitHub, and a pre-configured virtual machine builds your documents and provides them as downloadable **.zip** files. This works on any operating system.

2. **Run Locally (Advanced):** This method runs the build scripts directly on your own computer. This is faster but requires you to install all the necessary dependencies. This script is designed for **Linux and macOS** users; it is **not supported on Windows**.

### Method 1: GitHub Action (Recommended)

**You SHOULD only use this template in a new, PRIVATE repository to protect your configuration.**

#### Step 1: Create a New Private Repository
On GitHub, create a new repository. Make sure to select **Private** for the visibility.

#### Step 2: Clone This Template Repository
Clone this PolicyComposer repository to your local machine.  
```bash
git clone https://github.com/PluralFusion/PolicyComposer.git
```

#### Step 3: Create Your Private Configuration
The `conf/` directory contains all the files needed to customize your policies.

- **Main Configuration:** Copy the example config to create your private config. 
   ```bash 
   cp conf/config-example.yaml conf/config.yaml  
   ```
  Now, edit conf/config.yaml and fill in all your company's specific information (names, emails, compliance toggles, etc.)

- **Policy Order & Titles:** Open `conf/policy_order.yaml`. This file controls the exact order that your policies appear in the final combined PDF. You can also set a friendly `title` for each document, which will be used as the title of the individual PDF.

- **User Map (Optional):** Open conf/usermap.json. This maps Git usernames (e.g., "todde") to a full name (e.g., "Todd Emerson") for the version history table.

#### Step 4: Edit Your Policies
Modify the source .md files in the `policies/` directory. You can use Jinja2  
syntax (e.g., `{{ company\_name }}` or `{% if hipaa %}...{% endif %}`)  
to insert variables or logic from your config.yaml. <br/>**See the [Templating Guide](docs/templating_guide.md) for detailed examples.**

#### **Step 5: Push to Your Private Repository**
Change the Git remote to point to the new private repository you created in Step 1\.  
```bash
git remote set-url origin https://github.com/YOUR-USERNAME/YOUR-PRIVATE-REPO.git  
git push \-u origin main  
```
Pushing to the main branch will automatically trigger the GitHub Action.

#### **Step 6: Download Your Documents**
When the action is complete (a green checkmark on your commit), go to your  
repository's **"Actions"** tab and click on the latest workflow run. You will find  
your processed documents available to download as **"Artifacts"**:

- **processed-markdown-policies**: A **.zip** of the final **.md **files.
- **policy-pdfs**: A **.zip** containing the individual **.pdf** files and **`combined_policies.pdf`**.
- **available-fonts**: A **font\_list.txt** file showing all fonts you can use in your config.

### **Method 2: Running the Build Locally (Advanced - NOT FULLY TESTED)**
This method is for **Linux and macOS** users who want to build and test documents on their local machine without pushing to GitHub.

#### **Step 1: Install Dependencies**

The build script `cripts/compose.sh`will check for dependencies, but it cannot install system-level tools for you. You must first install:

- **Python 3** & **Pip 3**
- **Git**
- **Pandoc**
- **A LaTeX Distribution:**
  - On macOS: `brew install --cask mactex`
  - On Debian/Ubuntu: `sudo apt-get install texlive-latex-base`

#### **Step 2: Run the Composer Script**

The `compose.sh` script will automatically check for any missing dependencies and Python packages (like PyYAML or Jinja2) and ask to install them. It will then build all the documents.

1. **Make the script executable** (you only need to do this once):  
  ```bash
  chmod \+x scripts/compose.sh
  ```
2. **Run the script** from the root of the project:  
  ```bash
  ./scripts/compose.sh
  ```

#### **Step 3: Access Your Files**
The script will run the exact same build process as the GitHub Action. When it's finished, you won't get "artifacts." Instead, the files will be placed directly in your project folder:

- The processed markdown files will be in the `md/` directory.
- The generated PDFs will be in the `pdf/` directory.

## **Configuration Overview**

The core of this engine is the `conf/config.yaml` file, which acts as a master  
control panel for all your policies.

- **Company Variables:** Basic text replacement for names, emails, etc.
- **PDF Metadata:** Sets the title, author, and fonts (main text, headers, and code blocks) for the PDFs.
- **Feature Toggles:** Booleans (true/false) to show/hide entire sections (e.g., `show_internal_notes`).
- **Service Types:** Nested objects to control content based on your offerings (e.g., `service_types.paas.enabled`).
- **Compliance Frameworks:** Nested objects to show/hide policy sections based on framework (e.g., `compliance_frameworks.hipaa`).
- **Revision History Toggles:** Controls whether the Git history is appended to the final documents.
- **Version History Style:** Controls how the version history table is generated during a Global Release (`append` or `replace`).

### How Version History Works
This system supports two types of versioning, both of which are controlled by your `conf/config.yaml` settings.

#### 1. Global Release (Recommended Method)
This stamps *all* documents with a new version and creates an official GitHub Release with your PDFs.

* **How to trigger:** Simply change the `release_version` variable in your `conf/config.yaml` (e.g., from `"v1.0.0"` to `"v1.1.0"`).
* **What to commit:** Commit the `conf/config.yaml` file. The commit message doesn't matter, but using the version number (e.g., `"v1.1.0"`) is good practice.
* **What happens:** The build script detects that `release_version` has changed. It adds this *one* commit to the history table of *every single policy document* and creates a new GitHub Release.

#### 2. History Display Style (Global Releases Only)
You can control how a Global Release affects the version history table using the `global_release_history_style` setting in `conf/config.yaml`:
- **`append` (Default):** The new global release version is added to the top of the existing history. This maintains a complete audit trail within the document.
- **`replace`:** The history table is wiped clean and shows *only* the new global release version. This is useful for major releases where you want to present a clean slate.

#### 3. Hotfix Release (For single files)
This adds a version history entry to *only* the specific file(s) you changed, without creating a global release.

* **How to trigger:** Make a change to one or more policy files in the `policies/` directory.
* **What to commit:** Commit the changed policy files with a message that **starts with** your `release_commit_prefix` (e.g., `"RELEASE:"`).
    ```bash
    git commit -m "RELEASE: Fixed typo in risk_management_policy"
    ```
* **What happens:** The build script sees this commit, checks the prefix, and adds this commit *only* to the history table of the `risk_management_policy`. It does **not** create a GitHub Release.

## **Template Documentation**
The markdown documents are formatted to be updated based on changes to the \`conf/config.yaml\` file. 

- **Templating:** For a detailed guide on using Jinja2 logic (if, for, etc.), see [docs/templating_guide.md](docs/templating_guide.md).
- **Config Validation:** This project includes a script to help you check your config for errors. See [docs/CONFIG_VALIDATION.md](docs/CONFIG_VALIDATION.md) for details.

## **License**

This project uses a hybrid licensing model:

- **The Software** (all .py, .yml, .github/workflows files) is licensed under the MIT License.
- **The Content** (the .md policy files) is licensed under the CC BY-SA 4.0 License, as it is a derivative of the original Catalyze policies.

See the [LICENSE.md](LICENSE.md) file for full details.