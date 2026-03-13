"""Pytest configuration - Basic version without numpy"""

import sys
import os

# ملاحظة: هذا الملف لا يتطلب numpy
# للاختبارات المتقدمة، يرجى تثبيت numpy في بيئة مناسبة

def pytest_configure(config):
    """تكوين pytest"""
    print("⚡ INFRAS-CLOUD Test Configuration")
    print("📝 Running in basic mode (without numpy)")
    print("ℹ️  For full tests, install numpy in a compatible environment")
