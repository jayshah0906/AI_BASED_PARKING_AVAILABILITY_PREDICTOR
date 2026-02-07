"""
Generate MORE DIVERSE parking data with distinct zone personalities
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from config import ZONES, ZONE_METADATA

# Define DISTINCT zone personalities
ZONE_PERSONALITIES = {
    'BF_001': {  # Downtown Pike - VERY BUSY commercial
        'base': 0.75,
        'rush_multiplier': 1.3,
        'weekend_factor': -0.25,
        'lunch_boost': 0.15,
        'night_drop': -0.40
    },
    'BF_002': {  # Waterfront - Tourist area, busy afternoons
        'base': 0.70,
        'rush_multiplier': 1.1,
        'weekend_factor': 0.10,  # Busier on weekends!
        'lunch_boost': 0.20,
        'night_drop': -0.35
    },
    'BF_003': {  # Pioneer Square - Nightlife area
        'base': 0.65,
        'rush_multiplier': 1.2,
        'weekend_factor': 0.05,
        'lunch_boost': 0.10,
        'night_drop': -0.20  # Less drop at night!
    },
    'BF_045': {  # Stadium - EVENT DRIVEN
        'base': 0.45,  # Low base
        'rush_multiplier': 1.0,
        'weekend_factor': -0.10,
        'lunch_boost': 0.05,
        'night_drop': -0.25
    },
    'BF_046': {  # SoDo - Industrial, moderate
        'base': 0.50,
        'rush_multiplier': 1.15,
        'weekend_factor': -0.20,
        'lunch_boost': 0.10,
        'night_drop': -0.30
    },
    'BF_120': {  # Capitol Hill - Residential/nightlife mix
        'base': 0.60,
        'rush_multiplier': 1.1,
        'weekend_factor': 0.15,  # Busy weekends
        'lunch_boost': 0.08,
        'night_drop': -0.15  # Active at night
    },
    'BF_121': {  # Fremont - Artsy neighborhood
        'base': 0.55,
        'rush_multiplier': 1.05,
        'weekend_factor': 0.12,
        'lunch_boost': 0.12,
        'night_drop': -0.25
    },
    'BF_200': {  # University - Student area
        'base': 0.68,
        'rush_multiplier': 1.25,
        'weekend_factor': -0.30,  # Empty on weekends!
        'lunch_boost': 0.18,
        'night_drop': -0.35
    },
    'BF_201': {  # Ballard - Trendy neighborhood
        'base': 0.72,
        'rush_multiplier': 1.2,
        'weekend_factor': 0.08,
        'lunch_boost': 0.15,
        'night_drop': -0.30
    },
    'BF_202': {  # Green Lake - Park/recreation
        'base': 0.40,  # Low base
        'rush_multiplier': 0.9,  # Less affected by rush
        'weekend_factor': 0.25,  # MUCH busier on weekends!
        'lunch_boost': 0.10,
        'night_drop': -0.20
    }
}


def generate_diverse_parking_data(start_date='2023-01-01', end_date='2024-12-31'):
    """
    Generate synthetic parking data with DISTINCT zone personalities
    """
    print("Generating DIVERSE parking data...")
    print("Each zone has unique characteristics!")
    
    data = []
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    current = start
    record_count = 0
    
    while current <= end:
        for zone_id in ZONES:
            personality = ZONE_PERSONALITIES[zone_id]
            zone_info = ZONE_METADATA[zone_id]
            capacity = zone_info['capacity']
            
            # Start with zone's base occupancy
            occupancy_rate = personality['base']
            
            # Time of day pattern
            hour = current.hour
            if 7 <= hour <= 9:  # Morning rush
                occupancy_rate *= personality['rush_multiplier']
            elif 11 <= hour <= 14:  # Lunch
                occupancy_rate += personality['lunch_boost']
            elif 17 <= hour <= 19:  # Evening rush
                occupancy_rate *= personality['rush_multiplier']
            elif 20 <= hour <= 6:  # Night
                occupancy_rate += personality['night_drop']
            
            # Day of week pattern
            if current.weekday() >= 5:  # Weekend
                occupancy_rate += personality['weekend_factor']
            
            # Add zone-specific randomness (different variance per zone)
            if zone_id in ['BF_045', 'BF_046']:  # Stadium zones more variable
                noise = np.random.normal(0, 0.12)
            elif zone_id in ['BF_001', 'BF_200']:  # Busy zones more consistent
                noise = np.random.normal(0, 0.06)
            else:
                noise = np.random.normal(0, 0.08)
            
            occupancy_rate += noise
            
            # Clip to valid range
            occupancy_rate = max(0.05, min(0.98, occupancy_rate))
            
            # Calculate spaces
            occupied_spaces = int(occupancy_rate * capacity)
            
            data.append({
                'blockface_id': zone_id,
                'datetime': current.isoformat(),
                'occupied_spaces': occupied_spaces,
                'total_spaces': capacity,
                'occupancy_rate': round(occupancy_rate, 3)
            })
            
            record_count += 1
            if record_count % 50000 == 0:
                print(f"  Generated {record_count} records...")
        
        # Move to next hour
        current += timedelta(hours=1)
    
    df = pd.DataFrame(data)
    print(f"✅ Generated {len(df)} records with DIVERSE patterns")
    return df


def main():
    """Generate diverse data"""
    print("=" * 70)
    print("GENERATING DIVERSE PARKING DATA")
    print("=" * 70)
    print("This will create data with DISTINCT zone personalities:")
    print("  - Downtown Pike: Very busy commercial")
    print("  - Stadium: Event-driven, low base")
    print("  - University: Busy weekdays, empty weekends")
    print("  - Green Lake: Park area, busy weekends")
    print("  - etc.")
    print()
    
    # Generate diverse data
    parking_df = generate_diverse_parking_data('2023-01-01', '2024-12-31')
    
    # Save
    output_path = 'ml/data/processed/parking_data.json'
    print(f"\nSaving to {output_path}...")
    parking_df.to_json(output_path, orient='records', indent=2)
    
    # Show statistics
    print("\n" + "=" * 70)
    print("DATA STATISTICS:")
    print("=" * 70)
    for zone_id in ZONES:
        zone_data = parking_df[parking_df['blockface_id'] == zone_id]
        avg_occ = zone_data['occupancy_rate'].mean()
        std_occ = zone_data['occupancy_rate'].std()
        print(f"{zone_id}: Avg={avg_occ*100:.1f}% Std={std_occ*100:.1f}%")
    
    print("\n" + "=" * 70)
    print("✅ DONE! Now retrain the model:")
    print("   python ml/src/train.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
