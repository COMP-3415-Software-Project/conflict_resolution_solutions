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

    with open("parsed_response.json", "w") as parsed_file:
        parsed_file.write(json.dumps(parsed_json, indent=4))

    parsed_file.close()
    raw_file.close()


def parseProgramRequirementsJSON(programFilePath):
    # Dictionary that will hold our parsed json datat
    parsed_json = dict()

    # Load our Display names for rooms
    raw_file = open(programFilePath)
    raw_file_json = json.load(raw_file)

    program = raw_file_json.get("Program")
    parsed_requirement_list = []

    parsed_requirement_list = [c["Id"]
                               for R in program.get("Requirements")
                               for S in R.get("Subrequirements")
                               for G in S.get("Groups")
                               for c in (G.get("Courses")
                                         if len(G.get("Courses")) != 0 else G.get("FromCourses"))
                               ]

    parsed_json.update(
        {
            "Code": raw_file_json.get("Code"),
            "Title": raw_file_json.get("Title"),
            "Description": raw_file_json.get("Description"),
            "Minors": raw_file_json.get("Minors"),
            "Specializations": raw_file_json.get("Specializations"),
            "Requirements": parsed_requirement_list
        }
    )

    with open("parsed_response.json", "w") as parsed_file:
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
    # parseCourseListJSON()
