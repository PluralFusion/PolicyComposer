# PolicyComposer: A Company Policy Document Engine

This repository provides a complete build system for creating, managing, and versioning
company policies. It uses a Jinja2 templating engine, a Python build script,
and GitHub Actions to automatically generate versioned MD and PDF policy documents.

## Original Content Attribution

The policy templates in the `policies/` directory are based on the
[Catalyze HIPAA Compliance Policies](https://github.com/globerhofer/HIPAA-policies)
by Catalyze, Inc., which are licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

## !! IMPORTANT: How to Use This Project !!

**NOTE:** This repository is a **template**. The GitHub Action build process requires that you commit and push your configuration files (like `conf/config.yaml`), which will contain your company's private information.

**You MUST use this template in a new, PRIVATE repository to protect your configuration.**

## Step-by-Step Instructions

### Step 1: Create a New Private Repository

On GitHub, create a new repository. Make sure to select **Private** for the visibility.

### Step 2: Clone This Template Repository

Clone this `PolicyComposer` repository to your local machine.
```bash
git clone https://github.com/PluralFusion/PolicyComposer.git
```

*Note: You will later change the remote URL to point to your new private repository.*

### Step 3: Create Your Private Configuration

The `conf/` directory contains all the files needed to customize your policies.

1. **Main Configuration:** Copy the example config to create your private config.

```bash
cp conf/config-example.yaml conf/config.yaml
```

Now, edit `conf/config.yaml` and fill in all your company's specific information (names, emails, compliance toggles, etc.).

2. **Policy Order:** Open `conf/policy_order.yaml`. This file controls the exact order that your policies appear in the final combined PDF. You can add, remove, or reorder the files here. The `source` must match the filename in `policies/`.

3. **User Map (Optional):** Open `conf/usermap.json`. If you enable version history in your config, this file maps Git usernames (e.g., "todde") to a full name (e.g., "Todd Emerson") for the history table.

### Step 4: Edit Your Policies

Modify the source `.md` files in the `policies/` directory. You can use Jinja2
syntax (e.g., `{{ company_name }}` or `{% if hipaa %}...{% endif %}`)
to insert variables or logic from your `config.yaml`.

**See the [Templating Guide](https://www.google.com/search?q=docs/templating_guide.md) for detailed examples.**

### Step 5: Push to Your Private Repository

Change the Git remote to point to the new private repository you created in Step 1.

```bash
git remote set-url origin https://github.com/YOUR-USERNAME/YOUR-PRIVATE-REPO.git git push -u origin main
```


Pushing to the `main` branch will automatically trigger the GitHub Action.

### Step 6: Download Your Documents

When the action is complete (a green checkmark on your commit), go to your
repository's "Actions" tab and click on the latest workflow run. You will find
your processed documents available to download as "Artifacts":

* **`processed-markdown-policies`**: A `.zip` of the final `.md` files.

* **`policy-pdfs`**: A `.zip` containing both the individual `.pdf` files and the final `combined_policies.pdf`.

## Configuration Overview

The core of this engine is the `conf/config.yaml` file, which acts as a master
control panel for all your policies.

* **Company Variables:** Basic text replacement for names, emails, etc.

* **PDF Metadata:** Sets the title and author for the combined PDF.

* **Feature Toggles:** Booleans (`true`/`false`) to show/hide entire sections (e.g., `show_internal_notes`).

* **Service Types:** Nested objects to control content based on your offerings (e.g., `service_types.paas.enabled`).

* **Compliance Frameworks:** Nested objects to show/hide policy sections based on framework (e.g., `compliance_frameworks.hipaa`).

* **Revision History Toggles:** Controls whether the Git history is appended to the final documents.

### Advanced Documentation

* **Templating:** For a detailed guide on using Jinja2 logic (`if`, `for`, etc.), see [docs/templating_guide.md](https://www.google.com/search?q=docs/templating_guide.md).

* **Config Validation:** This project includes a script to help you check your config for errors. See [docs/CONFIG_VALIDATION.md](https://www.google.com/search?q=docs/CONFIG_VALIDATION.md) for details.

## License

This project uses a hybrid licensing model:

* **The Software** (all `.py`, `.yml`, `.github/workflows` files) is licensed under the MIT License.

* **The Content** (the `.md` policy files) is licensed under the CC BY-SA 4.0 License, as it is a derivative of the original Catalyze policies.

See the [LICENSE.md](license.md) file for full details.