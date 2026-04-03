from database import SessionLocal
from models import Package, create_tables

DEFAULT_PACKAGES = [
    {"package_name": "ريل 8", "package_type": "Reels", "default_price": 0, "description": "8 reels package"},
    {"package_name": "ريل 12", "package_type": "Reels", "default_price": 0, "description": "12 reels package"},
    {"package_name": "ريل 15", "package_type": "Reels", "default_price": 0, "description": "15 reels package"},
    {"package_name": "بوستات 8", "package_type": "Posts", "default_price": 0, "description": "8 posts package"},
    {"package_name": "بوستات 12", "package_type": "Posts", "default_price": 0, "description": "12 posts package"},
    {"package_name": "تفصيل مكس", "package_type": "Mixed", "default_price": 0, "description": "Custom mixed package"},
]


def seed_packages():
    create_tables()
    session = SessionLocal()
    try:
        for pkg in DEFAULT_PACKAGES:
            exists = session.query(Package).filter(Package.package_name == pkg["package_name"]).first()
            if not exists:
                session.add(Package(**pkg))
        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    seed_packages()
    print("Default packages seeded successfully.")
