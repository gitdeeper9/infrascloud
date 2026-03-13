#!/data/data/com.termux/files/usr/bin/bash

echo "⚡ INFRAS-CLOUD - Complete Report Generator"
echo "============================================"
echo ""

# Generate daily report
echo "📅 Generating daily report..."
python scripts/generate_daily_report.py

echo ""
# Generate weekly report
echo "📆 Generating weekly report..."
python scripts/generate_weekly_report.py

echo ""
# Generate monthly report
echo "📊 Generating monthly report..."
python scripts/generate_monthly_report.py

echo ""
# Generate alerts
echo "🚨 Generating alerts..."
python scripts/generate_alerts.py

echo ""
echo "============================================"
echo "✅ All reports generated successfully!"
tree reports/
