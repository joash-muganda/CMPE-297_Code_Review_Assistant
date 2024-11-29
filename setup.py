from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="code-review-assistant",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An automated code review system powered by Gemma-2b",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/code-review-assistant",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "code-review-assistant=src.run_server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "code_review_assistant": [
            "src/static/*",
            "prometheus.yml",
            ".env.example",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.1.0",
            "mypy>=1.6.0",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/code-review-assistant/issues",
        "Source": "https://github.com/yourusername/code-review-assistant",
    },
)
