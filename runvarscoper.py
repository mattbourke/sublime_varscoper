import sublime, sublime_plugin
import webbrowser

class runvarscoperCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		varScoperLink = self.view.settings().get('varscoper_cfm_url', 'http://127.0.0.1:8888/varscoper/varScoper.cfm?parseCFScript=disabled')
		if len(self.view.file_name()) > 0:
			varScoperLink = varScoperLink + '&filePath=' + self.view.file_name()
			webbrowser.open_new(varScoperLink)
			msg = "File " + self.view.file_name() + " is running on VarScoper"
			sublime.status_message(msg)