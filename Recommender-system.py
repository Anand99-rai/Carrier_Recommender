import os
from googleapiclient.discovery import build

# Define possible career categories and their associated courses with detailed info
career_options = {
    "Science": {
        "Engineering": {
            "Computer Science": "Focus on programming, algorithms, and software development. Career paths: Software Developer, Systems Architect.",
            "Mechanical Engineering": "Design and build mechanical systems. Career paths: Mechanical Engineer, Automotive Engineer.",
            "Electrical Engineering": "Work with electrical systems and equipment. Career paths: Electrical Engineer, Electronics Technician.",
            "Chemical Engineering": "Design processes for large-scale chemical manufacturing. Career paths: Chemical Engineer, Process Engineer."
        },
        "Medical": {
            "MBBS": "Study medicine to become a doctor. Career paths: General Practitioner, Surgeon, Specialist.",
            "Nursing": "Focus on healthcare and patient care. Career paths: Registered Nurse, Nurse Practitioner, Healthcare Administrator.",
            "Dentistry": "Study dental health and treatments. Career paths: Dentist, Orthodontist, Dental Hygienist.",
            "Pharmacy": "Study pharmaceutical sciences. Career paths: Pharmacist, Pharmaceutical Researcher."
        },
        "Pure Sciences": {
            "Physics": "Study the fundamental forces of nature. Career paths: Physicist, Researcher, Academic.",
            "Chemistry": "Study substances and their interactions. Career paths: Chemist, Biochemist, Industrial Chemist.",
            "Biology": "Study living organisms and ecosystems. Career paths: Biologist, Environmental Scientist.",
            "Mathematics": "Study abstract patterns and structures. Career paths: Mathematician, Data Scientist, Cryptographer."
        }
    },
    "Commerce": {
        "Business": {
            "BBA": "Study business fundamentals and management. Career paths: Business Analyst, Manager, Entrepreneur.",
            "MBA": "Advanced business management skills. Career paths: CEO, Marketing Director, Finance Director.",
            "Finance": "Focus on financial management and investments. Career paths: Investment Banker, Financial Analyst.",
            "Marketing": "Study market research and strategies. Career paths: Marketing Manager, Brand Manager."
        },
        "Accountancy": {
            "B.Com": "Study accounting and finance. Career paths: Accountant, Auditor.",
            "CA": "Chartered Accountancy, with a focus on auditing, taxation, and finance. Career paths: Chartered Accountant.",
            "CS": "Company Secretary. Career paths: Corporate Governance, Legal Compliance.",
            "ICWA": "Cost accounting and financial management. Career paths: Cost Accountant, Financial Planner."
        },
        "Economics": {
            "B.A. Economics": "Study economic theory, policy, and analysis. Career paths: Economist, Policy Analyst.",
            "B.Sc. Economics": "Focus on quantitative methods and data analysis. Career paths: Data Analyst, Researcher."
        }
    },
    "Arts": {
        "Humanities": {
            "History": "Study past events and their impact. Career paths: Historian, Archaeologist.",
            "Psychology": "Study the mind and behavior. Career paths: Psychologist, Therapist.",
            "Sociology": "Study social behavior and institutions. Career paths: Sociologist, Social Worker.",
            "Philosophy": "Study fundamental questions about existence, knowledge, and ethics. Career paths: Philosopher, Ethics Consultant."
        },
        "Creative Arts": {
            "Fine Arts": "Create visual art and design. Career paths: Artist, Art Curator.",
            "Music": "Study music theory and performance. Career paths: Musician, Composer.",
            "Theater": "Study drama and performance. Career paths: Actor, Director.",
            "Dance": "Study various forms of dance. Career paths: Dancer, Choreographer."
        },
        "Languages": {
            "English Literature": "Study English language and literature. Career paths: Writer, Editor.",
            "Foreign Languages": "Study languages like Spanish, French, etc. Career paths: Translator, Linguist.",
            "Linguistics": "Study the structure of language. Career paths: Linguist, Language Specialist."
        }
    },
    "Vocational": {
        "Design": {
            "Fashion Designing": "Study fashion trends and design garments. Career paths: Fashion Designer, Textile Designer.",
            "Interior Designing": "Design the interiors of buildings and homes. Career paths: Interior Designer, Home Decor Specialist.",
            "Graphic Designing": "Design visual content using software. Career paths: Graphic Designer, Art Director."
        },
        "Technology": {
            "Web Development": "Create and maintain websites. Career paths: Web Developer, Front-end Developer.",
            "Data Science": "Study data analysis, statistics, and machine learning. Career paths: Data Scientist, Machine Learning Engineer.",
            "Cyber Security": "Protect systems from cyber attacks. Career paths: Cybersecurity Analyst, Information Security Consultant."
        },
        "Healthcare": {
            "Medical Laboratory Technology": "Work in labs to analyze medical samples. Career paths: Lab Technician, Pathologist.",
            "Radiology Technician": "Operate imaging equipment to assist in diagnosis. Career paths: Radiologic Technologist, MRI Technician."
        }
    }
}

# Google API setup
API_KEY = 'Your API_KEY'  # Replace with your API Key
CSE_ID = 'YOUR CSE_ID'  # Replace with your Custom Search Engine ID

def google_search(query, num_results=5):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=query, cx=CSE_ID, num=num_results).execute()
    
    search_results = []
    for item in res.get("items", []):
        title = item.get("title")
        link = item.get("link")
        snippet = item.get("snippet")
        search_results.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n")
    
    return search_results

def recommend_courses(marks_10th, marks_12th, area_of_interest):
    # Filter based on marks: Let's assume marks will give a score for difficulty of courses
    if marks_10th < 50 or marks_12th < 50:
        difficulty_level = 'easy'
    elif marks_10th < 70 or marks_12th < 70:
        difficulty_level = 'moderate'
    else:
        difficulty_level = 'hard'

    # Suggest courses based on area of interest
    if area_of_interest not in career_options:
        return "Invalid area of interest. Please choose from: Science, Commerce, Arts, or Vocational.", None

    recommended_courses = []
    category = None
    for category, courses in career_options[area_of_interest].items():
        if difficulty_level == 'easy' and category == 'Vocational':
            recommended_courses.extend(courses)
        elif difficulty_level == 'moderate' and category != 'Vocational':
            recommended_courses.extend(courses)
        elif difficulty_level == 'hard' and category in ['Engineering', 'Medical', 'Accountancy', 'Economics']:
            recommended_courses.extend(courses)

    if not recommended_courses:
        return "No courses available based on your criteria.", None

    return recommended_courses, category  # Return both the list of courses and the category for exploration

def explore_course(courses, category, area_of_interest):
    print("\nSelect a course to explore further (Enter the course name):")
    for i, course in enumerate(courses, start=1):
        print(f"{i}. {course}")

    selected_course = int(input("\nEnter the number of the course you want to explore: "))
    if 1 <= selected_course <= len(courses):
        course_name = courses[selected_course - 1]
        course_details = career_options[area_of_interest][category].get(course_name, "No details available.")
        print(f"\nDetails for {course_name}: {course_details}")
        
        # Fetching online resources for the selected course
        print("\nFetching relevant online content about the course...")
        search_results = google_search(course_name + " course details education")
        if search_results:
            print("\nFound the following resources:")
            for result in search_results:
                print(result)
        else:
            print("\nNo online resources found for this course.")
    else:
        print("Invalid selection!")

# Example usage
marks_10th = int(input("Enter your 10th grade marks: "))
marks_12th = int(input("Enter your 12th grade marks: "))
area_of_interest = input("Enter your area of interest (Science, Commerce, Arts, Vocational): ").capitalize()

recommended_courses, category = recommend_courses(marks_10th, marks_12th, area_of_interest)
if isinstance(recommended_courses, list):
    print(f"\nBased on your marks and interest in {area_of_interest}, we suggest the following courses: \n")
    for course in recommended_courses:
        print(course)
    if category:
        explore_course(recommended_courses, category, area_of_interest)
else:
    print(recommended_courses)
