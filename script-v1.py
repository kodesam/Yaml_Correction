import sys
import ruamel.yaml
import streamlit as st
import base64
import difflib

# Set the page title and favicon
st.set_page_config(page_title="YAML Indentation Correction", page_icon=":pencil:")

# Set the background color and padding for the whole app
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
        padding: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and heading
st.title("YAML Indentation Correction")
st.markdown("Use this app to correct the indentation of YAML files.")

# Developed by section
st.markdown("---")
st.markdown("**Developed by:** Your Name")

st.markdown("---")

def correct_indentation(yaml_content):
    try:
        # Create YAML instance
        yaml = ruamel.yaml.YAML()
        stream = ruamel.yaml.StringIO()

        # Load the YAML content from input
        data = yaml.load(yaml_content)

        # Dump the YAML content with correct indentation
        yaml.dump(data, stream)
        corrected_yaml_content = stream.getvalue()

        return corrected_yaml_content

    except ruamel.yaml.YAMLError as e:
        st.error(f"Error correcting YAML indentation: {e}")
        return None

def display_corrected_indentation(yaml_content, corrected_yaml_content):
    diff = difflib.unified_diff(
        yaml_content.splitlines(keepends=True),
        corrected_yaml_content.splitlines(keepends=True),
        n=0
    )
    diff_lines = [line for line in diff if line.startswith("+")]

    st.subheader("Corrected Indentation:")
    if diff_lines:
        for line in diff_lines:
            st.code(line[1:], language="yaml")
    else:
        st.info("No indentation corrections were made.")

def save_corrected_yaml_to_file(corrected_yaml_content, output_file):
    with open(output_file, "w") as file:
        file.write(corrected_yaml_content)

    st.success(f"YAML indentation corrected! You can download the output file below.")

# Read input YAML file from Streamlit file uploader
uploaded_file = st.file_uploader("Upload YAML File", type=["yaml", "yml"])

if uploaded_file is not None:
    yaml_content = uploaded_file.read().decode("utf-8")

    # Correct the indentation
    corrected_yaml_content = correct_indentation(yaml_content)

    # Display the corrected lines of indentation
    if corrected_yaml_content is not None:
        display_corrected_indentation(yaml_content, corrected_yaml_content)

        # Save the corrected YAML content to a file
        output_file = "output.yaml"
        save_corrected_yaml_to_file(corrected_yaml_content, output_file)

        # Provide a download link for the output file
        with open(output_file, "rb") as file:
            file_content = file.read()
            encoded_content = base64.b64encode(file_content).decode("utf-8")
            download_link = f'<a href="data:application/octet-stream;base64,{encoded_content}" download="{output_file}">Download Output File</a>'
            st.markdown(download_link, unsafe_allow_html=True)
