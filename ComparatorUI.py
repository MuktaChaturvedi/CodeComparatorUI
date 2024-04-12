import streamlit as st
import json

def main():
    st.markdown("""
    <style>
    /* Center the title */
    .title {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    st.title("MAWM CODE COMPARATOR")

    # Layout setup
    left_column, right_column = st.columns(2)

    # Left side - Source Organisation
    with left_column:
        st.subheader("Source Organisation")
        source_username = st.text_input("Source Username")
        source_password = st.text_input("Source Password", type="password")
        source_organization = st.text_input("Source Organisation")

    # Right side - Target Organisation
    with right_column:
        st.subheader("Target Organisation")
        target_username = st.text_input("Target Username")
        target_password = st.text_input("Target Password", type="password")
        target_organization = st.text_input("Target Organisation")

    # Add a divider between the two sides
    # st.write("---")

    # Center-align the additional fields
    # st.write("<h2 style='text-align: center;'>Additional Fields</h2>", unsafe_allow_html=True)

    # Email, Category, and Component/Extension Pack fields
    st.write("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
    email_id = st.text_input("Email ID")
    category = st.selectbox("Category", ["Component", "Extension Pack"])

    selected_items = []
    if category == "Component":
        selected_items = st.multiselect("Select Components", ["Picking", "Packing", "DC Order", "Inventory", "Items"])
    elif category == "Extension Pack":
        uploaded_file = st.file_uploader("Upload JSON file", type="json")
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                extension_names = [entry.get("OneBoardName", "Unknown") for entry in data]
                selected_items = st.multiselect("Select Extension Packs", extension_names)
            except json.JSONDecodeError:
                st.error("Invalid JSON file. Please upload a valid JSON file which contains OneBoardName.")
    st.write("</div>", unsafe_allow_html=True)

    # Compare button
    if st.button("Compare"):
        if not all([source_username, source_password, source_organization,
                    target_username, target_password, target_organization,
                    email_id, category, selected_items]):
            st.error("Please fill in all required fields before proceeding.")
        else:
            open_new_tab(source_username, source_password, source_organization,
                         target_username, target_password, target_organization,
                         email_id, category, selected_items)

def open_new_tab(source_username, source_password, source_organization,
                 target_username, target_password, target_organization,
                 email_id, category, selected_items):
    st.write("Click the button below to open a new tab with user inputs")

    # Construct message with user inputs
    message = f"<h1>MAWM CODE COMPARATOR</h1>"
    message += "<h2>User Inputs:</h2>"
    message += f"<p>Source Username: {source_username}</p>"
    message += f"<p>Source Password: {source_password}</p>"
    message += f"<p>Source Organisation: {source_organization}</p>"
    message += f"<p>Target Username: {target_username}</p>"
    message += f"<p>Target Password: {target_password}</p>"
    message += f"<p>Target Organisation: {target_organization}</p>"
    message += f"<p>Email ID: {email_id}</p>"
    message += f"<p>Category: {category}</p>"
    if selected_items:
        message += "<p>Selected Items:</p>"
        message += "<ul>"
        for item in selected_items:
            message += f"<li>{item}</li>"
        message += "</ul>"

    # Embed HTML with JavaScript to open a new tab
    html_string = f"""
    <button onclick="openNewTab('{message}')">Open New Tab</button>
    <script>
        function openNewTab(message) {{
            var newTab = window.open("");
            newTab.document.write(message);
        }}
    </script>
    """
    st.components.v1.html(html_string, height=50)

if __name__ == "__main__":
    main()
