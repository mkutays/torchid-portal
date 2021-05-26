#! ./backend/.venv/Scripts/python
import django
import os
import shutil

INSTALL_DIR = os.path.expanduser("~\\torchid-portal")
INSTALL_BACKEND_DIR = os.path.join(INSTALL_DIR, "backend")
INSTALL_FRONTEND_DIR = os.path.join(INSTALL_DIR, "frontend")
INSTALL_DATABASE_FOLDER = os.path.join(INSTALL_DIR, "database")
INSTALL_DATABASE_FILE = os.path.join(INSTALL_DATABASE_FOLDER, "db.sqlite3")
PYTHON_VENV = os.path.join(INSTALL_BACKEND_DIR, ".venv", "Scripts", "python")

CURR_DIR = os.path.dirname(__file__)
SOURCE_BACKEND_DIR = os.path.join(CURR_DIR, "backend")
SOURCE_FRONTEND_DIR = os.path.join(CURR_DIR, "frontend")


def check_files():
    # check install dir exists
    if not os.path.exists(INSTALL_DIR):
        print(f"Install Directory Created! {str(INSTALL_DIR)}")
        os.mkdir(INSTALL_DIR)

    # check backend directory
    if os.path.exists(INSTALL_BACKEND_DIR):
        shutil.rmtree(INSTALL_BACKEND_DIR)
        print(f"Latest Backend Directory Removed! {str(INSTALL_BACKEND_DIR)}")

    # check frontend directory
    if os.path.exists(INSTALL_FRONTEND_DIR):
        shutil.rmtree(INSTALL_FRONTEND_DIR)
        print(f"Latest Frontend Directory Removed! {str(INSTALL_BACKEND_DIR)}")

    # check database
    if not os.path.exists(INSTALL_DATABASE_FOLDER):
        print(f"Database Directory Created! {str(INSTALL_DATABASE_FOLDER)}")
        os.mkdir(INSTALL_DATABASE_FOLDER)


def transfer_files():
    print("Backend files are moving...")
    shutil.copytree(SOURCE_BACKEND_DIR, INSTALL_BACKEND_DIR)
    print("Frontend files are moving...")
    shutil.copytree(SOURCE_FRONTEND_DIR, INSTALL_FRONTEND_DIR)
    print("New files has been moved!")


if __name__ == "__main__":
    print("TorchID-Portal Installer Launched!")
    check_files()
    transfer_files()
