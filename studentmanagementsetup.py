from cx_Freeze import *
excludes = []
packages = []
includefiles = ['st_icon.ico']
base = None
if sys.platform == 'win32':
    base = "Win32GUI"

shortcut_table = [
    ('DesktopShortcut',
     'DesktopFolder',
     'StudentManagementSystem',
     "TARGETDIR",
     "[TARGETDIR]\StudentManageSystem.exe",
     None,
     None,
     None,
     None,
     None,
     None,
     "TARGETDIR",)
]

msi_data = {"Shortcut": shortcut_table}

bdist_msi_options = {"data" : msi_data}
setup(
    version="0.1",
    description="Student Management System",
    author="Ashwini",
    name="Student Management System",
    options={'build_exe':{'include_files': includefiles}, "bdist_msi":bdist_msi_options, },
    executables=[
        Executable(
             script="StudentManageSystem.py",
             base=base,
             icon='st_icon.ico',
        )
    ]
)