#!/usr/bin/env python3
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, 'ml/src')
os.chdir('ml/src')

from predict import load_model
load_model()
from predict import HISTORICAL_DF

print("=" * 70)
print("DEBUGGING SIMILAR PREDICTIONS ISSUE")
print("=" * 70)

# Check date range
print(f"\n📅 Historical data range:")
print(f"  From: {HISTORICAL_DF['datetime'].min()}")
print(f"  To: {HISTORICAL_DF['datetime'].max()}")

# Check what happens when we look for 2026 data
target_date = datetime(2026, 2, 7, 14, 0, 0)
print(f"\n🎯 Predicting for: {target_date} (Friday, 2 PM)")
print(f"  ⚠️  This is AFTER the historical data ends!")

# Check historical patterns for different zones
print(f"\n📊 Historical patterns (Friday 2 PM):")
zones = [
    ('BF_001', 'Zone 1 - Downtown Pike'),
    ('BF_045', 'Zone 6 - Stadium'),
    ('BF_200', 'Zone 5 - University')
]

for zone_id, zone_name in zones:
    zone_data = HISTORICAL_DF[
        (HISTORICAL_DF['blockface_id'] == zone_id) &
        (HISTORICAL_DF['datetime'].dt.hour == 14) &
        (HISTORICAL_DF['datetime'].dt.weekday == 4)  # Friday
    ]
    if len(zone_data) > 0:
        avg = zone_data['occupancy_rate'].mean()
        std = zone_data['occupancy_rate'].std()
        print(f"  {zone_name}:")
        print(f"    Records: {len(zone_data)}")
        print(f"    Avg occupancy: {avg:.3f} ({avg*100:.1f}%)")
        print(f"    Std dev: {std:.3f}")
    else:
        print(f"  {zone_name}: NO DATA")

# Check lag features
print(f"\n⏰ Lag features (24h ago from prediction):")
lag_24h = target_date - timedelta(hours=24)
print(f"  Looking for: {lag_24h}")
print(f"  Latest data: {HISTORICAL_DF['datetime'].max()}")
print(f"  Gap: {(lag_24h - HISTORICAL_DF['datetime'].max()).days} days")

for zone_id, zone_name in zones:
    lag_data = HISTORICAL_DF[
        (HISTORICAL_DF['blockface_id'] == zone_id) &
        (HISTORICAL_DF['datetime'] >= lag_24h - timedelta(minutes=30)) &
        (HISTORICAL_DF['datetime'] <= lag_24h + timedelta(minutes=30))
    ]
    print(f"  {zone_name}: {len(lag_data)} records")

# Check overall zone averages
print(f"\n📈 Overall zone averages (all time):")
for zone_id, zone_name in zones:
    zone_all = HISTORICAL_DF[HISTORICAL_DF['blockface_id'] == zone_id]
    if len(zone_all) > 0:
        avg = zone_all['occupancy_rate'].mean()
        print(f"  {zone_name}: {avg:.3f} ({avg*100:.1f}%)")

print("\n" + "=" * 70)
print("DIAGNOSIS:")
print("=" * 70)
print("❌ PROBLEM: Predicting for 2026, but data only goes to 2024")
print("❌ RESULT: Lag features return fallback values (zone averages)")
print("❌ RESULT: All zones use similar fallback logic")
print("❌ RESULT: Predictions are similar across zones")
print("=" * 70)
