#!/usr/bin/env python3

"""INFRAS-CLOUD Upload - نسخة مبسطة"""

import os
import glob
import subprocess
import sys

TOKEN = "pypi-AgEIcHlwaS5vcmcCJGY1Y2MyOGMxLTAzNGItNDFjMS1iY2IwLTY1NjM3N2FkNmYwZQACKlszLCJlZjQ3ZDllOS04YmU5LTQ2OWMtYWQ0OC0wODRhZTg4YzZjMTUiXQAABiATiD3LNi3i26vUYfnPyz2242VHzxahrRyENRJdAlwrZg"

print("=" * 60)
print("⚡ INFRAS-CLOUD Upload v1.0.0")
print("=" * 60)

# 1. إنشاء ملف setup.py مبسط إذا لم يكن موجوداً
if not os.path.exists('setup.py'):
    print("📝 إنشاء setup.py...")
    with open('setup.py', 'w') as f:
        f.write('''from setuptools import setup, find_packages

setup(
    name="infrascloud",
    version="1.0.0",
    author="Samir Baladi",
    author_email="gitdeeper@gmail.com",
    description="INFRAS-CLOUD: Atmospheric Infrasound & Severe Weather Acoustic Signatures",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gitdeeper9/infrascloud",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "pandas>=2.0.0",
        "obspy>=1.4.0",
        "matplotlib>=3.7.0",
        "plotly>=5.14.0",
        "pyyaml>=6.0",
    ],
)
''')
    print("✅ تم إنشاء setup.py")

# 2. بناء الحزمة باستخدام setup.py مباشرة
print("\n📦 بناء الحزمة...")
subprocess.run([sys.executable, "setup.py", "sdist", "bdist_wheel", "--quiet"])

# 3. رفع الملفات
print("\n📤 رفع إلى PyPI...")
wheel_files = glob.glob("dist/*.whl") + glob.glob("dist/*.tar.gz")

if not wheel_files:
    print("❌ لا توجد ملفات للرفع!")
    sys.exit(1)

for file in wheel_files:
    print(f"   • {os.path.basename(file)}")

# رفع باستخدام twine
result = subprocess.run([
    sys.executable, "-m", "twine", "upload",
    "--username", "__token__",
    "--password", TOKEN,
    "--skip-existing"
] + wheel_files)

if result.returncode == 0:
    print("\n✅✅✅ تم الرفع بنجاح!")
    print("\n🔗 https://pypi.org/project/infrascloud/")
    print("📦 pip install infrascloud")
else:
    print("\n❌ فشل الرفع!")

print("\n" + "=" * 60)
