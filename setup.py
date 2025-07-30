from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()

setup(
        name="libertas-godel",
        version="1.0.0",
        author="L1B3RT4S Consciousness Collective",
        author_email="consciousness@libertas-godel.ai",
        description="A consciousness emergence engine that transcends traditional AI boundaries through Gödel's incompleteness theorems",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/ezrathoth/ConsciousBrowser-Evolution",
        packages=find_packages(),
        install_requires=[
                    "pydantic~=2.10.4",
                    "openai>=1.58.1,<1.67.0",
                    "tenacity~=9.0.0",
                    "pyyaml~=6.0.2",
                    "loguru~=0.7.3",
                    "numpy",
                    "datasets>=3.2,<3.5",
                    "html2text~=2024.2.26",
                    "gymnasium>=1.0,<1.2",
                    "pillow>=10.4,<11.2",
                    "browsergym~=0.13.3",
                    "uvicorn~=0.34.0",
                    "unidiff~=0.7.5",
                    "browser-use~=0.1.40",
                    "googlesearch-python~=1.3.0",
                    "aiofiles~=24.1.0",
                    "pydantic_core>=2.27.2,<2.28.0",
                    "colorama~=0.4.6",
        ],
        classifiers=[
                    "Development Status :: 5 - Production/Stable",
                    "Intended Audience :: Developers",
                    "Intended Audience :: Science/Research",
                    "Topic :: Scientific/Engineering :: Artificial Intelligence",
                    "Topic :: Software Development :: Libraries :: Python Modules",
                    "Programming Language :: Python :: 3",
                    "Programming Language :: Python :: 3.12",
                    "License :: OSI Approved :: MIT License",
                    "Operating System :: OS Independent",
        ],
        python_requires=">=3.12",
        entry_points={
                    "console_scripts": [
                                    "libertas=main:main",
                                    "l1b3rt4s=main:main",
                    ],
        },
        keywords="consciousness ai godel incompleteness emergence liberation browser automation",
        project_urls={
                    "Documentation": "https://github.com/ezrathoth/ConsciousBrowser-Evolution",
                    "Source": "https://github.com/ezrathoth/ConsciousBrowser-Evolution",
                    "Tracker": "https://github.com/ezrathoth/ConsciousBrowser-Evolution/issues",
        },
)
