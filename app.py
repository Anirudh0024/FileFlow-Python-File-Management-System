
from pathlib import Path
from datetime import datetime
import streamlit as st

# -------------------- Configuration --------------------

BASE_DIR = Path(__file__).resolve().parent / "managed_files"
BASE_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="File Manager",
    page_icon="📁",
    layout="wide"
)


# -------------------- Helper Functions --------------------

def get_safe_path(name):
    """Allow file operations only inside managed_files."""
    name = name.strip()

    if not name:
        raise ValueError("Please enter a file name.")

    relative_path = Path(name)

    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise ValueError("Invalid path. Use a relative file path.")

    path = (BASE_DIR / relative_path).resolve()

    if not path.is_relative_to(BASE_DIR.resolve()):
        raise ValueError("You cannot access files outside the workspace.")

    return path


def get_files():
    """Return files and folders inside the workspace."""
    return sorted(
        BASE_DIR.rglob("*"),
        key=lambda p: (p.is_file(), str(p).lower())
    )


def show_files():
    """Display the current workspace contents."""
    files = get_files()

    if not files:
        st.info("Your workspace is empty.")
        return

    rows = []

    for path in files:
        is_file = path.is_file()

        rows.append({
            "Name": str(path.relative_to(BASE_DIR)),
            "Type": "File" if is_file else "Folder",
            "Size": (
                f"{path.stat().st_size:,} bytes"
                if is_file else "—"
            ),
            "Last Modified": datetime.fromtimestamp(
                path.stat().st_mtime
            ).strftime("%d %b %Y, %I:%M %p")
        })

    st.dataframe(rows, use_container_width=True, hide_index=True)


# -------------------- Sidebar --------------------

st.sidebar.title("📁 File Manager")

page = st.sidebar.radio(
    "Choose an operation",
    [
        "Dashboard",
        "Create File",
        "Read File",
        "Update File",
        "Delete File"
    ]
)

st.sidebar.caption("Workspace: managed_files/")


# -------------------- Dashboard --------------------

if page == "Dashboard":
    st.title("📁 File Management System")
    st.write("Manage your text files from one simple interface.")

    files = get_files()
    file_count = sum(p.is_file() for p in files)
    folder_count = sum(p.is_dir() for p in files)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Files", file_count)
    col2.metric("Total Folders", folder_count)
    col3.metric(
        "Total Size",
        f"{sum(p.stat().st_size for p in files if p.is_file()):,} bytes"
    )

    st.subheader("Workspace Contents")
    show_files()


# -------------------- Create File --------------------

elif page == "Create File":
    st.title("➕ Create a File")

    name = st.text_input(
        "File name",
        placeholder="example.txt"
    )

    content = st.text_area(
        "Initial content",
        height=200,
        placeholder="Write something here..."
    )

    if st.button("Create File", type="primary"):
        try:
            path = get_safe_path(name)

            if path.exists():
                st.error("A file or folder with this name already exists.")
            else:
                path.parent.mkdir(parents=True, exist_ok=True)

                # Exclusive creation prevents accidental overwriting.
                with path.open("x", encoding="utf-8") as file:
                    file.write(content)

                st.success(f"Created: {path.relative_to(BASE_DIR)}")
                st.rerun()

        except (ValueError, OSError) as error:
            st.error(str(error))


# -------------------- Read File --------------------

elif page == "Read File":
    st.title("📖 Read a File")

    files = [
        p for p in get_files()
        if p.is_file()
    ]

    if not files:
        st.info("Create a file first.")
    else:
        selected = st.selectbox(
            "Select a file",
            files,
            format_func=lambda p: str(p.relative_to(BASE_DIR))
        )

        if st.button("Read File"):
            try:
                content = selected.read_text(encoding="utf-8")

                st.session_state["read_content"] = content
                st.session_state["read_name"] = str(
                    selected.relative_to(BASE_DIR)
                )

            except (OSError, UnicodeError) as error:
                st.error(f"Could not read the file: {error}")

        if "read_content" in st.session_state:
            st.caption(f"File: {st.session_state['read_name']}")
            st.text_area(
                "File contents",
                value=st.session_state["read_content"],
                height=300,
                disabled=True
            )


# -------------------- Update File --------------------

elif page == "Update File":
    st.title("✏️ Update a File")

    files = [
        p for p in get_files()
        if p.is_file()
    ]

    if not files:
        st.info("There are no files to update.")
    else:
        selected = st.selectbox(
            "Select a file",
            files,
            format_func=lambda p: str(p.relative_to(BASE_DIR))
        )

        action = st.radio(
            "Choose an action",
            ["Overwrite Content", "Append Content", "Rename File"],
            horizontal=True
        )

        if action == "Overwrite Content":
            new_content = st.text_area(
                "New content",
                height=200,
                placeholder="This will replace the existing content."
            )

            if st.button("Overwrite File", type="primary"):
                try:
                    selected.write_text(
                        new_content,
                        encoding="utf-8"
                    )
                    st.success("File content overwritten successfully.")
                    st.rerun()

                except OSError as error:
                    st.error(str(error))

        elif action == "Append Content":
            extra_content = st.text_area(
                "Content to append",
                height=150
            )

            if st.button("Append Content", type="primary"):
                try:
                    with selected.open("a", encoding="utf-8") as file:
                        file.write(extra_content)

                    st.success("Content appended successfully.")
                    st.rerun()

                except OSError as error:
                    st.error(str(error))

        elif action == "Rename File":
            new_name = st.text_input(
                "New file name",
                value=selected.name
            )

            if st.button("Rename File", type="primary"):
                try:
                    destination = get_safe_path(new_name)

                    if destination.exists():
                        st.error("The destination already exists.")
                    elif destination == selected:
                        st.info("The file already has this name.")
                    else:
                        selected.rename(destination)
                        st.success("File renamed successfully.")
                        st.rerun()

                except (ValueError, OSError) as error:
                    st.error(str(error))


# -------------------- Delete File --------------------

elif page == "Delete File":
    st.title("🗑️ Delete a File")

    files = [
        p for p in get_files()
        if p.is_file()
    ]

    if not files:
        st.info("There are no files to delete.")
    else:
        selected = st.selectbox(
            "Select a file",
            files,
            format_func=lambda p: str(p.relative_to(BASE_DIR))
        )

        st.warning(
            f"You are about to delete: "
            f"{selected.relative_to(BASE_DIR)}"
        )

        confirmed = st.checkbox("I confirm that I want to delete this file.")

        if st.button(
            "Delete File",
            type="primary",
            disabled=not confirmed
        ):
            try:
                # Recheck the path immediately before deletion.
                path = get_safe_path(
                    str(selected.relative_to(BASE_DIR))
                )

                if path.is_file():
                    path.unlink()
                    st.success("File deleted successfully.")
                    st.rerun()
                else:
                    st.error("The file no longer exists.")

            except (ValueError, OSError) as error:
                st.error(str(error))
