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
        "title": "UC Berkeley embARC Summer Design Academy",
        "category": "Summer Program",
        "grades": [10, 11, 12],
        "deadline": "March",
        "amountOrCost": "Scholarships Available",
        "description": "4-week UC Berkeley College of Environmental Design intensive in architecture, urban design, and sustainable city planning for high school students.",
        "link": "https://ced.berkeley.edu/academics/summer-programs/embarc"
    },
    {
        "title": "Berkeley Lab (LBNL) High School STEM Internships & Experiences",
        "category": "Research",
        "grades": [10, 11, 12],
        "deadline": "Spring",
        "amountOrCost": "Free / Paid Stipends",
        "description": "Research experiences and internships at Lawrence Berkeley National Laboratory (managed by UC) introducing high schoolers to physics, computing, and energy sciences.",
        "link": "https://k12education.lbl.gov/programs/high-school"
    },
    {
        "title": "Berkeley Lab QCaMP (Quantum Computing, Math & Physics Camp)",
        "category": "Summer Program",
        "grades": [9, 10, 11, 12],
        "deadline": "Spring",
        "amountOrCost": "Free / Stipend Available",
        "description": "Hands-on summer camp introducing high school students to quantum computing fundamentals, coding, and lab tours with UC Berkeley and Lawrence Berkeley National Lab scientists.",
        "link": "https://qcamp.lbl.gov/"
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
        "title": "UCLA Summer College Immersion Program Plus (SCIP+)",
        "category": "Research",
        "grades": [10, 11],
        "deadline": "May 1 (Domestic) / April 1 (International)",
        "amountOrCost": "Need-Based Scholarships Available",
        "description": "6-week UCLA summer research methodology track pairing undergraduate coursework with 1-on-1 research advising, lab guest speakers, and UC college credit (3.8+ unweighted GPA).",
        "link": "https://summer.ucla.edu/summer-programs/summer-college-immersion-program/scip-2/"
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
        "title": "UCLA Writing Project Summer Youth Camp",
        "category": "Summer Program",
        "grades": [9, 10, 11, 12],
        "deadline": "Spring",
        "amountOrCost": "~\$650 / Aid Available",
        "description": "Summer writing intensive hosted through UCLA helping rising 9th-12th graders develop academic and creative writing skills while exploring relevant social issues.",
        "link": "https://centerx.gseis.ucla.edu/writing-project/"
    },
    {
        "title": "UCLA Summer Precollege Focus Series",
        "category": "Summer Program",
        "grades": [9, 10, 11, 12],
        "deadline": "May",
        "amountOrCost": "Financial Aid Available",
        "description": "Specialized 1- to 3-week UCLA summer institutes covering film, architecture, engineering, data science, and public health for high school students (3.2+ GPA).",
        "link": "https://summer.ucla.edu/"
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
        "title": "UC San Diego (UCSD) Futures Program",
        "category": "Summer Program",
        "grades": [9, 10, 11, 12],
        "deadline": "Rolling / Spring",
      "title": "UC San Diego (UCSD) Global Environmental Leadership & Sustainability",
        "category": "Summer Program",
        "grades": [9, 10, 11, 12],
        "deadline": "Spring",
        "amountOrCost": "Scholarships Available",
        "description": "Field-based sustainability and climate leadership programs hosted with UCSD researchers focusing on environmental policy and conservation.",
        "link": "https://academicconnections.ucsd.edu/"
    },
