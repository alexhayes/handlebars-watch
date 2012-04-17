# handlebars-watch

Watches a specified location and on detecting a file change, precompiles the file
using **handlebars**.  

## Requirements

1. [handlebars](http://handlebarsjs.com/precompilation.html) binary must be installed.
2. Python [watchdog](http://packages.python.org/watchdog/) must be on your Python path.

## Installation

```bash
git clone git://github.com/alexhayes/handlebars-watch.git
cd handlebars-watch
python setup.py install
```

## Usage

```bash
cd my-project
mkdir handlebars
echo "<div>{{ var }}</div>" > handlebars/template.html
mkdir -p assets/js/handlebars
handlebars-watch -r
```

Will create the precompiled template at _assets/js/handlebars/template.html.js_

## Options

	$ handlebars-watch -h
	Usage: handlebars-watch [options]
	
	Options:
	  -h, --help            show this help message and exit
	  -t TEMPLATE_DIR, --template-dir=TEMPLATE_DIR
	                        Relative path to handlebar template directory
	                        [default: handlebars]
	  -c COMPILE_DIR, --compile-dir=COMPILE_DIR
	                        Relative path to handlebar pre-compiled templates
	                        directory [default: assets/js/handlebars]
	  -r, --refresh         When specified, all template files will be recompiled
	  -n, --no-watch        Don't watch - can be used with --refresh to exit upon
	                        compiling all templates.

## Todo

- Currently it doesn't handle deletion of template directories. 

## License

Dual licensed under the MIT or GPL Version 2 licenses.
