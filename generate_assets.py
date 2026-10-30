"""
Generate branding and sample visual assets for NIVORA
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / 'static' / 'images'
PG_IMG_DIR = IMG_DIR / 'pg'
UPLOADS_DIR = BASE_DIR / 'static' / 'uploads'

IMG_DIR.mkdir(parents=True, exist_ok=True)
PG_IMG_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# 1. Main NIVORA Logo (Vector SVG)
logo_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 350 80" width="350" height="80">
  <defs>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F5E6B3"/>
      <stop offset="50%" stop-color="#D4AF37"/>
      <stop offset="100%" stop-color="#9A7B1C"/>
    </linearGradient>
    <filter id="goldGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>
  
  <!-- Icon: Location pin merged with roof/house -->
  <g transform="translate(10, 10)">
    <!-- Pin outer ring -->
    <path d="M30,5 C16.2,5 5,16.2 5,30 C5,46 30,62 30,62 C30,62 55,46 55,30 C55,16.2 43.8,5 30,5 Z" 
          fill="#111111" stroke="url(#goldGrad)" stroke-width="2.5" />
    
    <!-- Stylized Roof & Door inside Pin -->
    <polygon points="30,16 17,29 21,29 21,43 39,43 39,29 43,29" fill="url(#goldGrad)" />
    <!-- Doorway cut -->
    <rect x="27" y="32" width="6" height="11" rx="2" fill="#111111" />
    <!-- Golden Accent Dot -->
    <circle cx="30" cy="24" r="2.5" fill="#FFFFFF" />
  </g>
  
  <!-- Text: NIVORA -->
  <text x="80" y="47" font-family="'Poppins', 'Cinzel', 'Montserrat', sans-serif" font-size="34" font-weight="800" letter-spacing="3" fill="#FFFFFF">
    NI<tspan fill="url(#goldGrad)">VO</tspan>RA
  </text>
  
  <!-- Tagline below NIVORA -->
  <text x="82" y="64" font-family="'Inter', sans-serif" font-size="8.5" font-weight="600" letter-spacing="2" fill="#D4AF37">
    FIND YOUR PLACE. FEEL AT HOME.
  </text>
</svg>"""

# 2. Favicon SVG
favicon_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <linearGradient id="favGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F5E6B3"/>
      <stop offset="50%" stop-color="#D4AF37"/>
      <stop offset="100%" stop-color="#9A7B1C"/>
    </linearGradient>
  </defs>
  <rect width="64" height="64" rx="14" fill="#0A0A0A"/>
  <path d="M32,6 C19,6 8.5,16.5 8.5,29.5 C8.5,44 32,58 32,58 C32,58 55.5,44 55.5,29.5 C55.5,16.5 45,6 32,6 Z" 
        fill="#141414" stroke="url(#favGold)" stroke-width="2.5" />
  <polygon points="32,16 20,28 23,28 23,41 41,41 41,28 44,28" fill="url(#favGold)" />
  <rect x="29" y="31" width="6" height="10" rx="1" fill="#0A0A0A" />
</svg>"""

with open(IMG_DIR / 'logo.svg', 'w', encoding='utf-8') as f:
    f.write(logo_svg)

with open(IMG_DIR / 'favicon.svg', 'w', encoding='utf-8') as f:
    f.write(favicon_svg)

# 3. Create Sample PG Images
pg_themes = [
    ("Aurum Luxe Coliving", "Suite & Rooftop Lounge", "#1F1B18", "#D4AF37", "Koramangala 4th Block"),
    ("The Ivy Executive", "Women's Luxury Haven", "#1B221E", "#4E9F76", "Indiranagar 100ft Rd"),
    ("Nexus Tech Living", "Modern Men's Residency", "#161B26", "#3A86FF", "HSR Layout Sector 3"),
    ("Zenith Heights", "Outer Ring Road Tech View", "#231E17", "#E0A96D", "Bellandur EcoWorld"),
    ("BTM Comfort Residency", "Budget & Student Friendly", "#1E1E24", "#9B5DE5", "BTM Layout 2nd Stage"),
    ("Silicon Oasis Suites", "Studio Style Co-living", "#15202B", "#00B4D8", "Whitefield ITPL"),
    ("TechVille Elite Men", "Walking distance to Infosys", "#1A1A24", "#FFB703", "Electronic City Phase 1"),
    ("Serene Haven Ladies", "Spacious & Peaceful", "#241822", "#F72585", "Jayanagar 4th Block"),
    ("Marathahalli Urban", "Connected & Economical", "#1E221B", "#80B918", "Marathahalli ORR"),
    ("Sarjapur Grand Coliving", "Luxury Co-living & Gym", "#201815", "#FB8500", "Sarjapur Road"),
    ("Manyata View Ladies", "Opposite Manyata Tech Park", "#192229", "#2EC4B6", "Hebbal Manyata"),
    ("Metro Link Residency", "Steps from Metro Station", "#251D18", "#DDA15E", "Rajajinagar 2nd Block")
]

def make_pg_svg(title, subtitle, bg_color, accent_color, location, room_label="Executive Room"):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="800" height="500">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg_color}"/>
      <stop offset="100%" stop-color="#090909"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{accent_color}"/>
      <stop offset="100%" stop-color="#D4AF37"/>
    </linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="1"/>
    </pattern>
  </defs>

  <rect width="800" height="500" fill="url(#bgGrad)"/>
  <rect width="800" height="500" fill="url(#grid)"/>

  <!-- Interior Architectural Illustration Artwork -->
  <g transform="translate(100, 70)" opacity="0.9">
    <!-- Room perspective walls -->
    <polygon points="0,0 600,0 500,70 100,70" fill="rgba(255,255,255,0.02)"/>
    <polygon points="100,70 500,70 500,280 100,280" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.08)"/>
    
    <!-- Big Window with Bangalore City Silhouette -->
    <rect x="340" y="90" width="140" height="130" rx="4" fill="#0C1017" stroke="rgba(255,255,255,0.15)"/>
    <line x1="410" y1="90" x2="410" y2="220" stroke="rgba(255,255,255,0.15)" stroke-width="2"/>
    <line x1="340" y1="155" x2="480" y2="155" stroke="rgba(255,255,255,0.15)" stroke-width="2"/>
    <!-- City silhouette lights -->
    <rect x="360" y="160" width="18" height="55" fill="#1C2536"/>
    <rect x="390" y="140" width="22" height="75" fill="#222E42"/>
    <rect x="425" y="150" width="25" height="65" fill="#18202D"/>
    <circle cx="450" cy="115" r="8" fill="#FFF275" opacity="0.7"/>

    <!-- Modern Platform Bed with Luxury Gold Linens -->
    <polygon points="130,220 290,220 310,270 110,270" fill="#202025" stroke="{accent_color}" stroke-width="1.5"/>
    <rect x="140" y="200" width="140" height="22" rx="4" fill="url(#accentGrad)"/>
    <!-- Pillows -->
    <rect x="150" y="185" width="50" height="15" rx="3" fill="#EDEDED"/>
    <rect x="215" y="185" width="50" height="15" rx="3" fill="#EDEDED"/>

    <!-- Workstation Desk & Lamp -->
    <rect x="330" y="225" width="150" height="8" rx="2" fill="{accent_color}"/>
    <rect x="345" y="233" width="6" height="37" fill="#444"/>
    <rect x="460" y="233" width="6" height="37" fill="#444"/>
    <!-- Laptop -->
    <polygon points="380,210 420,210 426,225 374,225" fill="#888"/>
    <rect x="382" y="196" width="36" height="15" rx="2" fill="#EAEAEA" stroke="#333"/>

    <!-- Ambient Pendant Lamp Hanging -->
    <line x1="220" y1="70" x2="220" y2="130" stroke="{accent_color}" stroke-width="1.5"/>
    <polygon points="205,145 235,145 228,130 212,130" fill="url(#accentGrad)"/>
    <circle cx="220" cy="148" r="4" fill="#FFEAA7"/>
  </g>

  <!-- Dark gradient scrim at bottom for text contrast -->
  <rect x="0" y="320" width="800" height="180" fill="url(#bottomScrim)"/>
  <defs>
    <linearGradient id="bottomScrim" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="transparent"/>
      <stop offset="60%" stop-color="#080808" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#080808"/>
    </linearGradient>
  </defs>

  <!-- Tag Pill -->
  <g transform="translate(40, 360)">
    <rect width="130" height="26" rx="13" fill="rgba(212, 175, 55, 0.2)" stroke="{accent_color}" stroke-width="1"/>
    <text x="65" y="17" font-family="'Inter', sans-serif" font-size="11" font-weight="700" fill="{accent_color}" text-anchor="middle">
      {room_label}
    </text>
  </g>

  <!-- Title & Meta -->
  <text x="40" y="420" font-family="'Poppins', sans-serif" font-size="28" font-weight="700" fill="#FFFFFF">
    {title}
  </text>
  <text x="40" y="450" font-family="'Inter', sans-serif" font-size="14" font-weight="500" fill="#B0B0B0">
    📍 {location}  •  {subtitle}
  </text>

  <!-- Watermark -->
  <text x="760" y="470" font-family="'Poppins', sans-serif" font-size="12" font-weight="700" fill="rgba(212, 175, 55, 0.5)" letter-spacing="2" text-anchor="end">
    NIVORA VERIFIED
  </text>
</svg>"""

# Generate 12 sample PG images + sub photos
for i, theme in enumerate(pg_themes, 1):
    title, subtitle, bg_color, accent_color, location = theme
    main_svg = make_pg_svg(title, subtitle, bg_color, accent_color, location, "Primary Suite")
    with open(PG_IMG_DIR / f"pg{i}_main.svg", 'w', encoding='utf-8') as f:
        f.write(main_svg)
    
    # Generate secondary photo for top listings
    if i in [1, 2, 3, 4, 6]:
        room_svg = make_pg_svg(f"{title} - Private Space", "Ergonomic Desk & Balcony", bg_color, accent_color, location, "Bedroom View")
        with open(PG_IMG_DIR / f"pg{i}_room.svg", 'w', encoding='utf-8') as f:
            f.write(room_svg)
    
    if i == 1:
        lounge_svg = make_pg_svg(f"{title} - Sky Lounge", "Rooftop Cafeteria & Co-working", bg_color, accent_color, location, "Common Lounge")
        with open(PG_IMG_DIR / f"pg1_lounge.svg", 'w', encoding='utf-8') as f:
            f.write(lounge_svg)

# Default Placeholder
placeholder_svg = make_pg_svg("NIVORA Accommodation", "Comfort & Convenience in Bangalore", "#141414", "#D4AF37", "Bangalore", "Verified PG")
with open(PG_IMG_DIR / 'placeholder.svg', 'w', encoding='utf-8') as f:
    f.write(placeholder_svg)

print("All branding & PG SVG assets generated successfully!")

