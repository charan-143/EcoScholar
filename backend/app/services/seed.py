from sqlalchemy.orm import Session
from app.models.course import Course

COURSES = [
 {"slug":"climate-basics","title":"Climate Science, Clearly Explained","category":"Climate","level":"Beginner","duration":"35 min","description":"Understand the greenhouse effect, climate evidence, mitigation and adaptation.","content":"Climate is the long-term pattern of weather. Greenhouse gases absorb and re-emit infrared radiation, warming the lower atmosphere. Mitigation addresses causes; adaptation addresses consequences."},
 {"slug":"clean-energy","title":"The Clean Energy Transition","category":"Energy","level":"Intermediate","duration":"45 min","description":"Explore renewable power, grids, storage and lifecycle trade-offs.","content":"Solar and wind are variable resources. Reliable low-carbon systems combine generation, transmission, demand flexibility, storage and other firm resources."},
 {"slug":"biodiversity","title":"Biodiversity and Living Systems","category":"Nature","level":"Beginner","duration":"30 min","description":"Learn why ecosystems matter and how conservation works.","content":"Biodiversity spans genetic, species and ecosystem diversity. Habitat loss and fragmentation are important pressures. Conservation includes protection, restoration and sustainable use."},
 {"slug":"circular-economy","title":"Designing Out Waste","category":"Circularity","level":"Intermediate","duration":"40 min","description":"Apply the waste hierarchy and circular design principles.","content":"Prevention and reuse generally preserve more value than recycling. Circular design considers durability, repairability, reuse systems and material recovery."},
]

def seed_courses(db: Session):
    for item in COURSES:
        if not db.query(Course).filter_by(slug=item["slug"]).first():
            db.add(Course(**item))
    db.commit()
