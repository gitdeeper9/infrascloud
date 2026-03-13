#!/usr/bin/env python3
# INFRAS-CLOUD Setup Script

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="infrascloud",
    version="1.0.0",
    author="Samir Baladi",
    author_email="gitdeeper@gmail.com",
    description="INFRAS-CLOUD: Atmospheric Infrasound & Severe Weather Acoustic Signatures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitdeeper9/infrascloud",
    packages=find_packages(include=["infras_core", "infras_core.*"]),
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "pandas>=2.0.0",
        "obspy>=1.4.0",
        "matplotlib>=3.7.0",
        "plotly>=5.14.0",
        "pyyaml>=6.0",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)
