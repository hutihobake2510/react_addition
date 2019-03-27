import functools
import os
import pathlib
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("headless")
driver = webdriver.Chrome(options=chrome_options)

# driver = webdriver.Chrome()

def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()


class GameTests(unittest.TestCase):
    def solve_problem(self, correctly=True):
        problem = driver.find_element_by_id("problem")
        result = functools.reduce(lambda acc, n: acc + n, (int(n.strip()) for n in problem.text.split("+")))
        _input = driver.find_element_by_tag_name("input")
        _input.send_keys(result if correctly else not result)
        _input.send_keys(Keys.RETURN)
        return problem, result, _input

    def setUp(self):
        driver.get(file_uri("index.html"))

    def test_title(self):
        self.assertEqual(driver.title, "Hello")

    def test_input_cleared_after_correct(self):
        _input = self.solve_problem()[2]
        self.assertEqual(_input.get_attribute("value"), "")

    def test_red_after_incorrect(self):
        problem = self.solve_problem(correctly=False)[0]
        self.assertEqual(problem.value_of_css_property("color"), "rgba(255, 0, 0, 1)")


if __name__ == "__main__":
    unittest.main()
