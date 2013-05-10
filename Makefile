
serve:
	hyde serve

contents: style content/* content/*/* content/*/*/* content/*/*/*/*
	hyde gen

style: content/media/scss/*.styl
	stylus content/media/scss -o content/media/css

watch-style:
	stylus --watch content/media/scss -o content/media/css
