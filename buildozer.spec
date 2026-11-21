[app]

title = AfinoAi
package.name = afinoai
package.domain = org.kirox

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,svg,json,txt

version = 1.0.0

requirements = python3,kivy==2.3.1,requests

orientation = portrait
fullscreen = 0

icon.filename = afinoai_icon.png

android.permissions = INTERNET

android.api = 33
android.minapi = 23
android.ndk = 25b

android.archs = arm64-v8a

android.accept_sdk_license = True

p4a.bootstrap = sdl2


[buildozer]

log_level = 2
warn_on_root = 1
