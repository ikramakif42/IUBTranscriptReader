import pdfplumber, re

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

def sortCourse(x):
    crsID, crsCred, crsGrade = x
    return delTGP(crsGrade, crsCred)
    
def delTGP(crsGrade, crsCred):
    return (4.0 - gradeToGPA[crsGrade]) * float(crsCred)

    


gradeToGPA = {
    "A" : 4.0, "A-": 3.7,
    "B+": 3.3, "B" : 3.0, "B-": 2.7,
    "C+": 2.3, "C" : 2.0, "C-": 1.7,
    "D+": 1.3, "D" : 1.0,
    "P" : 0.0, "R" : 0.0, "F" : 0.0, 
    "I" : 0.0, "W" : 0.0,
    "S" : 0.0, "U" : 0.0, "O" : 0.0,
    "Y" : 0.0, "Z" : 0.0, "E" : 0.0
}

# Add file path here
pdf_path = 'Transcript2110001.pdf'
pdf_text = extract_text_from_pdf(pdf_path)
lines = pdf_text.strip().split('\n')
course_pattern = re.compile(r'^[A-Za-z]{3}\d{3}.*')
course_info_lines = []
for line in lines:
    if course_pattern.match(line):
        line = re.sub(r'(\d{1,2}\.\d{2}\s+\d{1,2}\.\d{2}\s+\d{1,2}\.\d{2}\s+\d{1,2}\.\d{2}).*', r'\1', line)
        course_info_lines.append(line)

totalCreds, tgp = 0.0, 0.0
myCrs = list()
rep = dict()
for line in course_info_lines:
    course = line.strip().split()
    crsID = course[0]
    crsGPA = course[-1]
    crsCred = course[-2]
    crsGrade = course[-5]
    totalCreds += float(crsCred)
    tgp += float(crsGPA)

    if crsGPA != "0.00":
        myCrs.append((crsID, crsCred, crsGrade))
    else:
        rep[crsID] = rep[crsID]+1 if crsID in rep else 1

cgpa = tgp/totalCreds

print(f"Your total credits are {totalCreds}, TGPA is {tgp:.2f} and CGPA is {cgpa:.2f}")

recomm = list()
myCrs.sort(key=lambda x: sortCourse(x), reverse=True)
count = 0
target = int(input("How many recommendations do you want?: "))
for c in myCrs:
    if c[2] == "A":
        break
    recomm.append(c)
    count += 1
    if count == target:
        break

print(f"These are the top {target} recommendations to improve your CGPA:")
c = 1
rtgp = 0
rtgpa = tgp
flag = False
for i in recomm:
    print(f"{c}. If you retake {i[0]} and improve the last grade {i[2]} to an A,", end=" ")
    rtgp += (4.0 - gradeToGPA[i[2]]) * float(i[1])
    print(f"your CGPA will improve to {(tgp+rtgp)/totalCreds:.2f}{f' (Past repeat: '+str(rep[i[0]])+')' if i[0] in rep else ''}")
    if c == target:
        flag = True
        break
    c += 1
if not flag:
    print("Well, the rest are all As, nothing to improve :)")