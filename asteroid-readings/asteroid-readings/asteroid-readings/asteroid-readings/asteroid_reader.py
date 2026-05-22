import swisseph as swe
import datetime
from datetime import timedelta
import os
from dotenv import load_dotenv

# === YOUR PERSONAL BRANDING ===
YOUR_NAME = "Danielle Paige"
WEBSITE_URL = "https://daniellepaige.com/"
SERVICES_URL = "https://daniellepaige.com/services/"   # Change if your services link is different

print("=== Daily Asteroid Reader Starting ===")

def deg_to_zodiac(deg):
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    sign_num = int(deg // 30)
    degree = deg % 30
    return f"{int(degree):02d}° {signs[sign_num]}"

def get_asteroid_positions(target_date):
    jd = swe.julday(target_date.year, target_date.month, target_date.day, 0.0)
    positions = {}
    asteroids = {"Ceres": 1, "Pallas": 2, "Juno": 3, "Vesta": 4}
    
    for name, iid in asteroids.items():
        try:
            pos, _ = swe.calc(jd, iid, swe.FLG_SWIEPH)
            lon = pos[0] % 360
            positions[name] = deg_to_zodiac(lon)
        except:
            positions[name] = "Position unavailable (ephemeris missing)"
    return positions

def generate_reading(target_date):
    positions = get_asteroid_positions(target_date)
    
    md = f"""# 🌠 Daily Asteroid Reading — {target_date.strftime('%B %d, %Y')}

**by {YOUR_NAME}**  
[🌐 Website]({WEBSITE_URL}) | [📅 Book a Session]({SERVICES_URL})

---

"""
    for name, pos in positions.items():
        md += f"### {name} at {pos}\n**Vibe**: [Add short interpretation here]\n\n"
    
    md += "**Overall Theme**: Grounding, strategy, partnerships, and focused devotion.\n\n"
    md += f"For personalized readings combining these asteroids with your natal chart, visit [my services]({SERVICES_URL})."
    
    # Save the file
    os.makedirs("readings", exist_ok=True)
    filename = f"readings/asteroid_{target_date.strftime('%Y-%m-%d')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md)
    
    print(f"✅ Created: {filename}")
    return filename

# Generate the past 7 days when we run the file
if __name__ == "__main__":
    for i in range(7):
        date = datetime.date.today() - timedelta(days=i+1)
        generate_reading(date)
