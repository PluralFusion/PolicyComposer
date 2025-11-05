import streamlit as st
import yaml
import uuid
from collections import OrderedDict

# Helper to load yaml and keep the order of keys
def ordered_load(stream, Loader=yaml.SafeLoader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)

# Helper to dump yaml and keep the order of keys
def ordered_dump(data, stream=None, Dumper=yaml.SafeDumper, **kwds):
    class OrderedDumper(Dumper):
        pass
    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


CONFIG_PATH = 'conf/config.yaml'
SCHEMA_PATH = 'conf/ui_schema.yaml'

# --- App Layout ---
st.set_page_config(layout="wide")
st.title("PolicyComposer Configuration Manager")
st.write("A web interface to easily edit your `config.yaml` file. Make your changes and click 'Save Configuration' at the bottom. For more details, see the Configuration UI Manual.")

def set_delete_flag(key, item_id):
    st.session_state["delete_item_id"] = (key, item_id)

# Process deletions before rendering
if st.session_state.get("delete_item_id") is not None:
    key, item_id = st.session_state.delete_item_id
    # Handle composite keys for nested lists (e.g., "approved_tools.collaboration")
    if '.' in key:
        parent_key, child_key = key.split('.', 1)
        if parent_key in st.session_state.config and child_key in st.session_state.config[parent_key]:
            target_list = st.session_state.config[parent_key][child_key]
            st.session_state.config[parent_key][child_key] = [obj for obj in target_list if obj.get("_id") != item_id]
    else: # Handle simple top-level lists
        target_list = st.session_state.config.get(key, [])
        st.session_state.config[key] = [obj for obj in target_list if obj.get("_id") != item_id]
    del st.session_state["delete_item_id"]

# --- Load Config and Schema ---
# Use session state to preserve config across reruns from widget interactions
if 'config' not in st.session_state:
    try:
        with open(CONFIG_PATH, 'r') as f:
            st.session_state.config = ordered_load(f)
    except FileNotFoundError:
        st.error(f"Configuration file not found at `{CONFIG_PATH}`. Please ensure it exists.")
        st.stop()
try:
    with open(SCHEMA_PATH, 'r') as f:
        schema = ordered_load(f)
except FileNotFoundError:
    st.error(f"UI Schema file not found at `{SCHEMA_PATH}`. The UI cannot be rendered.")
    st.stop()

def find_lists_for_id_backfill(schema_node):
    """Recursively find all keys in the schema that use list-of-object widgets."""
    keys = []
    for key, definition in schema_node.items():
        if key.startswith('_'):
            continue
        if isinstance(definition, dict):
            widget_type = definition.get('_widget')
            if widget_type == 'list_of_objects':
                keys.append({'type': 'list_of_objects', 'key': key})
            elif widget_type == 'dict_of_list_of_objects':
                keys.append({'type': 'dict_of_list_of_objects', 'key': key})
            else:
                keys.extend(find_lists_for_id_backfill(definition))
    return keys

# --- Data Backfilling ---
# Ensure all list items have a unique ID for stable deletion.
list_definitions = find_lists_for_id_backfill(schema)
for definition in list_definitions:
    key = definition['key']
    if key in st.session_state.config:
        if definition['type'] == 'list_of_objects' and isinstance(st.session_state.config[key], list):
            for item in st.session_state.config[key]:
                if '_id' not in item:
                    item['_id'] = str(uuid.uuid4())
        elif definition['type'] == 'dict_of_list_of_objects' and isinstance(st.session_state.config[key], dict):
            for category_list in st.session_state.config[key].values():
                if isinstance(category_list, list):
                    for item in category_list:
                        if '_id' not in item:
                            item['_id'] = str(uuid.uuid4())

def render_widget(key, definition, data_node):
    """Renders a single widget based on the schema definition."""
    widget_type = definition.get("_widget") or definition.get("widget")
    label = definition.get("label", key.replace('_', ' ').title())
    help_text = definition.get("help")
    
    if widget_type == "text_input":
        data_node[key] = st.text_input(label, value=data_node.get(key, ''), help=help_text)
    
    elif widget_type == "toggle":
        data_node[key] = st.toggle(label, value=data_node.get(key, False), help=help_text)
        
    elif widget_type == "selectbox":
        options = definition.get("options", [])
        try:
            index = options.index(data_node.get(key))
        except (ValueError, TypeError):
            index = 0
        data_node[key] = st.selectbox(label, options=options, index=index, help=help_text)
        
    elif widget_type == "text_area":
        # Handle list-to-string conversion for text_area
        list_data = data_node.get(key, [])
        str_data = "\n".join(list_data) if isinstance(list_data, list) else ""
        new_str_data = st.text_area(label, str_data, height=definition.get("height", 100), help=help_text)
        data_node[key] = [item.strip() for item in new_str_data.split("\n") if item.strip()]
        
    elif widget_type == "toggle_group":
        # Special widget for a dictionary of booleans
        # **FIX:** The data is nested one level deeper, under the 'key' itself.
        if key not in data_node:
            data_node[key] = {}
        target_dict = data_node[key]

        num_columns = definition.get("_columns", 3)
        cols = st.columns(num_columns)
        i = 0
        for item_key, item_value in target_dict.items():
            if isinstance(target_dict.get(item_key), bool):
                with cols[i % num_columns]:
                    target_dict[item_key] = st.toggle(item_key.upper(), value=target_dict.get(item_key, False))
                i += 1
                
    elif widget_type == "dict_of_toggles":
        # Special widget for nested dictionaries of booleans (like service_types)
        # **FIX:** The data is nested one level deeper, under the 'key' itself.
        if key not in data_node:
            data_node[key] = {}
        target_dict = data_node[key]

        for service_name, details in target_dict.items():
            if isinstance(details, dict) and 'enabled' in details:
                with st.container(border=True):
                    st.subheader(f"Service: {service_name.replace('_', ' ').title()}")
                    details['enabled'] = st.toggle(f"Enable {service_name.title()}", value=details.get('enabled', False), key=f"toggle_{service_name}")
                    
                    if details['enabled']:
                        sub_cols = st.columns(3)
                        i = 0
                        for sub_key, sub_value in details.items():
                            if isinstance(sub_value, bool) and sub_key != 'enabled':
                                with sub_cols[i % 3]:
                                    details[sub_key] = st.toggle(sub_key.replace('_', ' ').title(), value=sub_value, key=f"toggle_{service_name}_{sub_key}")
                                i += 1

    elif widget_type == "dict_of_frameworks":
        # Custom widget for the nested compliance_frameworks structure
        if key not in data_node:
            data_node[key] = {}
        target_dict = data_node[key]

        for framework_name, details in target_dict.items():
            if isinstance(details, dict) and 'supported' in details:
                with st.container(border=True):
                    st.subheader(f"Framework: {framework_name.upper()}")
                    details['supported'] = st.toggle(f"Support {framework_name.upper()}", value=details.get('supported', False), key=f"toggle_framework_{framework_name}")

                    if details['supported']:
                        audit_details = details.get('audit', {})
                        if isinstance(audit_details, dict):
                            st.markdown("---")
                            st.write("**Audit Status**")
                            cols = st.columns(2)
                            with cols[0]:
                                audit_details['in_progress'] = st.toggle("Audit In Progress", value=audit_details.get('in_progress', False), key=f"audit_ip_{framework_name}")
                                audit_details['completed'] = st.toggle("Audit Completed", value=audit_details.get('completed', False), key=f"audit_comp_{framework_name}")
                            with cols[1]:
                                audit_details['provider'] = st.text_input("Audit Provider", value=audit_details.get('provider', ''), key=f"audit_prov_{framework_name}")
                                audit_details['completed_date'] = st.text_input("Completion Date", value=audit_details.get('completed_date', ''), key=f"audit_date_{framework_name}", help="Use YYYY-MM-DD format.")
                            # Write the updated audit details back to the main details dict
                            details['audit'] = audit_details

    elif widget_type == "dict_group":
        # Special widget for a group of fields under a single config key (like hipaa_audit)
        # **FIX:** The data is nested one level deeper, under the 'key' itself.
        if key not in data_node:
            data_node[key] = {}
        target_dict = data_node[key]

        st.subheader(definition.get("_label", key.title()))
        
        # Iterate through the fields defined in the schema for this group
        for field_key, field_def in definition.items():
            if field_key.startswith('_'):
                continue
            
            field_widget = field_def.get("widget")
            field_label = field_def.get("label")
            if field_widget == "text_input":
                target_dict[field_key] = st.text_input(field_label, value=target_dict.get(field_key, ''), key=f"{key}_{field_key}")
            elif field_widget == "toggle":
                target_dict[field_key] = st.toggle(field_label, value=target_dict.get(field_key, False), key=f"{key}_{field_key}")

    elif widget_type == "list_of_objects":
        # Special widget for a list of dictionaries (like vendors)
        # **FIX:** The data is nested one level deeper, under the 'key' itself.
        if key not in data_node:
            data_node[key] = []
        target_list = data_node[key]

        object_schema = definition.get("_object_schema", {})

        # Display existing items with edit/delete options
        for i, item in enumerate(target_list):
            with st.container(border=True):
                item_id = item.get("_id") # Get the stable UUID for this item
                cols = st.columns(len(object_schema) + 1)
                field_index = 0
                for field_key, field_def in object_schema.items():
                    with cols[field_index]:
                        # Simplified rendering for sub-widgets
                        field_widget = field_def.get("widget")
                        field_label = field_def.get("label")
                        if field_widget == "text_input":
                            item[field_key] = st.text_input(label, value=item.get(field_key, ''), key=f"{key}_{item_id}_{field_key}")
                        elif field_widget == "toggle":
                            item[field_key] = st.toggle(label, value=item.get(field_key, False), key=f"{key}_{item_id}_{field_key}")
                        elif field_widget == "text_area":
                            list_data = item.get(field_key, [])
                            str_data = "\n".join(list_data) if isinstance(list_data, list) else ""
                            new_str_data = st.text_area(label, str_data, height=definition.get("height", 100), key=f"{key}_{item_id}_{field_key}")
                            item[field_key] = [s.strip() for s in new_str_data.split("\n") if s.strip()]
                        elif field_widget == "multiselect":
                            options = field_def.get("options", [])
                            item[field_key] = st.multiselect(field_label, options=options, default=item.get(field_key, []), key=f"{key}_{item_id}_{field_key}")
                    field_index += 1
                
                with cols[-1]: # Delete button in the last column
                    st.write("") # Spacer
                    st.write("") # Spacer

                    st.button(
                        "Delete",
                        key=f"delete_{key}_{item_id}",
                        type="secondary",
                        use_container_width=True,
                        on_click=set_delete_flag,
                        args=(key, item_id)
                    )

        # Add a button to create a new item in the list
        singular_key = key[:-1] if key.endswith('s') else key
        if st.button(f"＋ Add New {singular_key.replace('_', ' ').title()}", key=f"add_new_{key}"):
            new_item = {"_id": str(uuid.uuid4())}
            for k, v in object_schema.items():
                new_item[k] = [] if v.get('widget') in ['text_area', 'multiselect'] else ""
            target_list.append(new_item)
            st.rerun()
        
    elif widget_type == "dict_of_list_of_objects":
        # Special widget for a dict of lists of objects (like approved_tools)
        if key not in data_node:
            data_node[key] = {}
        target_dict = data_node[key]
        object_schema = definition.get("_object_schema", {})

        for category, item_list in target_dict.items():
            st.subheader(f"{category.replace('_', ' ').title()} Tools")
            if not isinstance(item_list, list):
                continue

            for i, item in enumerate(item_list):
                with st.container(border=True):
                    # Use a unique key for each item based on its ID
                    item_id = item.get("_id")
                    cols = st.columns(len(object_schema) + 1)
                    field_index = 0
                    for field_key, field_def in object_schema.items():
                        with cols[field_index]:
                            field_widget = field_def.get("widget")
                            field_label = field_def.get("label")
                            if field_widget == "text_input":
                                item[field_key] = st.text_input(field_label, value=item.get(field_key, ''), key=f"{category}_{item_id}_{field_key}")
                            elif field_widget == "text_area":
                                list_data = item.get(field_key, [])
                                str_data = "\n".join(list_data) if isinstance(list_data, list) else ""
                                new_str_data = st.text_area(field_label, str_data, height=field_def.get("height", 100), key=f"{category}_{item_id}_{field_key}")
                                item[field_key] = [s.strip() for s in new_str_data.split("\n") if s.strip()]
                        field_index += 1
                    
                    with cols[-1]:
                        st.write("")
                        st.write("")
                        st.button(
                            "Delete",
                            key=f"delete_{category}_{item_id}",
                            type="secondary",
                            use_container_width=True,
                            on_click=set_delete_flag,
                            args=(f"{key}.{category}", item_id) # Pass a composite key
                        )
            
            # Add a button to create a new item in this category's list
            singular_category = category[:-1] if category.endswith('s') else category
            if st.button(f"＋ Add New {singular_category.replace('_', ' ').title()}", key=f"add_new_{key}_{category}"):
                new_item = {"_id": str(uuid.uuid4())}
                for k, v in object_schema.items():
                    new_item[k] = [] if v.get('widget') in ['text_area', 'multiselect'] else ""
                item_list.append(new_item)
                st.rerun()
    else:
        # This can be expanded to handle more complex types like list_of_objects
        pass

# --- Main UI Rendering Loop ---
for section_key, section_def in schema.items():
    widget = section_def.get("_widget", "container")
    label = section_def.get("_label", section_key.replace('_', ' ').title())
    help_text = section_def.get("_help")
    
    # Determine the container type (e.g., expander or simple container)
    if widget == "expander":
        container = st.expander(label)
    else: # Default to container
        container = st.container(border=True)
        container.subheader(label)
        
    with container:
        if help_text:
            st.markdown(help_text)
        
        # Check for special headers or dividers before rendering widgets
        if section_def.get("_header"):
            st.write(section_def.get("_header"))
        if section_def.get("_divider"):
            st.markdown("---")
            
        # --- Simplified and Corrected Rendering Logic ---
        column_keys = [k for k, v in section_def.items() if not k.startswith('_')]
        num_columns = section_def.get("_columns")

        if num_columns:
            cols = st.columns(num_columns)
            for i, key in enumerate(column_keys):
                with cols[i % num_columns]:
                    # The widget definition is section_def[key]
                    # The data_node is the top-level config object
                    render_widget(key, section_def[key], st.session_state.config)
        else:
            for key in column_keys:
                render_widget(key, section_def[key], st.session_state.config)

# --- Save Button ---
st.divider()
if st.button("💾 Save Configuration", type="primary"):
    with open(CONFIG_PATH, 'w') as f:
        ordered_dump(st.session_state.config, f, default_flow_style=False)
    st.success(f"✅ Configuration successfully saved to `{CONFIG_PATH}`!")
    st.balloons()