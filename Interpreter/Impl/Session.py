import multiprocessing as mp
import contextlib
import sys
import io


# Many problems
class Session(mp.Process):
	class FakeSTDIN(io.TextIOBase):
		def __init__(self, child_conn):
			self.child_conn = child_conn
			super().__init__()

		def read(self, size=-1): return self.child_conn.recv()

		readline = read

	class FakeOUT(io.TextIOBase):
		def __init__(self, child_conn):
			self.child_conn = child_conn

		def write(self, data): self.child_conn.send(data)

	def __init__(self, mod_inst):
		super().__init__()
		self.parent_conn, self.child_conn = mp.Pipe()
		self.fake_stdout = self.FakeOUT(self.child_conn)
		self.fake_stdin = self.FakeSTDIN(self.child_conn)
		self.mod_inst = mod_inst
		# Change it to property
		self.bg = False

	def run(self):
		if self.bg:
			sys.stdin = self.fake_stdin
			sys.stdout = self.fake_stdout
			sys.stderr = self.fake_stdout
		self.mod_inst.run()
