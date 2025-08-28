from setuptools import setup, find_packages
import io


def read_requirements_sections(path="requirements.txt"):
    core = []
    test = []
    current = "core"
    with io.open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line:
                continue
            if line.startswith("#"):
                h = line.lower()
                current = "test" if "test" in h else "core" if "core" in h else current
                continue
            if line.startswith("-"):
                continue
            (core if current == "core" else test).append(line)
    # dedupe while preserving order
    core = list(dict.fromkeys(core))
    test = list(dict.fromkeys(test))
    return core, test


install_requires, test_requires = read_requirements_sections()


setup(
    name="mediaichemy",
    version="0.1.0b1",
    description="A Python library for AI powered multimedia content creation 🧪",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Pedro Blaya Luz",
    author_email="blaya.luz@gmail.com",
    url="https://github.com/pedroblayaluz/mediaichemy",
    license="MIT",
    packages=find_packages(exclude=["tests*", "htmlcov*"]),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        "tests": test_requires,
    },
    python_requires=">=3.8,<3.13",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "mediaichemy-cli=mediaichemy.cli:main",
        ],
    },
)
