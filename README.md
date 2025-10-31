# PolicyComposer: A Company Policy Document Engine

This repository provides a complete build system for creating, managing, and versioning company policies. It uses a [Jinja2](https://jinja.palletsprojects.com/en/stable/) templating engine, a Python build script, and GitHub Actions to automatically generate versioned MD and PDF policy documents.

## Original Content Attribution

The policy templates in the `policies/` directory were originally based on the Catalyze HIPAA Compliance Policies by Catalyze, Inc. which [were originally available on GitHub](https://github.com/catalyzeio/policies/) -- and [apparently live on in forks](https://github.com/globerhofer/HIPAA-policies). These are licensed under a  Creative Commons Attribution-ShareAlike 4.0 International License.

## How to Use This Project
There are two ways to generate your policy documents:

1. **GitHub Action (Recommended):** This is the easiest method. You push your changes to GitHub, and a pre-configured virtual machine builds your documents and provides them as downloadable .zip files. This works on any operating system.

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
The conf/ directory contains all the files needed to customize your policies.

- **Main Configuration:** Copy the example config to create your private config. 
   ```bash 
   cp conf/config-example.yaml conf/config.yaml  
   ```
  Now, edit conf/config.yaml and fill in all your company's specific information (names, emails, compliance toggles, etc.)

- **Policy Order:** Open `conf/policy_order.yaml`. This file controls the exact order that your policies appear in the final combined PDF.

- **User Map (Optional):** Open conf/usermap.json. This maps Git usernames (e.g., "todde") to a full name (e.g., "Todd Emerson") for the version history table.

#### Step 4: Edit Your Policies
Modify the source .md files in the `policies/` directory. You can use Jinja2  
syntax (e.g., `{{ company\_name }}` or `{% if hipaa %}...{% endif %}`)  
to insert variables or logic from your config.yaml. <br/>**See the [Templating Guide](https://www.google.com/search?q=docs/templating_guide.md) for detailed examples.**

#### **Step 5: Push to Your Private Repository**
Change the Git remote to point to the new private repository you created in Step 1\.  
```bash
git remote set-url origin https://github.com/YOUR-USERNAME/YOUR-PRIVATE-REPO.git  
git push \-u origin main  
```
Pushing to the main branch will automatically trigger the GitHub Action.

#### **Step 6: Download Your Documents**
When the action is complete (a green checkmark on your commit), go to your  
repository's "Actions" tab and click on the latest workflow run. You will find  
your processed documents available to download as "Artifacts":

- **processed-markdown-policies**: A .zip of the final .md files.
- **policy-pdfs**: A .zip containing the individual .pdf files and combined\_policies.pdf.
- **available-fonts**: A font\_list.txt file showing all fonts you can use in your config.

### **Method 2: Running the Build Locally (Advanced - NOT FULLY TESTED)**
This method is for **Linux and macOS** users who want to build and test documents on their local machine without pushing to GitHub.

#### **Step 1: Install Dependencies**

The build script scripts/compose.sh will check for dependencies, but it cannot install system-level tools for you. You must first install:

- **Python 3** & **Pip 3**
- **Git**
- **Pandoc**
- **A LaTeX Distribution:**
  - On macOS: brew install \--cask mactex
  - On Debian/Ubuntu: sudo apt-get install texlive-latex-base

#### **Step 2: Run the Composer Script**

The compose.sh script will automatically check for any missing dependencies and Python packages (like PyYAML or Jinja2) and ask to install them. It will then build all the documents.

1. **Make the script executable** (you only need to do this once):  
  chmod \+x scripts/compose.sh
2. **Run the script** from the root of the project:  
  ./scripts/compose.sh

#### **Step 3: Access Your Files**

The script will run the exact same build process as the GitHub Action. When it's finished, you won't get "artifacts." Instead, the files will be placed directly in your project folder:

- The processed markdown files will be in the md/ directory.
- The generated PDFs will be in the pdf/ directory.

## **Configuration Overview**

The core of this engine is the conf/config.yaml file, which acts as a master  
control panel for all your policies.

- **Company Variables:** Basic text replacement for names, emails, etc.
- **PDF Metadata:** Sets the title, author, and font for the PDFs.
- **Feature Toggles:** Booleans (true/false) to show/hide entire sections (e.g., show\_internal\_notes).
- **Service Types:** Nested objects to control content based on your offerings (e.g., service\_types.paas.enabled).
- **Compliance Frameworks:** Nested objects to show/hide policy sections based on framework (e.g., compliance\_frameworks.hipaa).
- **Revision History Toggles:** Controls whether the Git history is appended to the final documents.

## **Version History Control**

The build script generates a version history table at the end of your documents if you have `..._show_revision_history`: true in your config.  
By default, this table is populated only by commits that start with a specific prefix (default is RELEASE:). This keeps your history clean of minor typo fixes.

- **To version-stamp ONE file:** Make your changes to that file and commit with the prefix.  
  git commit \-m "RELEASE: v1.1 update to risk policy"
- **To version-stamp ALL files (e.g., for a major release):** Make a commit that *only* changes the `conf/config.yaml` file (e.g., update a version number or add a comment) and use the RELEASE: prefix.  
   ```bash
  git commit -m "RELEASE: v2.0 - 2025 Annual Policy Review"  
  ```
  The script will see this config-only change and apply this commit to *every document's* history table.

## **Template Documentation**
The markdown documents are formatted to be updated based on changes to the \`conf/config.yaml\` file. 

- **Templating:** For a detailed guide on using Jinja2 logic (if, for, etc.), see [docs/templating\_guide.md](https://www.google.com/search?q=docs/templating_guide.md).
- **Config Validation:** This project includes a script to help you check your config for errors. See [docs/CONFIG\_VALIDATION.md](https://www.google.com/search?q=docs/CONFIG_VALIDATION.md) for details.

## **License**

This project uses a hybrid licensing model:

- **The Software** (all .py, .yml, .github/workflows files) is licensed under the MIT License.
- **The Content** (the .md policy files) is licensed under the CC BY-SA 4.0 License, as it is a derivative of the original Catalyze policies.

See the [LICENSE.md](http://docs.google.com/license.md) file for full details.