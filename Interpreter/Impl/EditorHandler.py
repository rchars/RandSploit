import configparser as cr
import pathlib


class Handler:
	def __init__(self, editor_file_path, current_editor=''):
		self._editor_file_path = editor_file_path
		self._current_editor = current_editor or self._setup_editor()

	def _setup_editor(self, new_file=None):
		if self._editor_file_path.is_file():
			reader = cr.ConfigParser()
			with self._editor_file_path.open('r') as config_file:
				reader.read_file(config_file)
			self._current_editor = reader.get('', 'editor')

	def ask_for_editor(self, force=False):
		if self._current_editor:
			return self._current_editor
		editor_str = input('Editor:').strip('\n')
		if not editor_str:
			raise RuntimeError('Editor not chosen')
		self._current_editor = editor_str
		return editor_str

	@property
	def editor_file_path(self):
		return self._editor_file_path

	@property
	def current_editor(self):
		return self._current_editor

	@current_editor.setter
	def current_editor(self, new_editor_str):
		self._current_editor = new_editor_str
