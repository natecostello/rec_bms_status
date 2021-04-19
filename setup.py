import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="recq-NSC",  # Replace with your own username
    version="0.0.1",
    author="Nate Costello",
    author_email="natecostello@gmail.com",
    description="A package that collects information from the REC Q Battery Management System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/natecostello/rec_bms_status",
    project_urls={
        "Bug Tracker": "https://github.com/natecostello/rec_bms_status/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #package_dir={"": "recq"},
    #packages=setuptools.find_packages(where="recq"),
    packages=['recq']
    python_requires=">=3.6",
)
