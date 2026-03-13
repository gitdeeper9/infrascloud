"""اختبارات أساسية بدون numpy"""

import sys
import os
import unittest

# إضافة المسار الرئيسي
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestBasic(unittest.TestCase):
    """اختبارات أساسية للتحقق من هيكل المشروع"""
    
    def test_import_infras_core(self):
        """اختبار استيراد الحزمة الرئيسية"""
        try:
            import infras_core
            self.assertTrue(True)
            print(f"✅ infras_core version: {infras_core.__version__}")
        except ImportError as e:
            self.fail(f"❌ فشل استيراد infras_core: {e}")
    
    def test_check_files_exist(self):
        """التحقق من وجود الملفات الأساسية"""
        required_files = [
            'README.md',
            'LICENSE',
            'CHANGELOG.md',
            'CONTRIBUTING.md',
            'AUTHORS.md',
            'CITATION.cff',
            'pyproject.toml',
            'setup.py',
            'requirements.txt'
        ]
        
        for file in required_files:
            self.assertTrue(os.path.exists(file), f"❌ الملف {file} غير موجود")
        print("✅ جميع الملفات الأساسية موجودة")
    
    def test_check_infras_core_modules(self):
        """التحقق من وجود وحدات infras_core"""
        required_modules = [
            'processor.py',
            'beamformer.py',
            'ducting.py',
            'classifier.py',
            'microbarom.py',
            'absorption.py',
            'coherence.py',
            'aisi.py',
            'utils/__init__.py',
            'utils/filters.py',
            'utils/geo.py',
            'utils/io.py',
            'utils/plotting.py'
        ]
        
        for module in required_modules:
            path = os.path.join('infras_core', module)
            self.assertTrue(os.path.exists(path), f"❌ الوحدة {path} غير موجودة")
        print("✅ جميع وحدات infras_core موجودة")
    
    def test_check_directories(self):
        """التحقق من وجود المجلدات الأساسية"""
        required_dirs = [
            'data/catalogs',
            'data/ims_stations',
            'models',
            'notebooks',
            'scripts',
            'docs',
            'tests/unit',
            'tests/integration',
            'deploy/docker'
        ]
        
        for dir_path in required_dirs:
            self.assertTrue(os.path.isdir(dir_path), f"❌ المجلد {dir_path} غير موجود")
        print("✅ جميع المجلدات الأساسية موجودة")


if __name__ == '__main__':
    unittest.main()
