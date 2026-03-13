"""INFRAS-CLOUD Core Package
Atmospheric Infrasound & Severe Weather Acoustic Signatures
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Samir Baladi"
__email__ = "gitdeeper@gmail.com"
__doi__ = "10.5281/zenodo.18952438"

# رسالة ترحيب عند استيراد الحزمة
print("⚡ INFRAS-CLOUD v" + __version__)
print("📡 Atmospheric Infrasound & Severe Weather Acoustic Signatures")
print("🔗 DOI: " + __doi__)
print("-" * 50)

# محاولة استيراد numpy (اختياري)
try:
    import numpy as np
    HAS_NUMPY = True
    print("✅ NumPy available - Full functionality enabled")
except ImportError:
    HAS_NUMPY = False
    print("⚠️ NumPy not available - Limited functionality")
    print("   Install with: pkg install python-numpy")

# تصدير الوحدات الرئيسية
__all__ = [
    'InfrasProcessor',
    'BeamFormer',
    'DuctingAnalyzer',
    'AIEventClassifier',
    'MicrobaromAmplitude',
    'AtmosphericAbsorption',
    'InterStationCoherence',
    'AISI',
]

# استيراد الوحدات مع معالجة الأخطاء
try:
    from infras_core.processor import InfrasProcessor
    from infras_core.beamformer import BeamFormer
    from infras_core.ducting import DuctingAnalyzer
    from infras_core.classifier import AIEventClassifier
    from infras_core.microbarom import MicrobaromAmplitude
    from infras_core.absorption import AtmosphericAbsorption
    from infras_core.coherence import InterStationCoherence
    from infras_core.aisi import AISI
    print("✅ All modules loaded successfully")
except ImportError as e:
    print(f"⚠️ Some modules could not be loaded: {e}")
    print("   Full functionality requires NumPy and other dependencies")
