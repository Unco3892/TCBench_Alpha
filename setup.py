# --------------------------------------------------------------------------------
# Setup script for TCBenchmark

import os
import platform
import shutil
import sys
from pathlib import Path
from setuptools import Command, setup

# Get the README content
this_directory = Path(__file__).parent
try:
    long_description = (this_directory / "README.md").read_text(encoding="utf-8")
except FileNotFoundError:
    long_description = DESCRIPTION

DISTNAME = "TCBenchmark"
DESCRIPTION = (
    "Python platform and benchmark dataset for data-driven tropical cyclone studies."
)
MAINTAINER = "Anonymous"
MAINTAINER_EMAIL = "anonymous@domain.com"
URL = "https://anonymous.url/"
LICENSE = "MIT"
PROJECT_URLS = {
    "Bug Tracker": "https://anonymous.url/issues",
    "Documentation": "https://anonymous.url/wiki",
    "Source Code": "https://anonymous.url",
}

VERSION = "0.0.3rc12"

# Custom clean command to remove build artifacts
class CleanCommand(Command):
    description = "Remove build artifacts from the source tree"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # Remove c files if we are not within a sdist package
        cwd = os.path.abspath(os.path.dirname(__file__))
        remove_c_files = not os.path.exists(os.path.join(cwd, "PKG-INFO"))
        if remove_c_files:
            print("Will remove generated .c files")
        if os.path.exists("build"):
            shutil.rmtree("build")
        for dirpath, dirnames, filenames in os.walk("tcbenchmark"):
            for filename in filenames:
                root, extension = os.path.splitext(filename)

                if extension in [".so", ".pyd", ".dll", ".pyc"]:
                    os.unlink(os.path.join(dirpath, filename))

                if remove_c_files and extension in [".c", ".cpp"]:
                    pyx_file = str.replace(filename, extension, ".pyx")
                    if os.path.exists(os.path.join(dirpath, pyx_file)):
                        os.unlink(os.path.join(dirpath, filename))

            for dirname in dirnames:
                if dirname == "__pycache__":
                    shutil.rmtree(os.path.join(dirpath, dirname))

cmdclass = {
    "clean": CleanCommand,
}

def setup_package():
    python_requires = ">=3.9"
    required_python_version = (3, 9)

    metadata = dict(
        name=DISTNAME,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        license=LICENSE,
        url=URL,
        project_urls=PROJECT_URLS,
        version=VERSION,
        long_description=long_description,
        long_description_content_type="text/markdown",
        classifiers=[
            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Topic :: Scientific/Engineering :: Atmospheric Science",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Development Status :: 3 - Alpha",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: Unix",
            "Operating System :: MacOS",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
        ],
        cmdclass=cmdclass,
        python_requires=python_requires,
        packages=['tcbenchmark'],
        package_data={
            "": ["*.csv", "*.gz", "*.txt", "*.pxd", "*.rst", "*.jpg", "*.css"]
        },
        zip_safe=False,  # the package can run out of an .egg file
    )

    commands = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    if not all(
        command in ("egg_info", "dist_info", "clean", "check") for command in commands
    ):
        if sys.version_info < required_python_version:
            required_version = "%d.%d" % required_python_version
            raise RuntimeError(
                "TCBenchmark requires Python %s or later. The current"
                " Python version is %s installed in %s."
                % (required_version, platform.python_version(), sys.executable)
            )

    setup(**metadata)

if __name__ == "__main__":
    setup_package()