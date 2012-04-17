import time, logging, os, subprocess, sys
from optparse import OptionParser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO,
					format='%(asctime)s %(levelname)s - %(message)s',
					datefmt='%Y-%m-%d %H:%M:%S')

class HandlebarsEventHandler(FileSystemEventHandler):
	"""Watches and precompiles handlebars templates."""

	def __init__(self, template_dir, compile_dir):
		self.template_dir = template_dir
		self.compile_dir = compile_dir

	def get_compiled_path(self, file):
		"""Returns the path the compiled file"""
		return file.replace(self.template_dir, self.compile_dir) + '.js' 

	def compile(self, file):
		"""Compile a file using handlebars"""
		compiled = self.get_compiled_path(file)
		logging.info("Compiling: %s", compiled)
		
		compiled_dir = os.path.dirname(compiled)
		if not os.path.exists(compiled_dir):
			os.makedirs(compiled_dir)
		 
		cmd = ['handlebars', file, '-f', compiled, '-k', 'each', '-k', 'if', '-k', 'unless']
		process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(stdout, stderr) = process.communicate()
		if stderr:
			logging.warn('Error while compiling: %s', stderr)

	def remove(self, file):
		"""Remove a file"""
		compiled = self.get_compiled_path(file)
		if os.path.exists(compiled):
			logging.info("Removing: %s", compiled)
			os.remove(compiled)

	def on_moved(self, event):
		super(HandlebarsEventHandler, self).on_moved(event)
		if event.is_directory:
			# Ignore directories
			return False
		logging.info("Moved detected: from %s to %s", event.src_path, event.dest_path)
		self.remove(event.src_path)
		self.compile(event.dest_path)

	def on_created(self, event):
		super(HandlebarsEventHandler, self).on_created(event)
		if event.is_directory:
			# Ignore directories
			return False

		logging.info("New file detected: %s", event.src_path)
		self.compile(event.src_path)

	def on_deleted(self, event):
		super(HandlebarsEventHandler, self).on_deleted(event)
		if event.is_directory:
			# @todo Remove compiled directories
			return False
		logging.info("Deletion detected: %s", event.src_path)
		self.remove(event.src_path)

	def on_modified(self, event):
		super(HandlebarsEventHandler, self).on_modified(event)
		if event.is_directory:
			# @todo Remove compiled directories
			return False
		logging.info("Change detected: %s", event.src_path)
		self.compile(event.src_path)

def main():
	"""Entry-point function."""
	parser = OptionParser()
	parser.add_option("-t", "--template-dir", dest="template_dir", default='handlebars',
	                  help="Relative path to handlebar template directory [default: %default]")
	parser.add_option("-c", "--compile-dir", dest="compile_dir", default=os.path.join('assets', 'js', 'handlebars'),
	                  help="Relative path to handlebar pre-compiled templates directory [default: %default]")
	parser.add_option("-r", "--refresh", dest="refresh", default=False, action="store_true",
	                  help="When specified, all template files will be recompiled")
	parser.add_option("-n", "--no-watch", dest="no_watch", default=False, action="store_true",
	                  help="Don't watch - can be used with --refresh to exit upon compiling all templates.")
	
	(options, args) = parser.parse_args()

	template_dir = os.path.join(os.getcwd(), options.template_dir)
	compile_dir = os.path.join(os.getcwd(), options.compile_dir)

	if not os.path.exists(template_dir):
		print "Template directory '%s' doesn't exist." % (template_dir)
		sys.exit(1)
		
	if not os.path.exists(compile_dir):
		print "Compile directory '%s' doesn't exist." % (compile_dir)
		sys.exit(1)

	event_handler = HandlebarsEventHandler(template_dir, compile_dir)
	
	if options.refresh:
		for i in os.walk(template_dir):
			for file in i[2]:
				path = os.path.join(i[0], file)
				if os.path.exists( path ):
					event_handler.compile(path)
	
		if options.no_watch:
			sys.exit()

	observer = Observer()
	observer.schedule(event_handler, path=template_dir, recursive=True)
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
			observer.stop()
	observer.join()

if __name__ == '__main__':
  main()