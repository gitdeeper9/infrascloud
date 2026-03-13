#!/data/data/com.termux/files/usr/bin/python
"""Alerts Generator System"""

import os
import sys
import datetime

# Add main path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class AlertGenerator:
    """Alerts generator"""
    
    def __init__(self, alerts_dir="reports/alerts"):
        self.alerts_dir = alerts_dir
        os.makedirs(alerts_dir, exist_ok=True)
    
    def generate_alert(self, alert_type, message, aisi_value=None):
        """Generate new alert"""
        timestamp = datetime.datetime.now()
        filename = timestamp.strftime("alert_%Y%m%d_%H%M%S.txt")
        filepath = os.path.join(self.alerts_dir, filename)
        
        # Determine alert level
        if alert_type == "CRITICAL":
            level = "🔴 CRITICAL"
        elif alert_type == "ELEVATED":
            level = "🟡 ELEVATED"
        else:
            level = "🔵 INFO"
        
        # Generate content
        content = []
        content.append("=" * 60)
        content.append("⚡ INFRAS-CLOUD - Alert")
        content.append("=" * 60)
        content.append(f"Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        content.append(f"Level: {level}")
        content.append(f"Type: {alert_type}")
        if aisi_value:
            content.append(f"AISI: {aisi_value}")
        content.append("-" * 60)
        content.append(f"\n{message}\n")
        content.append("=" * 60)
        content.append("⚡ INFRAS-CLOUD - Acoustic Weather Intelligence System")
        content.append("=" * 60)
        
        # Save alert
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        
        print(f"🚨 Alert created: {filepath}")
        return filepath
    
    def check_aisi_thresholds(self, aisi_value):
        """Check AISI thresholds and create alerts"""
        if aisi_value >= 0.8:
            return self.generate_alert(
                "CRITICAL",
                f"⚠️ CRITICAL AISI: {aisi_value}\nSevere atmospheric activity likely!",
                aisi_value
            )
        elif aisi_value >= 0.55:
            return self.generate_alert(
                "ELEVATED",
                f"⚠️ ELEVATED AISI: {aisi_value}\nIncreased atmospheric activity detected.",
                aisi_value
            )
        return None

def main():
    """Generate sample alerts"""
    import random
    
    generator = AlertGenerator()
    
    print("⚡ Generating sample alerts...")
    
    # Info alert
    generator.generate_alert("INFO", "✅ All sensors operating normally")
    
    # Elevated alert
    generator.generate_alert("ELEVATED", "⚠️ Increased seismic activity in region")
    
    # Critical alert
    generator.generate_alert("CRITICAL", "🔴 Potential tornado within 15-20 minutes")
    
    # Check random AISI
    aisi = round(random.uniform(0.4, 0.95), 2)
    print(f"\n📊 Checking AISI = {aisi}")
    generator.check_aisi_thresholds(aisi)

if __name__ == "__main__":
    main()
