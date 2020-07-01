#!/usr/bin/env python

import asyncio
import logging
import os
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


class TCXHandler(object):

    ns = {'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}

    def __init__(self, filepath, speed=10):
        self.filepath = filepath
        self.speed = speed # m/s
        self.tree = None
        self.root = None
        self.namespace= None
        self.course = None
        self.course_name = None
        self.course_distance = None
        self.course_distance_per_trackpoint = None
        self.course_trackpoints = []
        self.course_pos_index = 0
        self.callback = None
        self.__initialization()

    def __load_file(self):
        self.tree = ET.parse(self.filepath)

    def __load_root(self):
        self.root = self.tree.getroot()

    def __load_course_data(self):
        courses = self.root.findall(".//ns:Course", namespaces=self.ns)
        if len(courses) != 1:
            logger.error("The handler is only enable to process a single course")
            return
        self.course = courses[0]
        course_names = self.course.findall("ns:Name", namespaces=self.ns)
        if len(course_names) != 1:
            logger.error("More than one (or no) course name detected")
            return
        self.course_name = course_names[0].text
        course_laps = self.course.findall("ns:Lap", namespaces=self.ns)
        if len(course_laps) != 1:
            logger.error("More than one (or no) course lap detected")
            return
        course_lap = course_laps[0]
        self.course_distance = int(course_lap.find("ns:DistanceMeters", namespaces=self.ns).text)

        logger.debug("Course data: '{}' ({} meters)".format(self.course_name, self.course_distance))

    def __lat_and_long(self, element):
        position = element.find("ns:Position", namespaces=self.ns)
        lat = position.find("ns:LatitudeDegrees", namespaces=self.ns).text
        long = position.find("ns:LongitudeDegrees", namespaces=self.ns).text
        result = { "latitude": lat, "longitude": long}
        return result

    def __load_trackpoints(self):
        course_tracks = self.course.findall("ns:Track", namespaces=self.ns)
        if len(course_tracks) != 1:
            logger.error("More than one (or no) course track detected")
            return
        course_track = course_tracks[0]
        trackpoints = course_track.findall("ns:Trackpoint", namespaces=self.ns)
        self.course_trackpoints = list(map(self.__lat_and_long, trackpoints))
        self.course_distance_per_trackpoint = self.course_distance / len(self.course_trackpoints)

    def __initialization(self):
        self.__load_file()
        self.__load_root()
        self.__load_course_data()
        self.__load_trackpoints()

    def register_callback(self, callback):
        self.callback = callback

    def remove_callback(self):
        self.callback = None

    async def start(self):
        course_trackpoints_num = len(self.course_trackpoints)
        course_trackpoints_max_index = course_trackpoints_num-1
        while(True):
            position = self.course_trackpoints[self.course_pos_index]
            if self.callback:
                await self.callback(position)
            self.course_pos_index = self.course_pos_index + 1 if self.course_pos_index < course_trackpoints_max_index else 0
            sleep_time = self.course_distance_per_trackpoint / self.speed
            await asyncio.sleep(sleep_time)