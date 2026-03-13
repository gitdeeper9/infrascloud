"""اختبارات السكريبتات الأساسية"""

import sys
import os
import unittest

class TestScriptsBasic(unittest.TestCase):
    """اختبار وجود ملفات السكريبتات"""
    
    def test_scripts_exist(self):
        """التحقق من وجود جميع ملفات السكريبتات"""
        scripts = [
            'scripts/run_realtime.py',
            'scripts/batch_validate.py',
            'scripts/download_ims_data.py',
            'scripts/export_aisi_report.py'
        ]
        
        for script in scripts:
            self.assertTrue(os.path.exists(script), f"❌ السكريبت {script} غير موجود")
        print("✅ جميع السكريبتات موجودة")
    
    def test_scripts_executable(self):
        """التحقق من صلاحيات التنفيذ (اختياري)"""
        scripts = [
            'scripts/run_realtime.py',
            'scripts/batch_validate.py',
        ]
        
        for script in scripts:
            if os.path.exists(script):
                is_exec = os.access(script, os.X_OK)
                print(f"🔹 {script}: {'✅ قابل للتنفيذ' if is_exec else '⚠️ غير قابل للتنفيذ'}")


if __name__ == '__main__':
    unittest.main()
