#!/data/data/com.termux/files/usr/bin/python
"""Weekly Report Generator"""

import os
import sys
import datetime

# Add main path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class WeeklyReportGenerator:
    """Weekly report generator"""
    
    def __init__(self, daily_dir="reports/daily", weekly_dir="reports/weekly"):
        self.daily_dir = daily_dir
        self.weekly_dir = weekly_dir
        os.makedirs(weekly_dir, exist_ok=True)
    
    def get_week_dates(self, date=None):
        """Get week dates"""
        if date is None:
            date = datetime.datetime.now()
        
        # Find week start (Sunday)
        start = date - datetime.timedelta(days=date.weekday() + 1)
        dates = [start + datetime.timedelta(days=i) for i in range(7)]
        return dates
    
    def generate_filename(self, date=None):
        """Generate weekly filename"""
        if date is None:
            date = datetime.datetime.now()
        
        week_dates = self.get_week_dates(date)
        start_str = week_dates[0].strftime("%Y%m%d")
        end_str = week_dates[-1].strftime("%Y%m%d")
        
        return f"weekly_{start_str}_to_{end_str}.txt"
    
    def collect_daily_reports(self, week_dates):
        """Collect daily reports for the week"""
        reports = []
        for day in week_dates:
            filename = day.strftime("report_%Y%m%d.txt")
            filepath = os.path.join(self.daily_dir, filename)
            if os.path.exists(filepath):
                reports.append(filepath)
        return reports
    
    def generate_report(self, date=None):
        """Generate weekly report"""
        if date is None:
            date = datetime.datetime.now()
        
        week_dates = self.get_week_dates(date)
        daily_reports = self.collect_daily_reports(week_dates)
        
        filename = self.generate_filename(date)
        filepath = os.path.join(self.weekly_dir, filename)
        
        # Generate content
        content = []
        content.append("=" * 60)
        content.append("⚡ INFRAS-CLOUD - Weekly Report")
        content.append("=" * 60)
        content.append(f"Week: {week_dates[0].strftime('%Y-%m-%d')} to {week_dates[-1].strftime('%Y-%m-%d')}")
        content.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("-" * 60)
        
        # Weekly statistics
        content.append("\n📊 Weekly Statistics:")
        content.append(f"   • Daily reports: {len(daily_reports)} of 7")
        content.append(f"   • Available days: {len(daily_reports)}")
        content.append(f"   • Missing days: {7 - len(daily_reports)}")
        content.append("")
        
        # Events summary
        content.append("🌪️ Events Summary:")
        for i, report in enumerate(daily_reports, 1):
            content.append(f"   Day {i}: {os.path.basename(report)}")
        content.append("")
        
        content.append("=" * 60)
        content.append("⚡ INFRAS-CLOUD - Acoustic Weather Intelligence System")
        content.append("=" * 60)
        
        # Save report
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        
        print(f"✅ Weekly report created: {filepath}")
        return filepath

def main():
    generator = WeeklyReportGenerator()
    generator.generate_report()

if __name__ == "__main__":
    main()
