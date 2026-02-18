#!/usr/bin/env python3
"""
Image Generator for Gynecology Clinic Website
Generates placeholder SVG images for the website
"""

import os
import base64
from pathlib import Path

def create_images_directory():
    """Create images directory if it doesn't exist"""
    images_dir = Path('images')
    images_dir.mkdir(exist_ok=True)
    return images_dir

def create_logo_svg():
    """Create logo SVG"""
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
    <circle cx="100" cy="100" r="95" fill="#16a085" stroke="#0f3460" stroke-width="2"/>
    <circle cx="100" cy="100" r="80" fill="#e8f1f5" stroke="#16a085" stroke-width="2"/>
    <text x="100" y="110" font-family="Arial, sans-serif" font-size="48" font-weight="bold" text-anchor="middle" fill="#0f3460">♀</text>
    <text x="100" y="165" font-family="Arial, sans-serif" font-size="14" font-weight="bold" text-anchor="middle" fill="#0f3460">ΚΛΙΝΙΚΗ</text>
</svg>'''
    return svg_content

def create_hero_banner_svg():
    """Create hero banner SVG"""
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600">
    <defs>
        <linearGradient id="heroGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#16a085;stop-opacity:0.3" />
            <stop offset="100%" style="stop-color:#0f3460;stop-opacity:0.3" />
        </linearGradient>
    </defs>
    <rect width="1200" height="600" fill="#e8f1f5"/>
    <rect width="1200" height="600" fill="url(#heroGrad)"/>
    <circle cx="300" cy="150" r="80" fill="#16a085" opacity="0.2"/>
    <circle cx="900" cy="450" r="120" fill="#0f3460" opacity="0.1"/>
    <path d="M 200 400 Q 300 300 400 400 T 600 400" stroke="#16a085" stroke-width="2" fill="none" opacity="0.3"/>
    <text x="600" y="250" font-family="Arial, sans-serif" font-size="48" font-weight="bold" text-anchor="middle" fill="#0f3460">Ιατρική Φροντίδα</text>
    <text x="600" y="300" font-family="Arial, sans-serif" font-size="24" text-anchor="middle" fill="#16a085">Με Ειδίκευση</text>
    <rect x="100" y="350" width="1000" height="3" fill="#16a085" opacity="0.5"/>
</svg>'''
    return svg_content

def create_doctor_profile_svg():
    """Create doctor profile SVG"""
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500">
    <defs>
        <linearGradient id="docGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#16a085;stop-opacity:0.1" />
            <stop offset="100%" style="stop-color:#0f3460;stop-opacity:0.2" />
        </linearGradient>
    </defs>
    <rect width="400" height="500" fill="url(#docGrad)"/>
    <circle cx="200" cy="120" r="70" fill="#16a085"/>
    <circle cx="200" cy="120" r="65" fill="#e8f1f5"/>
    <circle cx="185" cy="105" r="8" fill="#0f3460"/>
    <circle cx="215" cy="105" r="8" fill="#0f3460"/>
    <path d="M 190 140 L 210 140" stroke="#0f3460" stroke-width="2"/>
    <path d="M 185 150 Q 200 160 215 150" stroke="#0f3460" stroke-width="2" fill="none"/>
    <path d="M 100 220 L 300 220 Q 300 250 200 280 Q 100 250 100 220" fill="#16a085" opacity="0.6"/>
    <path d="M 80 280 L 320 280 L 350 400 Q 200 450 50 400 Z" fill="#16a085" opacity="0.5"/>
    <text x="200" y="480" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#0f3460">Γυναικολόγος</text>
</svg>'''
    return svg_content

def create_service_icon_svg(service_number):
    """Create service icon SVG based on service number"""
    icons = {
        1: '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
    <circle cx="100" cy="100" r="95" fill="#e8f1f5" stroke="#16a085" stroke-width="2"/>
    <g transform="translate(50, 50)">
        <rect x="20" y="10" width="30" height="50" rx="5" fill="#0f3460"/>
        <circle cx="35" cy="70" r="15" fill="#16a085"/>
        <path d="M 35 20 L 50 10 L 65 20" fill="#16a085"/>
    </g>
    <text x="100" y="160" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#0f3460">Εξετάσεις</text>
</svg>''',
        2: '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
    <circle cx="100" cy="100" r="95" fill="#e8f1f5" stroke="#16a085" stroke-width="2"/>
    <path d="M 100 40 L 140 70 L 140 130 Q 100 150 60 130 L 60 70 Z" fill="#16a085" stroke="#0f3460" stroke-width="2"/>
    <circle cx="100" cy="90" r="20" fill="#e8f1f5"/>
    <path d="M 80 80 Q 100 100 120 80" stroke="#0f3460" stroke-width="2" fill="none"/>
    <text x="100" y="160" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#0f3460">Υπερηχογραφίες</text>
</svg>''',
        3: '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
    <circle cx="100" cy="100" r="95" fill="#e8f1f5" stroke="#16a085" stroke-width="2"/>
    <path d="M 70 60 Q 70 80 85 90 L 85 130 Q 85 140 75 140 L 65 140 Q 55 140 55 130 L 55 90 Q 70 80 70 60" fill="#0f3460"/>
    <path d="M 130 60 Q 130 80 115 90 L 115 130 Q 115 140 125 140 L 135 140 Q 145 140 145 130 L 145 90 Q 130 80 130 60" fill="#16a085"/>
    <circle cx="100" cy="75" r="8" fill="#e8f1f5"/>
    <text x="100" y="160" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#0f3460">Κολποσκοπία</text>
</svg>''',
        4: '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
    <circle cx="100" cy="100" r="95" fill="#e8f1f5" stroke="#16a085" stroke-width="2"/>
    <rect x="60" y="50" width="80" height="100" rx="5" fill="#16a085" opacity="0.3" stroke="#0f3460" stroke-width="2"/>
    <circle cx="75" cy="70" r="6" fill="#0f3460"/>
    <circle cx="100" cy="70" r="6" fill="#0f3460"/>
    <circle cx="125" cy="70" r="6" fill="#0f3460"/>
    <path d="M 65 100 L 135 100 M 65 120 L 135 120" stroke="#0f3460" stroke-width="1.5"/>
    <text x="100" y="160" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="#0f3460">Παπανικολάου</text>
</svg>'''
    }
    return icons.get(service_number, icons[1])

def save_svg_as_png_data_uri(svg_content, filename):
    """Convert SVG to data URI and save reference"""
    # For simplicity, we'll just save the SVG directly
    # In production, you'd convert to PNG
    svg_b64 = base64.b64encode(svg_content.encode()).decode()
    data_uri = f"data:image/svg+xml;base64,{svg_b64}"
    return data_uri, svg_content

def generate_all_images():
    """Generate all required images"""
    images_dir = create_images_directory()
    
    images_data = {
        'logo': create_logo_svg(),
        'hero-banner': create_hero_banner_svg(),
        'doctor-profile': create_doctor_profile_svg(),
        'service-1': create_service_icon_svg(1),
        'service-2': create_service_icon_svg(2),
        'service-3': create_service_icon_svg(3),
        'service-4': create_service_icon_svg(4),
    }
    
    # Save SVG files
    for name, svg_content in images_data.items():
        filepath = images_dir / f'{name}.svg'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f'✓ Created: {filepath}')
    
    # Create a data URIs file for reference
    data_uris = {}
    for name, svg_content in images_data.items():
        svg_b64 = base64.b64encode(svg_content.encode()).decode()
        data_uri = f"data:image/svg+xml;base64,{svg_b64}"
        data_uris[name] = data_uri
    
    # Save data URIs to a file
    with open(images_dir / 'data_uris.txt', 'w', encoding='utf-8') as f:
        for name, uri in data_uris.items():
            f.write(f'{name}:\n{uri}\n\n')
    
    print('✓ Created: images/data_uris.txt')
    print('\n✓ Image generation completed successfully!')

if __name__ == '__main__':
    try:
        generate_all_images()
    except Exception as e:
        print(f'✗ Error generating images: {e}')
        exit(1)
