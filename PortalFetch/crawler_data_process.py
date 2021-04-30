#!/usr/bin/env python
"""Process html course information to save in a .json file.

It requires file 'user.ini' to load the user's own user name and password.
"""
from bs4 import BeautifulSoup
import json
import time
import os


class DataProcess:
    """Deputy .html file to .json file.

    It needs to import an .html file from De Anza courses information website.
    """

    def __getRustContents(self, html):
        """
        Get rust list contents from html.

        Input: html is html of the courses
        Output : courseList will include all the courses list in text and some other contents
        Parameters: String
        Returns: List
        """
        rustCourseList = []
        soup = BeautifulSoup(html, 'lxml')
        trs = soup.find_all('tr')
        for tr in trs:
            rowData = []
            for td in tr:
                if td == '\n':
                    continue
                elif td.string:
                    rowData.append(str(td.string))
                else:
                    rowData.append(td)
            if len(rowData) == 19:
                rustCourseList.append(rowData[:18])
        return rustCourseList

    def __getList(self, courseList, html):
        """
        Get course list from html.

        Input: html is html of the courses, courseList is an empty list []
        Output : courseList will include all the courses list in text
        Parameters: List, String
        Returns: None
        """
        rustCourseList = self.__getRustContents(html)
        for course in rustCourseList:
            courseData = []
            for ele in course:
                if type(ele) is not str:
                    soup = BeautifulSoup(str(ele), 'lxml')
                    ele = soup.get_text()
                courseData.append((ele))
            courseList.append(courseData)

    def __deputyList(self, courseList):
        """
        Deputy courseList to a json file.

        Input: courseList is courses list from __getContents
        Output : .json objects will include all the courses information
        Parameters: List
        Returns: a json object(key: subject, value: an array of courses of this subject)
        """
        coursesData = {}
        title = ['Select', 'CRN', 'Coreq', 'Subj', 'Crse', 'Sec', 'Cmp', 'Cred', 'Title', 'Days', 'Time', 'Act', 'Rem',
                'WL Rem', 'Instructor', 'Date (MM/DD)', 'Location', 'Attribute', 'lab']
        for CourseIndex in range(len(courseList)):
            # Create a new subject
            if courseList[CourseIndex][0] == 'Select':
                subjectName = courseList[CourseIndex + 1][3]
                coursesData[subjectName] = []
            else:
                # deputy one line of course information
                if courseList[CourseIndex][0] != '\xa0': #this line is a course
                    course = {}
                    self.__deputyCourseLine(title, courseList[CourseIndex], course)
                    coursesData[courseList[CourseIndex][3]].append(course)
                # deputy lab information
                else: # this line is a lab
                    lab = {}
                    # find the subject
                    labSubjectIndex = CourseIndex - 1
                    while courseList[labSubjectIndex][3] == '\xa0':
                        labSubjectIndex -= 1
                    subjectName = courseList[labSubjectIndex][3]
                    self.__deputyLabLine(title, courseList[CourseIndex], lab)
                    coursesData[subjectName][-1]['lab'].append(lab)
        return coursesData

    def __deputyCourseLine(self, title, oneLine, emptyDiction):
        """
        Deputy one line of courseList to the diction.

        Input: title is a list of courses' key words, oneLine is a line of course information, emptyDiction is {}
        Parameters: List, List, Dictionary
        Returns: None
        """
        titleIndex = -1
        for ele in oneLine:
            titleIndex += 1
            if titleIndex != 2 and titleIndex != 3:
                emptyDiction[title[titleIndex]] = ele if ele != '\xa0' else ''
        emptyDiction['lab'] = []

    def __deputyLabLine(self, title, labLine, emptyDiction):
        """
        Deputy one line of lab information to the diction.

        Input: title is a list of courses' key words, labLine is a line of lab information, emptyDiction is {}
        Parameters: List, List, Dictionary
        Returns: None
        """
        titleIndex = -1
        for ele in labLine:
            titleIndex += 1
            if ele != '\xa0':
                emptyDiction[title[titleIndex]] = ele

    def htmlToJson(self, htmlFile, jsonFilename, quarter, fetchTime):
        """
        Deputy htmlFile to a json file.

        Input:  htmlFile is a .html file got from __deputyList,
                jsonFilename is .json file name you want to give for the output
                quarter is the name of the course quarter.
                fetchTime is the fetch time of crawler
        Output : .json file  will include all the courses information
        Parameters: string, string, string, string
        Returns: None
        """
        courseDataList = []
        self.__getList(courseDataList, htmlFile)
        CourseDataJson = self.__deputyList(courseDataList)
        output = {}
        output[quarter] = {}
        output[quarter]["FetchTime"] = fetchTime
        output[quarter]["CourseData"] = CourseDataJson
        if not os.path.exists('../output'):
            try:
                os.makedirs('../output')
            except OSError as e:
                logger.error("Unable to create output directory: %s", e)

        with open('../output/' + jsonFilename, 'w') as outfile:
            json.dump(output, outfile, indent=4)

    def data_process(self, html, filename, quarter):
        """
        Deputy HTML text to save in a .json file.

        input:  'html' is the HTML string.
                'filename' is the name of the saved .json.
                'quarter' is the quarter of the json file'
        output: save 'quarter' courses in a file 'filename'.json with current time stamp.
        Parameters: String, String, String
        Return: None
        """
        self.htmlToJson(html, filename, quarter, int(time.time()))

