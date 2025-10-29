# PolicyComposer: A Company Policy Document Engine
This repository provides a complete build system for creating, managing, and versioning company policies. It uses a Jinja2 templating engine, a Python build script, and GitHub Actions to automatically generate versioned MD and PDF policy documents.

## Original Content Attribution

The policy templates in the `/policy` directory are based on the  
[Catalyze HIPAA Compliance Policies](https://github.com/globerhofer/HIPAA-policies) by Catalyze, Inc., which are licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.

## !! IMPORTANT: How to Use This Project !!

**NOTE:** This repository is a **template**. The GitHub Action build process requires that you commit and push your `conf/config.yml` file, which will contain your company's private information.

**You MUST use this template in a new, PRIVATE repository to protect your configuration.**


1. **Create a New PRIVATE Repository**
On GitHub, create a new repository and make sure to select Private in the visibility settings.

2. **Clone the Repository**  
   `git clone https://github.com/PluralFusion/PolicyComposer`

3. **Configure Your Company**
   Copy the example config file to create your own config.
   ```bash
   cp conf/config_example.yml conf/config.yml
   ```

4. **Edit Your Config**
   Open `conf/config.yml` (the new file) and fill in all your company's specific information (names, emails, compliance toggles, etc.). You can add any values that you'd like to include in your policy documentation.

3. **Edit Policies**
   Modify the source files in the `/policy` directory. You can use Jinja2  
   syntax (e.g.,  `{{ company_name }}` or   `{% if hipaa %}` ...   `{% endif %} `)  
   to insert variables or logic from your config.yml.  
   **See the [Templating Guide](/docs/templating_guide.md) for detailed examples.**  

4. **Define Policy Order**
   Edit `/conf/policy_order.txt` to list the markdown filenames from the  
   `/policy` directory in the exact order you want them to appear in the  
   combined PDF.  

5. **Push Changes**
   Commit and push your changes to the main branch. A GitHub Action will  
   automatically run.  

6. **Download Your Documents** 
   When the action is complete (a green checkmark on your commit), go to the  
   "Actions" tab and click on the latest workflow run. You will find your  
   processed documents as "Artifacts":  
   * **processed-markdown-policies**: A .zip of the final .md files.  
   * **policy-pdfs**: A .zip containing both the individual .pdf files and the final `combined_policies.pdf`.

## Configuration Overview
The core of this engine is the `conf/config.yml` file, which acts as a master  
control panel for all your policies. The build script passes all variables  
from this file into the Jinja2 templating engine.  
This file controls:

* Company-specific variables (names, emails, etc.)  
* PDF metadata (titles, authors)  
* Feature toggles (e.g., show_internal_notes)  
* Service type toggles (e.g., PaaS, SaaS)  
* Compliance framework toggles (e.g., hipaa, soc2)  
* Revision history toggles

For a detailed guide on how to use these variables with Jinja2, please see the  
Templating Guide.

## **License**
This project uses a hybrid licensing model:

* **The Software** (all .py, .yml, .github/workflows files) is licensed under the MIT License.  
* **The Content** (the .md policy files) is licensed under the CC BY-SA 4.0 License, as it is a derivative of the original Catalyze policies.

See the [LICENSE.md](LICENSE.md) file for full details.