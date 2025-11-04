# PolicyComposer Configuration UI Manual

The PolicyComposer Configuration UI is a web-based tool designed to make editing the `conf/config.yaml` file easier and more intuitive. Instead of editing YAML text directly, you can use a graphical interface with toggles, text boxes, and buttons.

This is particularly useful for users who are not comfortable with YAML syntax or for making quick, structured changes without the risk of formatting errors.

## How to Run the Configuration UI

The UI is built with Streamlit, a Python library for creating web apps. To run it, you need to have Python and the project's dependencies installed.

1.  **Create a Python Virtual Environment:** This creates an isolated environment for the project's dependencies. You only need to do this once.
    ```bash
    python3 -m venv .venv
    ```

2.  **Activate the Environment:** You'll need to do this every time you open a new terminal to work on the project.
    ```bash
    # On macOS and Linux
    source .venv/bin/activate
    
    # On Windows
    .venv\Scripts\activate
    ```

3.  **Install Dependencies:** This command reads the `requirements.txt` file and installs Streamlit and other necessary packages.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the UI script:** From the root directory of the project, run the following command:
    ```bash
    streamlit run config_ui.py
    ```

Your default web browser will automatically open a new tab with the Configuration UI. When you are finished making changes, you can stop the web server by pressing `Ctrl+C` in your terminal.

## Using the Interface

The interface directly reflects the structure of your `conf/config.yaml` and the `conf/ui_schema.yaml` files. The UI is organized into sections that can be expanded or collapsed.

### Key Features

*   **Interactive Widgets:**
    *   **Text Input:** For simple string values like `company_name`.
    *   **Toggle:** For boolean `true`/`false` values like `show_internal_notes`.
    *   **Select Box:** For fields with a predefined list of options, like `global_release_history_style`.
    *   **Text Area:** For multi-line string inputs or lists of strings, like the `review_committee`.

*   **Dynamic Lists (List of Objects):**
    *   Sections like **Vendors** or **Approved Tools** are managed as dynamic lists.
    *   **Editing:** You can edit the details of each existing item directly in its own container.
    *   **Deleting:** Each item has a `Delete` button to remove it from the list.
    *   **Adding:** At the bottom of each list section, there is an `＋ Add New...` button to append a new, empty item to the list for you to fill out.

*   **Nested Configuration:**
    *   Complex nested structures like `service_types` or `remote_work` are displayed in organized containers with their own sub-fields, making them easy to manage.

### Saving Your Changes

After you have made your desired changes in the web interface, scroll to the very bottom of the page and click the **"💾 Save Configuration"** button.

This action will:
1.  Overwrite the `conf/config.yaml` file with the current state of the UI.
2.  Preserve the order and formatting of the original file as much as possible.
3.  Display a success message and a celebratory animation.

Once saved, you can commit the updated `conf/config.yaml` file to your Git repository to trigger the GitHub Action that builds your policy documents.

## How It Works

The UI is not hard-coded. It is dynamically generated based on two files:

1.  **`conf/config.yaml`:** This is the data source. The UI reads this file on startup to get the current configuration values.
2.  **`conf/ui_schema.yaml`:** This file is the "blueprint" for the UI. It tells the script which widget to use for each configuration key (e.g., use a `toggle` for `show_internal_notes`), what label to display, and how to group fields into sections and columns.

If you add a new key to your `config.yaml` and want it to appear in the UI, you must also add a corresponding entry to `ui_schema.yaml`. The `validate_config.py` script can help you find keys that are in your config but missing from the schema.