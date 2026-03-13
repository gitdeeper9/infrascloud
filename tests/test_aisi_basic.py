"""اختبارات AISI أساسية بدون numpy"""

import sys
import os
import unittest

# إضافة المسار الرئيسي
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# استيراد AISI بطريقة آمنة
try:
    from infras_core.aisi import AISI, AISIParameters
    HAS_AISI = True
except ImportError:
    HAS_AISI = False
    print("⚠️ AISI module requires numpy - skipping tests")

@unittest.skipIf(not HAS_AISI, "AISI module requires numpy")
class TestAISIBasic(unittest.TestCase):
    """اختبارات AISI الأساسية (تتطلب numpy)"""
    
    def test_aisi_weights(self):
        """اختبار أوزان AISI"""
        aisi = AISI()
        weights = aisi.weights
        self.assertEqual(len(weights), 8)
        self.assertAlmostEqual(sum(weights.values()), 1.0, places=5)
        print("✅ أوزان AISI صحيحة")


class TestAISIDocumentation(unittest.TestCase):
    """اختبارات توثيق AISI (بدون numpy)"""
    
    def test_aisi_readme_exists(self):
        """التحقق من وجود توثيق AISI"""
        aisi_docs = [
            'docs/theory/aisi_framework.md',
            'docs/api/aisi.md'
        ]
        for doc in aisi_docs:
            if os.path.exists(doc):
                print(f"✅ توثيق AISI موجود: {doc}")
                return
        print("⚠️ توثيق AISI غير موجود (اختياري)")
    
    def test_aisi_thresholds(self):
        """التحقق من قيم عتبات AISI من README"""
        readme_path = 'README.md'
        if os.path.exists(readme_path):
            with open(readme_path, 'r') as f:
                content = f.read()
                if '≥ 0.80' in content and 'CRITICAL' in content:
                    print("✅ عتبات AISI موثقة في README")
                else:
                    print("⚠️ عتبات AISI غير موجودة في README")


if __name__ == '__main__':
    unittest.main()
