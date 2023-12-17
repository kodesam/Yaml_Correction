import sys
import ruamel.yaml
import streamlit as st
import base64

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
st.markdown("**Developed by:** Syed Aamir")

st.markdown("---")

def correct_indentation(input_file, output_file):
    try:
        # Create YAML instance
        yaml = ruamel.yaml.YAML()

        # Load the YAML content from input file
        with open(input_file, "r") as file:
            yaml_content = file.read()
            data = yaml.load(yaml_content)

        # Dump the YAML content with correct indentation
        with open(output_file, "w") as file:
            yaml.dump(data, file)

        st.success(f"YAML indentation corrected! You can download the output file below.")

    except ruamel.yaml.YAMLError as e:
        st.error(f"Error correcting YAML indentation: {e}")


# Read input and output file paths from Streamlit file uploader
uploaded_file = st.file_uploader("Upload YAML File", type=["yaml", "yml"])

if uploaded_file is not None:
    input_file = uploaded_file.name
    output_file = "output.yaml"

    # Save the uploaded file to input file path
    with open(input_file, "wb") as file:
        file.write(uploaded_file.getvalue())

    # Correct the indentation and write to output file
    correct_indentation(input_file, output_file)

    # Provide a download link for the output file
    with open(output_file, "rb") as file:
        file_content = file.read()
        encoded_content = base64.b64encode(file_content).decode("utf-8")
        download_link = f'<a href="data:application/octet-stream;base64,{encoded_content}" download="{output_file}">Download Output File</a>'
        st.markdown(download_link, unsafe_allow_html=True)
