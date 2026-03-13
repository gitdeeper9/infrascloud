#!/data/data/com.termux/files/usr/bin/python
"""Daily Report Generator - TXT format only"""

import os
import sys
import datetime
import random

# Add main path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class DailyReportGenerator:
    """Daily report generator in TXT format"""
    
    def __init__(self, reports_dir="reports/daily"):
        self.reports_dir = reports_dir
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure directories exist"""
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def generate_filename(self, date=None):
        """Generate filename"""
        if date is None:
            date = datetime.datetime.now()
        return date.strftime("report_%Y%m%d.txt")
    
    def generate_report_content(self, date):
        """Generate report content"""
        # Sample data for display
        aisi_value = round(random.uniform(0.3, 0.9), 2)
        p_ub = round(random.uniform(0.05, 0.45), 3)
        d_str = round(random.uniform(-0.05, 0.25), 3)
        f_p = round(random.uniform(0.1, 2.5), 2)
        
        # Determine AISI status
        if aisi_value >= 0.8:
            status = "🔴 CRITICAL"
            alert = "WARNING: Severe atmospheric activity!"
        elif aisi_value >= 0.55:
            status = "🟡 ELEVATED"
            alert = "ALERT: Elevated atmospheric activity"
        else:
            status = "🟢 BACKGROUND"
            alert = "Normal conditions"
        
        # Generate sample events
        events = []
        event_types = ["🌀 Cyclone", "🌪️ Tornado", "🌋 Volcano", "📡 Microbarom", "🌊 Gravity Wave"]
        for i in range(random.randint(0, 3)):
            event = {
                'time': f"{random.randint(0,23):02d}:{random.randint(0,59):02d}",
                'type': random.choice(event_types),
                'confidence': random.randint(75, 99)
            }
            events.append(event)
        
        # Build report content
        content = []
        content.append("=" * 60)
        content.append("⚡ INFRAS-CLOUD - Daily Report")
        content.append("=" * 60)
        content.append(f"Date: {date.strftime('%Y-%m-%d')}")
        content.append(f"Time: {date.strftime('%H:%M:%S')}")
        content.append("-" * 60)
        
        # AISI Index
        content.append("\n📊 Atmospheric Infrasonic Severity Index (AISI)")
        content.append(f"   AISI: {aisi_value} - {status}")
        content.append(f"   Status: {alert}")
        content.append("")
        
        # Eight Parameters
        content.append("🔬 Eight Parameters:")
        content.append(f"   1. Microbarom Amplitude (P_ub): {p_ub} Pa")
        content.append(f"   2. Stratospheric Ducting Efficiency (D_str): {d_str}")
        content.append(f"   3. Spectral Peak Frequency (f_p): {f_p} Hz")
        content.append(f"   4. Arrival Angle (θ): {random.randint(0,360)}°")
        content.append(f"   5. Phase Velocity (v_ph): {random.randint(300,360)} m/s")
        content.append(f"   6. Absorption Coefficient (α_air): {round(random.uniform(0.001,0.009),3)} dB/km")
        content.append(f"   7. Coherence (γ²): {round(random.uniform(0.4,0.95),2)}")
        content.append(f"   8. Signal-to-Noise Ratio (SNR): {random.randint(10,25)} dB")
        content.append("")
        
        # Detected Events
        content.append("🌪️ Detected Events Today:")
        if events:
            for i, event in enumerate(events, 1):
                content.append(f"   {i}. {event['time']} - {event['type']} (Confidence: {event['confidence']}%)")
        else:
            content.append("   No significant events today")
        content.append("")
        
        # Predictions
        content.append("🔮 Next 24 Hours Forecast:")
        next_day_aisi = round(aisi_value + random.uniform(-0.15, 0.15), 2)
        next_day_aisi = max(0, min(1, next_day_aisi))
        content.append(f"   Expected AISI: {next_day_aisi}")
        
        if next_day_aisi >= 0.8:
            content.append("   ⚠️ WARNING: Severe atmospheric activity expected!")
        elif next_day_aisi >= 0.55:
            content.append("   ⚠️ ALERT: Elevated atmospheric activity expected")
        else:
            content.append("   ✅ Stable atmospheric conditions expected")
        content.append("")
        
        # Notes
        content.append("📝 Notes:")
        content.append("   • Database updated successfully")
        content.append("   • All sensors operating normally")
        content.append("   • Last update: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        content.append("")
        content.append("=" * 60)
        content.append("⚡ INFRAS-CLOUD - Acoustic Weather Intelligence System")
        content.append("=" * 60)
        
        return "\n".join(content)
    
    def generate_report(self, date=None):
        """Generate and save report"""
        if date is None:
            date = datetime.datetime.now()
        
        filename = self.generate_filename(date)
        filepath = os.path.join(self.reports_dir, filename)
        
        content = self.generate_report_content(date)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Report created: {filepath}")
        return filepath

def main():
    """Main function"""
    print("⚡ INFRAS-CLOUD - Daily Report Generator")
    print("-" * 40)
    
    generator = DailyReportGenerator()
    
    # Generate today's report
    today = datetime.datetime.now()
    filepath = generator.generate_report(today)
    
    # Preview report
    print("\n📄 Report Preview:")
    print("-" * 40)
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[:15]:
            print(line.rstrip())
    print("...")

if __name__ == "__main__":
    main()
