import asyncio
import json

import aiohttp as aiohttp
from aiohttp import FormData


def parseCourseListJSON():
    # Dictionary that will hold our parsed json datat
    parsed_json = dict()

    # Load our Display names for rooms
    raw_file = open('lakehead_formated_catalogdump.json')
    raw_file_json = json.load(raw_file)

    page_list = raw_file_json.get("Pages")
    parsed_course_list = []

    for page in page_list:
        course_list = page.get("CourseFullModels")

        while bool(course_list):
            parsed_course_list.append(parseCourse(course_list.pop(0)))

    parsed_json.update(
        {
            "Courses": parsed_course_list
        }
    )

    with open("parsed_course_list.json", "w") as parsed_file:
        parsed_file.write(json.dumps(parsed_json, indent=4))

    parsed_file.close()
    raw_file.close()


# # This just takes the course codes and will ignore the program requirements that dont require specific courses (
# such as 2.5 FCE electives or 0.5 FCE in BIO)
def parseProgramRequirementsJSON(programFilePath):
    parsed_json = dict()

    raw_file = open(programFilePath)
    raw_file_json = json.load(raw_file)

    program = raw_file_json.get("Program")
    parsed_requirement_list = []
    elective_list = []

    for R in program.get("Requirements"):
        for S in R.get("Subrequirements"):
            for G in S.get("Groups"):
                if len(G.get("Courses")) != 0:
                    for c in G.get("Courses"):
                        parsed_requirement_list.append(c.get("Id"))
                elif len(G.get("FromCourses")) != 0:
                    for c in G.get("FromCourses"):
                        parsed_requirement_list.append(c.get("Id"))
                elif 'ELECTIVE' in G.get("RequirementCode"):
                    elective_list.append(G.get("RequirementCode").split(".", 1)[1])

    parsed_json.update(
        {
            "Code": program.get("Code"),
            "Title": program.get("Title"),
            "Description": program.get("Description"),
            "Minors": program.get("Minors"),
            "Specializations": program.get("Specializations"),
            "Requirements": parsed_requirement_list,
            "Elective": elective_list
        }
    )

    with open("parsed_program_list.json", "w") as parsed_file:
        parsed_file.write(json.dumps(parsed_json, indent=4))

    parsed_file.close()
    raw_file.close()

    # parse their data set by just taking the values we want. It's easier than deleting the rest. maybe we can just load
    # in specific keys with JSON though
    def parseCourse(course):
        parsed_course = dict()

        parsed_course.update({
            "Id": course.get("Id"),
            "SubjectCode": course.get("SubjectCode"),
            "CourseCode": course.get("CourseTitleDisplay"),
            "Title": course.get("Title"),
            "Description": course.get("Description"),
            "CourseRequisites": course.get("CourseRequisites"),
            "Requisites": course.get("Requisites")
        })
        return parsed_course


if __name__ == '__main__':
    parseProgramRequirementsJSON("bio3year.json")
