import time
import math
from bb_extended_endplate_calc import ExtendedEndPlateCalculation


class ReportGenerator(ExtendedEndPlateCalculation):
	"""
	Generate Design Report for Seated Angle Connection
	"""
	def __init__(self,extnd_calc_object ):
		"""

		Args:
			extnd_calc_object:  method from bbExtendedEndPlateSplice
		"""
		super(ReportGenerator, self).__init__()
		self.beam_tw = extnd_calc_object.bolt_dia

	def save_html(self, report_summary, filename, folder):
		"""

		Args:
			report_summary:
			filename:
			folder:

		Returns:
			None

		"""
		myfile = open(filename, "w")
		myfile.write(t('! DOCTYPE html') + nl())
		myfile.write(t('html') + nl())
		myfile.write(t('head') + nl())
		myfile.write(t('link type="text/css" rel="stylesheet" ') + nl())

		myfile.write(html_space(4) + t('style'))
		myfile.write('table{width= 100%; border-collapse:collapse; border:1px solid black collapse}')
		myfile.write('th,td {padding:3px}' + nl())
		myfile.write(html_space(8) + 'td.detail{background-color:#D5DF93; font-size:20;'
									 'font-family:Helvetica, Arial, Sans Serif; font-weight:bold}' + nl())
		myfile.write(html_space(8) + 'td.detail1{font-size:20;'
									 'font-family:Helvetica, Arial, Sans Serif; font-weight:bold}' + nl())
		myfile.write(html_space(8) + 'td.detail2{font-size:20;'
									 'font-family:Helvetica, Arial, Sans Serif}' + nl())
		myfile.write(html_space(8) + 'td.header0{background-color:#8fac3a; font-size:20;'
									 'font-family:Helvetica, Arial, Sans Serif; font-weight:bold}' + nl())
		myfile.write(html_space(8) + 'td.header1{background-color:#E6E6E6; font-size:20;'
									 ' font-family:Helvetica, Arial, Sans Serif; font-weight:bold}' + nl())
		myfile.write(html_space(8) + 'td.header2{font-size:20; width:50%}' + nl())
		myfile.write(html_space(4) + t('/style') + nl())

		myfile.write(t('/head') + nl())
		myfile.write(t('body') + nl())

		self.company_name = str(report_summary["ProfileSummary"]['CompanyName'])
		self.company_logo = str(report_summary["ProfileSummary"]['CompanyLogo'])
		self.group_team_name = str(report_summary["ProfileSummary"]['Group/TeamName'])
		self.designer = str(report_summary["ProfileSummary"]['Designer'])
		self.project_title = str(report_summary['ProjectTitle'])
		self.sub_title = str(report_summary['Subtitle'])
		self.job_number = str(report_summary['JobNumber'])
		self.client = str(report_summary['Client'])
		additional_comments = str(report_summary['AdditionalComments'])


def space(n):
	"""Create html code to create tab space in html-output.

	Args:
		n (int): number of tab spaces to be created in the html-output.

	Returns:
		rstr (str): html code that creates 'n' number of tab spaces.
	"""
	rstr = "&nbsp;" * 4 * n
	return rstr


def t(param):
	"""Enclose argument in html tag.

	Args:
		param (str): parameter to be enclosed in html tag <>.

	Returns:
		rstr (str): given param enclosed in html tag <>.
	"""
	return '<' + param + '>'


def w(n):
	"""Enclose argument in curly brace parenthesis.

	Args:
		n (str): parameter to be enclosed in curly brace parenthesis.

	Returns:
		rstr (str): given param enclosed in curly brace parenthesis.
	"""
	return '{' + n + '}'


def quote(m):
	"""Enclose argument in double quotes.

	Args:
		m (str): parameter to be enclosed in double quotes

	Returns:
		rstr (str): given param enclosed in double quotes
	"""
	return '"' + m + '"'


def nl():
	"""Create new line.

	Args:

	Returns:
		new line tag.

	Note:
		Instead of directly inserting the new line tag '\n' in the code, this function was created,
		to enable custom formatting in future.
	"""
	return '\n'


def html_space(n):
	"""Create space in html code.

	Args:
		n (int): number of spaces to be created in the html-code.

	Returns:
		(str): specified number_of_spaces
	"""
	return " " * n


def sub(string, subscript):
	"""Create html code to display subscript.

	Args:
		string (str):
		subscript (str): string to be subscript

	Returns:
		(str): html code with concatenated string and subscript
	"""
	return string + "<sub>" + subscript + "</sub>"

