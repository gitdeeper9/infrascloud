#!/data/data/com.termux/files/usr/bin/bash

echo "⚡ INFRAS-CLOUD Test Suite"
echo "========================="
echo ""

# الألوان للتنسيق
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# تشغيل الاختبارات الأساسية
echo -e "${YELLOW}تشغيل الاختبارات الأساسية...${NC}"
python tests/test_basic.py

echo ""
echo -e "${YELLOW}تشغيل اختبارات AISI الأساسية...${NC}"
python tests/test_aisi_basic.py

echo ""
echo -e "${YELLOW}تشغيل اختبارات السكريبتات...${NC}"
python tests/test_scripts_basic.py

echo ""
echo "========================="
echo -e "${GREEN}✅ جميع الاختبارات المكتملة${NC}"
echo "ملاحظة: بعض الاختبارات تطلب numpy وتحتاج بيئة كاملة"
