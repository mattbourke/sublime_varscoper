import sublime, sublime_plugin
import urllib
import os
from xml.dom import minidom

# -- below is originally from sublime linter
# Select one of the predefined gutter mark themes, the options are:
# "alpha", "bright", "dark", "hard" and "simple"
MARK_THEMES = ('alpha', 'bright', 'dark', 'hard', 'simple')
# The path to the built-in gutter mark themes
MARK_THEMES_PATH = os.path.join('..', 'sublimeVarScoper', 'gutter_mark_themes')
# The original theme for anyone interested the previous minimalist approach
ORIGINAL_MARK_THEME = {
    'violation': 'dot',
    'warning': 'dot',
    'illegal': 'circle'
}

class eventsstuff(sublime_plugin.EventListener):
	# these are called on certain events
	# this is called when someone does the default save of ctrl+s or file menu save etc
	def on_post_save(self, view='none'):
		sublime.active_window().run_command("runvarscoperhighlight")

	def on_load(self, view='none'):
		sublime.active_window().run_command("runvarscoperhighlight")

class runvarscoperhighlightCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		varscoper_cfm_url = self.view.settings().get('varscoper_cfm_url', 'http://127.0.0.1:8888/varscoper/varScoper.cfm?')
		varScoperBaseURL  = varscoper_cfm_url+'displayFormat=xml&'
		if len(self.view.file_name()) > 0:
			varScoperLink = varScoperBaseURL + 'filePath=' + self.view.file_name()
			self.view.erase_status('varscoper')
			try:
				resp = urllib.urlopen(varScoperLink)
				code = urllib.urlopen(varscoper_cfm_url).getcode()
				if code != 200:
					sublime.error_message('Server '+varscoper_cfm_url+' non raggiungibile')
					return
				data     = resp.read()

				xmldoc   = minidom.parseString(data)
				itemlist = xmldoc.getElementsByTagName('line_number')
				first    = False
				regions = []
				for s in itemlist :
					line = self.getText(s.childNodes)
					p    = self.view.text_point(int(line)-1, 0)
					regions.append(self.view.full_line(p))

				self.view.add_regions('varscoper', regions, 'string', MARK_THEMES_PATH+'/hard-illegal',sublime.HIDDEN)
				if len(regions) > 0:
					if(not first):
						# self.view.show(p)
						first = True

				if len(itemlist) > 0:
					self.view.set_status('varscoper', str(len(itemlist)) + ' Unscoped variables found, please see the gutter icons next to each affected row')


			except (urllib.error.HTTPError) as e:
				sublime.error_message(str(e))

	def getText(self, nodelist):
		rc = []
		for node in nodelist:
			if node.nodeType == node.TEXT_NODE:
				rc.append(node.data)
		return ''.join(rc)