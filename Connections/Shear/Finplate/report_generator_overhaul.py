def space(n):
    rstr = "&nbsp;" * 4 * n
    return rstr

def t(n):
    return '<' + n + '>'

def w(n):
    return '{' + n + '}'

def quote(m):
    return '"' + m + '"'

def nl():
    return '\n'

def html_space(n):
    return " " * n
	
def summary_row(tab_spaces, text_one, text_one_css, text_two = " ", text_two_css = text_one_css):
	"""Create formatted html row entry.
	
	Args:
		tab_spaces (int): number of (tab) spaces
		text_one (str): Text entry
		text_one_css (str): Key pointing to table-data css format
		text_two (str): Text entry
		text_two_css (str): Key pointing to table-data css format
	
	Returns (str):
		Formatted line of html-code.
		
	"""
	
