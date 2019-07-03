from urllib.robotparser import RobotFileParser
import url_util as uu
import re


#
# Provides functionality for adhering to a sites exclusing protocol
# in domain/robots.txt
#
class Exclusion(object):
    def __init__(self):
        self.robot_cache = {}
        self.rp = RobotFileParser()

    def test_url(self, url):
        robot_url = uu.domain_name(url) + '/robots.txt'
        self.rp.set_url(robot_url)
        self.rp.read()
        return self.rp.can_fetch('*', url)
