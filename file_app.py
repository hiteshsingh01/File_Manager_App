import os
import shutil
import streamlit as st
from pathlib import Path

st.set_page_config(layout="wide")
st.title("🗂️ Advanced Windows File Manager")

# --- Sidebar Directory Selector ---
root_dir = st.sidebar.text_input("Root directory", value=str(Path.home()))

def get_subdirs(path):
    try:
        return sorted([d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))])
    except:
        return []

sub_dir = st.sidebar.selectbox("Subdirectory", [""] + get_subdirs(root_dir))
current_path = os.path.join(root_dir, sub_dir) if sub_dir else root_dir

st.sidebar.write(f"📁 Accessing: `{current_path}`")

# --- List Files and Directories ---
if os.path.exists(current_path):
    st.subheader(f"📂 Contents of: `{current_path}`")
    items = os.listdir(current_path)
    if not items:
        st.info("Directory is empty.")
    else:
        for i in items:
            full_path = os.path.join(current_path, i)
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                st.write("📄" if os.path.isfile(full_path) else "📁", i)
            with col2:
                if st.button("📝 Rename", key=f"rename_{i}"):
                    st.session_state['rename_target'] = i
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{i}"):
                    try:
                        if os.path.isfile(full_path):
                            os.remove(full_path)
                        else:
                            shutil.rmtree(full_path)
                        st.success(f"Deleted: {i}")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # Rename Modal
    if 'rename_target' in st.session_state:
        old_name = st.session_state['rename_target']
        new_name = st.text_input("Enter new name", value=old_name)
        if st.button("Confirm Rename"):
            try:
                os.rename(os.path.join(current_path, old_name), os.path.join(current_path, new_name))
                st.success("Renamed successfully.")
                del st.session_state['rename_target']
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error: {e}")

else:
    st.error("❌ Directory does not exist.")

# --- File Upload ---
st.subheader("📤 Upload File")
uploaded_file = st.file_uploader("Choose a file to upload", type=None)
if uploaded_file:
    save_path = os.path.join(current_path, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Uploaded {uploaded_file.name}")

# --- Create New Folder ---
st.subheader("📁 Create New Directory")
new_folder = st.text_input("New folder name")
if st.button("Create Folder"):
    try:
        os.makedirs(os.path.join(current_path, new_folder), exist_ok=True)
        st.success("Folder created successfully.")
    except Exception as e:
        st.error(f"Error: {e}")

# --- Create/Edit Text File ---
st.subheader("✏️ Create or Edit a Text File")
file_name = st.text_input("Enter file name", placeholder="example.txt")
file_content = st.text_area("Enter file content")

if st.button("Save File"):
    try:
        with open(os.path.join(current_path, file_name), "w", encoding="utf-8") as f:
            f.write(file_content)
        st.success("File saved successfully.")
    except Exception as e:
        st.error(f"Error: {e}")

# --- Move File/Folder ---
st.subheader("📦 Move File/Folder")
source = st.text_input("Source path", placeholder="C:\\path\\to\\source")
destination = st.text_input("Destination path", placeholder="C:\\path\\to\\destination")

if st.button("Move"):
    try:
        shutil.move(source, destination)
        st.success("Moved successfully.")
    except Exception as e:
        st.error(f"Error: {e}")
