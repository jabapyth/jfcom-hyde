
serve:
	hyde serve

contents: content/media/css content/* content/*/* content/*/*/* content/*/*/*/*
	hyde gen

style: content/media/css

content/media/css: content/media/styl/
	stylus content/media/styl -o content/media/css

watch-style:
	stylus --watch content/media/styl -o content/media/css

get-projects:
	python github-projects.py jaredly projects.json

process-projects:
	/usr/bin/python github/gh-hyde.py projects.json content/projects/_hidden

.PHONY: style watch-style get-projects process-projects
