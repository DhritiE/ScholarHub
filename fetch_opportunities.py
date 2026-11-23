import json
import os
import time
import urllib.request

DATA_FILE = "scholarhub-opportunities.json"

UC_OPPORTUNITIES = [
    {
        "title": "UC COSMOS (California State Summer School for Mathematics and Science)",
        "category": "Summer Program",
        "grades": [9, 10, 11, 12],
        "deadline": "February",
        "amountOrCost": "Financial Aid Available",
        "description": "Intensive 4-week residential STEM summer program hosted at UC Davis, UC Irvine, UCLA, UC San Diego, and UC Santa Cruz. Students work directly with UC faculty and researchers in specialized STEM clusters.",
        "link": "https://cosmos-ucop.ucdavis.edu/"
    },
    {
        "title": "UCSB Research Mentorship Program (RMP)",
        "category": "Research",
        "grades": [10, 11],
        "deadline": "March",
        "amountOrCost": "Scholarships Available",
        "description": "Competitive 6-week summer program at UC Santa Barbara pairing high-achieving high school students with a mentor to conduct hands-on university-level research and earn UC credit.",
        "link": "https://www.summer.ucsb.edu/programs/research-mentorship-program/overview"
    },
    {
        "title": "UCSB Summer Research Academies (SRA)",
        "category": "Research",
        "grades": [9, 10, 11],
        "deadline": "March",
        "amountOrCost": "Scholarships Available",
        "description": "4-week UC Santa Barbara program introducing high school students to university research through project-based tracks in STEM, humanities, and social sciences.",
        "link": "https://www.summer.ucsb.edu/programs/summer-research-academies/overview"
    },
    {
        "title": "UC Berkeley Academic Talent Development Program (ATDP)",
        "category": "Summer Program",
        "grades": [9, 10, 11, 12],
        "deadline": "February / March",
        "amountOrCost": "Need-Based Aid Available",
        "description": "Challenging summer courses at UC Berkeley in computer science, biotechnology, engineering, creative writing, and advanced mathematics for motivated high school students.",
        "link": "https://atdp.berkeley.edu/"
    },
    {
        "title": "UC Berkeley Pre-College Scholars (Summer Residential & Commuter)",
        "category": "Summer Program",
        "grades": [10, 11, 12],
        "deadline": "March",
        "amountOrCost": "Tuition / Aid Varies",
        "description": "Earn official UC Berkeley college credit while living on campus or commuting during the summer session alongside undergraduate students.",
        "link": "https://precollege.berkeley.edu/"
    },
    {
        "title": "UC Berkeley Girls in Engineering (GiE) Summer Camp",
        "category": "Summer Program",
        "grades": [9, 10],
        "deadline": "Spring",
        "amountOrCost": "Low Cost / Scholarships",
        "description": "UC Berkeley College of Engineering program introducing students to coding, robotics, bioengineering, and hands-on lab visits with Berkeley faculty.",
        "link": "https://girlsinengineering.berkeley.edu/"
    },
    {
        "title": "UC Berkeley Haas Business Academy for Youth (B-BAY)",
        "category": "Summer Program",
        "grades": [9, 10, 11, 12],
        "deadline": "February",
        "amountOrCost": "Scholarships Available",
        "description": "2-week entrepreneurship and business leadership program taught by UC Berkeley Haas School of Business faculty, culminating in a team business plan pitch.",
        "link": "https://haas.berkeley.edu/business-academy/"
    },
    {
        "title": "UCLA Summer College Immersion Program (SCIP)",
        "category": "Summer Program",
        "grades": [10, 11],
        "deadline": "May",
        "amountOrCost": "Financial Aid Available",
        "description": "6-week summer program allowing exceptional high school students to take real UCLA undergraduate courses, attend college workshops, and earn UC credit.",
        "link": "https://summer.ucla.edu/program/summer-college-immersion-program-scip/"
    },
    {
        "title": "UCLA Sci|Art NanoLab Summer Institute",
        "category": "Research",
        "grades": [10, 11, 12],
        "deadline": "March",
        "amountOrCost": "Scholarships Available",
        "description": "2-week intensive at the California NanoSystems Institute (CNSI) at UCLA exploring nanoscience, biotechnology, and scientific visualization through lab experiments.",
        "link": "https://www.cnsi.ucla.edu/education/sciart/"
    },
    {
        "title": "UCLA Applications of Nanoscience Summer Institute",
        "category": "Research",
        "grades": [10, 11, 12],
        "deadline": "April",
        "amountOrCost": "Scholarships Available",
        "description": "2-week UCLA lab-intensive program where students learn the fundamentals of nanoscience research and pitch a technology commercialization project.",
        "link": "https://www.cnsi.ucla.edu/education/applications-of-nanoscience/"
    },
    {
        "title": "UCLA Computer Science Summer Institute",
        "category": "Summer Program",
        "grades": [9, 10, 11, 12],
        "deadline": "May",
        "amountOrCost": "Financial Aid Available",
        "description": "3-week coding and computer science intensive at UCLA featuring lab tours, programming workshops, and college credit.",
        "link": "https://summer.ucla.edu/program/computer-science-summer-institute-introductory-track/"
    },
    {
        "title": "UCSD Academic Connections",
        "category": "Summer Program",
        "grades": [9, 10, 11, 12],
        "deadline": "May",
        "amountOrCost": "Scholarships Available",
        "description": "3-week residential and online summer academic experience at UC San Diego immersing high schoolers in marine science, biomedical research, engineering, and social sciences.",
        "link": "https://academicconnections.ucsd.edu/"
    },
    {
        "title": "UCSD Research Experience for High School Students (REHS)",
        "category": "Research",
        "grades": [10, 11, 12],
        "deadline": "March",
        "amountOrCost": "Free / Low Fee",
        "description": "8-week volunteer research internship at the San Diego Supercomputer Center (UCSD) pairing students with computational scientists on real research projects.",
        "link": "https://education.sdsc.edu/studenttech/rehs/"
    },
    {
        "title": "UCSD Heithoff-Brody High School Scholars Program (Salk Institute)",
        "category": "Research",
        "grades": [11, 12],
        "deadline": "March",
        "amountOrCost": "Paid Internship",
        "description": "8-week paid summer biomedical research internship in La Jolla working alongside Salk Institute and UC San Diego researchers.",
        "link": "https://www.salk.edu/about/education-outreach/programs/heithoff-brody-high-school-summers-scholars/"
    },
    {
        "title": "UC Irvine (UCI) Summer Pre-College Programs",
        "category": "Summer Program",
        "grades": [9, 10, 11, 12],
        "deadline": "May",
        "amountOrCost": "Tuition / Aid Varies",
        "description": "Academic academies and undergraduate courses at UC Irvine in biomedical sciences, game design, computer science, and business.",
        "link": "https://summer.uci.edu/high-school-students/"
    },
    {
        "title": "UCI Cancer Research Institute Youth Science Fellowship Program (YSFP)",
        "category": "Research",
        "grades": [11, 12],
        "deadline": "March",
        "amountOrCost": "Free (Orange County)",
        "description": "6-week summer laboratory fellowship at UC Irvine for Orange County high school juniors and seniors conducting hands-on cancer biology research.",
        "link": "https://cri.uci.edu/education-outreach/youth-science-fellowship-program/"
    },
    {
        "title": "UCI Brain Camp",
        "category": "Summer Program",
        "grades": [9, 10, 11, 12],
        "deadline": "Spring",
        "amountOrCost": "Scholarships Available",
        "description": "2-week immersive neuroscience summer camp at UC Irvine's Center for the Neurobiology of Learning and Memory featuring lab dissections, brain imaging, and experiments.",
        "link": "https://braincamp.bio.uci.edu/"
    },
    {
        "title": "UC Davis Young Scholars Program (YSP)",
        "category": "Research",
        "grades": [10, 11],
        "deadline": "March",
        "amountOrCost": "Need-Based Fee Reductions",
        "description": "6-week residential research program at UC Davis introducing 40 high-achieving high schoolers to original research in biological, agricultural, and environmental sciences.",
        "link": "https://ysp.ucdavis.edu/"
    },
    {
        "title": "UC Santa Cruz Science Internship Program (SIP)",
        "category": "Research",
        "grades": [9, 10, 11, 12],
        "deadline": "March",
        "amountOrCost": "Full/Partial Scholarships",
        "description": "10-week summer research internship placing high school students in active UC Santa Cruz research groups across astrophysics, biology, computer science, and psychology.",
        "link": "https://sip.ucsc.edu/"
    },
    {
        "title": "UCSF High School Intern Program (HIP)",
        "category": "Research",
        "grades": [11],
        "deadline": "February",
        "amountOrCost": "Paid Stipend ($3,200-$4,500)",
        "description": "8-week paid biomedical and health sciences research internship at UC San Francisco for San Francisco high school juniors.",
        "link": "https://sep.ucsf.edu/hs_programs/high-school-intern-program/"
    },
    {
        "title": "UC Riverside (UCR) Summer Academy & High School Programs",
        "category": "Summer Program",
        "grades": [9, 10, 11, 12],
        "deadline": "May",
        "amountOrCost": "Varies",
        "description": "Summer academic enrichment, engineering workshops, and college credit courses hosted at UC Riverside.",
        "link": "https://summer.ucr.edu/high-school"
    },
    {
        "title": "UC Merced Summer Bridge & Youth STEM Programs",
        "category": "Summer Program",
        "grades": [9, 10, 11, 12],
        "deadline": "Spring",
        "amountOrCost": "Free / Low Cost",
        "description": "STEM workshops, engineering academies, and college readiness programs at UC Merced for California high school students.",
        "link": "https://admissions.ucmerced.edu/"
    },
    {
        "title": "UC Regents & Chancellor's Scholarships (Incoming UC Freshmen)",
        "category": "Scholarship",
        "grades": [12],
        "deadline": "November 30 (UC App)",
        "amountOrCost": "$2,500 - Full Need",
        "description": "The most prestigious merit scholarship awarded by UC campuses based on your UC admissions application.",
        "link": "https://admission.universityofcalifornia.edu/tuition-financial-aid/types-of-aid/scholarships/"
    },
    {
        "title": "UC Blue and Gold Opportunity Plan",
        "category": "Scholarship",
        "grades": [12],
        "deadline": "March 2 (FAFSA/CADAA)",
        "amountOrCost": "Full Systemwide Tuition",
        "description": "Covers 100% of systemwide UC tuition and fees for eligible California high school seniors whose families earn under $80,000 per year.",
        "link": "https://admission.universityofcalifornia.edu/tuition-financial-aid/types-of-aid/blue-and-gold-opportunity-plan.html"
    }
]

SEARCH_QUERIES = [
    ("high school students", "Scholarship"),
    ("high school summer", "Summer Program"),
    ("high school research", "Research"),
    ("high school internship", "Summer Program"),
    ("high school senior", "Scholarship"),
    ("high school fellowship", "Research"),
    ("secondary school", "Scholarship"),
    ("teen leadership", "Summer Program"),
    ("pre-college", "Summer Program"),
    ("college prep", "Scholarship"),
    ("youth stem", "Research"),
    ("youth science", "Research"),
    ("computer science youth", "Research"),
    ("robotics youth", "Summer Program"),
    ("engineering high school", "Research"),
    ("biomedical youth", "Research"),
    ("environmental youth", "Research"),
    ("cybersecurity youth", "Summer Program"),
    ("youth civic engagement", "Summer Program"),
    ("youth arts", "Summer Program"),
    ("youth entrepreneurship", "Summer Program"),
    ("youth mentorship", "Summer Program"),
    ("student scholarship", "Scholarship"),
    ("summer institute high school", "Summer Program"),
    ("summer academy youth", "Summer Program")
]

def load_existing():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def categorize_item(title, default_category):
    t = title.lower()
    if any(w in t for w in ["summer", "camp", "internship", "academy", "institute", "mentorship"]):
        return "Summer Program"
    if any(w in t for w in ["research", "science", "stem", "lab", "fellowship", "environmental", "biomedical", "engineering"]):
        return "Research"
    return default_category

def assign_grades(keyword, title):
    combined = f"{keyword} {title}".lower()
    if any(w in combined for w in ["senior", "college prep", "12th"]):
        return [11, 12]
    return [9, 10, 11, 12]

def format_award(item):
    ceiling = item.get("awardCeiling")
    if ceiling and str(ceiling).isdigit() and int(ceiling) > 0:
        return f"Up to ${int(ceiling):,}"
    return "Federal Grant / Program"

def fetch_grants_gov():
    url = "https://api.grants.gov/v1/api/search2"
    all_fetched = []

    for keyword, default_cat in SEARCH_QUERIES:
        payload = json.dumps({
            "keyword": keyword,
            "oppStatuses": "posted|forecasted",
            "rows": 250
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                raw_data = json.loads(response.read().decode("utf-8"))
        except Exception as e:
            print(f"Skipping '{keyword}' due to network error: {e}")
            continue

        hits = raw_data.get("data", {}).get("oppHits", [])
        print(f"Keyword '{keyword}': found {len(hits)} results.")

        for item in hits:
            title = item.get("title", "").strip()
            opp_id = item.get("id", "")
            if not title or not opp_id:
                continue

            agency = item.get("agency", "U.S. Federal Agency")
            desc = f"Sponsored by {agency}. Click below for full eligibility requirements and application instructions."

            all_fetched.append({
                "title": title,
                "category": categorize_item(title, default_cat),
                "grades": assign_grades(keyword, title),
                "deadline": item.get("closeDate") or "Rolling / Check Site",
                "amountOrCost": format_award(item),
                "description": desc,
                "link": f"https://www.grants.gov/search-results-detail/{opp_id}"
            })

        time.sleep(0.3)

    return all_fetched

def merge_and_deduplicate(existing, incoming):
    seen_titles = {item["title"].strip().lower() for item in existing if isinstance(item, dict) and "title" in item}
    max_id = max((item.get("id", 0) for item in existing if isinstance(item, dict)), default=0)

    added_count = 0
    for item in incoming:
        key = item["title"].strip().lower()
        if key not in seen_titles:
            max_id += 1
            item["id"] = max_id
            existing.append(item)
            seen_titles.add(key)
            added_count += 1

    print(f"Added {added_count} new unique opportunities. Total: {len(existing)}")
    return existing

if __name__ == "__main__":
    current_data = load_existing()
    combined_incoming = UC_OPPORTUNITIES + fetch_grants_gov()
    updated_data = merge_and_deduplicate(current_data, combined_incoming)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, indent=2)
