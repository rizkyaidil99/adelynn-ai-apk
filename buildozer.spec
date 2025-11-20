[app]
title = Adelynn AI
package.name = adelynnai
package.domain = org.kazeo
source.dir = .
source.include_exts = py,png,jpg,kv,ico,json,txt
version = 0.1
requirements = python3,kivy,requests
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/adelynn.ico
presplash.filename =
android.api = 33
android.minapi = 21
android.arch = arm64-v8a,armeabi-v7a,x86,x86_64
# (add other settings as needed)

[buildozer]
log_level = 2
warn_on_root = 1
