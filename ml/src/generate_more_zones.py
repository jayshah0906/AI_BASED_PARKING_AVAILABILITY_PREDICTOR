"""
Generate more parking zones for better map visualization.
This will create 40 additional zones (50 total) spread across Seattle neighborhoods.
"""
import json
import random

# Seattle neighborhoods with approximate coordinates
NEIGHBORHOODS = {
    'Downtown': {
        'center': (47.6062, -122.3321),
        'radius': 0.01,
        'zones': 12,
        'type': 'commercial'
    },
    'Capitol Hill': {
        'center': (47.6205, -122.3212),
        'radius': 0.008,
        'zones': 8,
        'type': 'mixed'
    },
    'University District': {
        'center': (47.6615, -122.3132),
        'radius': 0.01,
        'zones': 8,
        'type': 'commercial'
    },
    'Fremont': {
        'center': (47.6505, -122.3493),
        'radius': 0.006,
        'zones': 6,
        'type': 'mixed'
    },
    'Ballard': {
        'center': (47.6685, -122.3840),
        'radius': 0.008,
        'zones': 7,
        'type': 'mixed'
    },
    'Queen Anne': {
        'center': (47.6369, -122.3573),
        'radius': 0.007,
        'zones': 6,
        'type': 'residential'
    },
    'South Lake Union': {
        'center': (47.6270, -122.3370),
        'radius': 0.005,
        'zones': 5,
        'type': 'commercial'
    },
    'Pioneer Square': {
        'center': (47.6020, -122.3340),
        'radius': 0.004,
        'zones': 4,
        'type': 'commercial'
    },
    'Stadium District': {
        'center': (47.5952, -122.3316),
        'radius': 0.005,
        'zones': 4,
        'type': 'event'
    }
}

STREET_NAMES = [
    'Pike St', '1st Ave', '2nd Ave', '3rd Ave', '4th Ave', '5th Ave',
    'Broadway', 'Pine St', 'Union St', 'University Way', 'Market St',
    'Fremont Ave', 'Stone Way', 'Westlake Ave', 'Dexter Ave',
    'Mercer St', 'Roy St', 'Republican St', 'Harrison St',
    'Thomas St', 'John St', 'Denny Way', 'Olive Way',
    '45th St', '50th St', 'NE Campus Pkwy', 'Brooklyn Ave',
    'Ballard Ave', 'Leary Way', 'Queen Anne Ave', 'Occidental Ave'
]

def generate_zones():
    """Generate parking zones for all neighborhoods."""
    zones = {}
    zone_counter = 1
    
    for neighborhood, config in NEIGHBORHOODS.items():
        center_lat, center_lon = config['center']
        radius = config['radius']
        num_zones = config['zones']
        zone_type = config['type']
        
        for i in range(num_zones):
            # Generate random position within neighborhood radius
            angle = random.uniform(0, 2 * 3.14159)
            distance = random.uniform(0, radius)
            
            lat = center_lat + (distance * random.choice([-1, 1]))
            lon = center_lon + (distance * random.choice([-1, 1]))
            
            # Generate zone ID
            zone_id = f"BF_{zone_counter:03d}"
            
            # Generate zone name
            street = random.choice(STREET_NAMES)
            zone_name = f"{neighborhood} - {street}"
            
            # Generate capacity (15-40 spaces)
            if zone_type == 'event':
                capacity = random.randint(25, 40)
            elif zone_type == 'commercial':
                capacity = random.randint(18, 30)
            else:  # mixed or residential
                capacity = random.randint(15, 25)
            
            zones[zone_id] = {
                'name': zone_name,
                'lat': round(lat, 4),
                'lon': round(lon, 4),
                'capacity': capacity,
                'type': zone_type
            }
            
            zone_counter += 1
    
    return zones

def main():
    """Generate and save zones."""
    print("Generating parking zones...")
    
    zones = generate_zones()
    
    print(f"Generated {len(zones)} zones:")
    for neighborhood, config in NEIGHBORHOODS.items():
        count = config['zones']
        print(f"  - {neighborhood}: {count} zones")
    
    # Save to file
    output_file = 'ml/data/processed/zones_metadata_extended.json'
    with open(output_file, 'w') as f:
        json.dump(zones, f, indent=2)
    
    print(f"\n✅ Zones saved to: {output_file}")
    print(f"\nTo use these zones:")
    print("1. Backup current zones: mv ml/data/processed/zones_metadata.json ml/data/processed/zones_metadata_backup.json")
    print("2. Use new zones: mv ml/data/processed/zones_metadata_extended.json ml/data/processed/zones_metadata.json")
    print("3. Update ml/src/config.py with new zone IDs")
    print("4. Generate training data: python ml/src/generate_sample_data.py")
    print("5. Retrain model: python ml/src/train.py")

if __name__ == "__main__":
    main()
