const OPPORTUNITIES = [
  {
    id: 1,
    title: "Coolidge Scholarship",
    category: "Scholarship",
    grades: [11],
    award: "Full-ride (4 years of undergraduate study)",
    focus: "Academic merit, public policy, and civic leadership",
    deadlineWindow: "Typically January",
    description: "An independently endowed, non-partisan scholarship for high school juniors who plan to enroll in college the following fall.",
    url: "https://coolidgescholars.org/"
  },
  {
    id: 2,
    title: "Horatio Alger National & State Scholarships",
    category: "Scholarship",
    grades: [11],
    award: "$10,000 to $25,000",
    focus: "Financial need, perseverance, and overcoming adversity",
    deadlineWindow: "Typically spring of junior year",
    description: "Supports high school juniors facing financial hardship who demonstrate integrity, grit, and a commitment to completing higher education.",
    url: "https://scholars.horatioalger.org/"
  },
  {
    id: 3,
    title: "Davidson Fellows Scholarship",
    category: "Scholarship",
    grades: [9, 10, 11, 12],
    award: "$10,000, $25,000, or $50,000",
    focus: "Significant student projects in STEM, Literature, Music, Philosophy, or Outside the Box",
    deadlineWindow: "Typically February",
    description: "Recognizes students under 18 who have produced an original, graduate-level-caliber piece of work.",
    url: "https://www.davidsongifted.org/gifted-programs/fellows-scholarship/"
  },
  {
    id: 4,
    title: "VFW Voice of Democracy",
    category: "Scholarship",
    grades: [9, 10, 11, 12],
    award: "Up to $35,000 national top award",
    focus: "Recorded audio-essay competition on an annual theme",
    deadlineWindow: "Typically October 31",
    description: "High school students record and submit a short audio essay expressing their perspective on a yearly civic theme.",
    url: "https://www.vfw.org/community/youth-and-education/youth-scholarships"
  },
  {
    id: 5,
    title: "Cameron Impact Scholarship",
    category: "Scholarship",
    grades: [11],
    award: "Full-tuition merit scholarship",
    focus: "Leadership, community service, academics, and extracurricular impact",
    deadlineWindow: "Early application opens spring of junior year",
    description: "Four-year merit scholarship rewarding students who actively lead initiatives and help others in their school or community.",
    url: "https://www.bryancameroneducationfoundation.org/"
  },
  {
    id: 6,
    title: "Coca-Cola Scholars Program",
    category: "Scholarship",
    grades: [12],
    award: "$20,000 college scholarship",
    focus: "Leadership, service, and academic achievement",
    deadlineWindow: "Opens in August before senior year; closes October",
    description: "Achievement-based scholarship awarded to graduating seniors who drive positive change in their schools and communities.",
    url: "https://www.coca-colascholarsfoundation.org/"
  },
  {
    id: 7,
    title: "Bank of America Student Leaders",
    category: "Summer Program",
    grades: [11, 12],
    award: "Paid 8-week internship + D.C. leadership summit",
    focus: "Nonprofit community service and civic leadership",
    deadlineWindow: "Typically January",
    description: "Connects juniors and seniors with paid summer internships at local nonprofits alongside a week-long leadership summit in Washington, D.C.",
    url: "https://about.bankofamerica.com/en/making-an-impact/student-leaders"
  },
  {
    id: 8,
    title: "MITES Summer",
    category: "Summer Program",
    grades: [11],
    award: "Free 6-week residential STEM program at MIT",
    focus: "Engineering, science, mathematics, and collaborative projects",
    deadlineWindow: "Typically January / early February",
    description: "Free, immersive summer program at MIT for high school juniors interested in science, engineering, and quantitative problem-solving.",
    url: "https://mites.mit.edu/"
  },
  {
    id: 9,
    title: "Telluride Association Summer Seminar (TASS)",
    category: "Summer Program",
    grades: [10, 11],
    award: "Free residential summer seminar (all expenses covered)",
    focus: "Humanities, critical inquiry, and democratic community",
    deadlineWindow: "Typically December",
    description: "Free summer seminar bringing high school sophomores and juniors together for college-level discussion and seminar-style learning.",
    url: "https://www.tellurideassociation.org/"
  },
  {
    id: 10,
    title: "American Legion Boys State / Girls State",
    category: "Summer Program",
    grades: [11],
    award: "State-sponsored leadership & government program",
    focus: "Civics, public speaking, policy, and leadership simulation",
    deadlineWindow: "Varies by state chapter (winter/spring)",
    description: "Hands-on program where rising seniors learn how local, county, and state government operate through interactive leadership roles.",
    url: "https://www.legion.org/boysnation"
  },
  {
    id: 11,
    title: "Yale Young Global Scholars (YYGS)",
    category: "Summer Program",
    grades: [10, 11],
    award: "2-week academic program (need-based aid available)",
    focus: "Interdisciplinary seminars in STEM, humanities, policy, and global affairs",
    deadlineWindow: "Typically early January",
    description: "Enrichment program at Yale University where students explore specialized academic tracks with peers from around the world.",
    url: "https://globalscholars.yale.edu/"
  },
  {
    id: 12,
    title: "Research Science Institute (RSI)",
    category: "Research",
    grades: [11],
    award: "Free 6-week summer research program at MIT",
    focus: "Full research cycle in science, technology, engineering, and mathematics",
    deadlineWindow: "Typically December (domestic) / January (international)",
    description: "Combines on-campus STEM coursework with mentored research where students conduct original investigations and present findings.",
    url: "https://www.cee.org/programs/research-science-institute"
  },
  {
    id: 13,
    title: "Stanford Institutes of Medicine Summer Research (SIMR)",
    category: "Research",
    grades: [11, 12],
    award: "8-week biomedical research internship (stipends available)",
    focus: "Biology, medicine, bioinformatics, and lab research",
    deadlineWindow: "Typically February",
    description: "High school juniors and seniors (age 16+) work alongside Stanford researchers on mentored projects in medicine and biological sciences.",
    url: "https://simr.stanford.edu/"
  },
  {
    id: 14,
    title: "NASA High School Internship Program (OSTEM)",
    category: "Research",
    grades: [10, 11, 12],
    award: "Paid internship / research experience",
    focus: "Space exploration, engineering, earth science, and STEM research",
    deadlineWindow: "Seasonal cycles (Fall, Spring, Summer)",
    description: "Offers students (age 16+) hands-on research and technical internships supporting NASA missions and science teams.",
    url: "https://stem.nasa.gov/ostem/"
  },
  {
    id: 15,
    title: "Science & Engineering Apprenticeship Program (SEAP)",
    category: "Research",
    grades: [10, 11, 12],
    award: "Paid 8-week summer research placement",
    focus: "Department of the Navy laboratory research and engineering",
    deadlineWindow: "Typically fall / early winter",
    description: "Places eligible high school students (age 16+) in Navy research laboratories to work with scientists and engineers.",
    url: "https://www.seap.nasa.gov/"
  },
  {
    id: 16,
    title: "Regeneron Science Talent Search",
    category: "Research",
    grades: [12],
    award: "Awards up to $250,000",
    focus: "Independent original scientific or mathematical research",
    deadlineWindow: "Typically November of senior year",
    description: "Nation’s oldest and most prestigious high school science and math research competition based on original student research.",
    url: "https://www.societyforscience.org/regeneron-sts/"
  }
];
