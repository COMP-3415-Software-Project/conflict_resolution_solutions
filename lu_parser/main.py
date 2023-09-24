import json


def parseJSON():
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
    parseJSON()

hell no, same reason I dont use Arch, I dont want to have to build my ide from scratch
