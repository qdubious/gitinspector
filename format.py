# coding: utf-8
#
# Copyright © 2012 Ejwa Software. All rights reserved.
#
# This file is part of gitinspector.
#
# gitinspector is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gitinspector is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gitinspector. If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
import base64
import basedir
import os
import terminal
import version
import zipfile

__available_formats__ = ["html", "text", "xml"]
__default_format__ = __available_formats__[1]
__selected_format__ = __default_format__

class InvalidFormatError(Exception):
	pass

def select(format):
	global __selected_format__
	__selected_format__ = format

	return format in __available_formats__

def is_interactive_format():
	return __selected_format__ == "text"

def __output_html_template__(name):
	template_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), name)
	file_r = open(template_path, "rb")
	return file_r.read().decode("utf-8", "replace")

def __get_zip_file_content__(name):
	zip_file = zipfile.ZipFile(basedir.get_basedir() + "/html/flot.zip", "r")
	content = zip_file.read(name)
	zip_file.close()
	return content

def output_header():
	if __selected_format__ == "html":
		base = basedir.get_basedir()
		html_header = __output_html_template__(base + "/html/html.header")
		jquery_js = __get_zip_file_content__("jquery.js")
		flot_js = __get_zip_file_content__("jquery.flot.js")

		logo_file = open(base + "/html/gitinspector_piclet.png", "rb")
		logo = logo_file.read()
		logo_file.close()
		logo = base64.b64encode(logo)

		print(html_header.format(version.__version__, jquery_js, flot_js, logo))
	elif __selected_format__ == "xml":
		print("<gitinspector>")

def output_footer():
	if __selected_format__ == "html":
		html_footer = __output_html_template__("html/html.footer")
		print(html_footer)
	elif __selected_format__ == "xml":
		print("</gitinspector>")
 
def call_output_function(html_function, text_function, xml_function, *parameters):
	if __selected_format__ == "html":
		html_function(*parameters)
	elif __selected_format__ == "text":
		text_function(*parameters)
	else:
		xml_function(*parameters)
