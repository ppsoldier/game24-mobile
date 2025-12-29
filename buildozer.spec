[app]

title = 24点扑克牌游戏
package.name = game24
package.domain = org.game24

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0

presplash.filename = %(source.dir)s/data/presplash.png
icon.filename = %(source.dir)s/data/icon.png

[buildozer]

log_level = 2

warn_on_root_pitcher = True

[buildozer.target.android]

android.archs = arm64-v8a,armeabi-v7a

android.ndk = 25b
android.sdk = 33

android.accept_sdk_license = True

android.minapi = 21
android.maxapi =

android.manifest = 

android.permissions = INTERNET

android.entrypoint = org.kivy.android.PythonActivity

android.gradle_dependencies =

android.add_src =

android.aars_dirs =

android.java_src_dirs =

android.uses_library =

[buildozer.target.ios]

ios.codesign.allowed = false
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

[buildozer.source]

include_exts = py,png,jpg,kv,atlas,json

[buildozer.target.osx]

[buildozer.target.windows]

[buildozer.target.macos]
