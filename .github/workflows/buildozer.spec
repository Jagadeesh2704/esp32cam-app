[app]
title = ESP32CAM Setup
package.name = esp32camsetup
package.domain = org.esp32cam
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_WIFI_STATE,ACCESS_NETWORK_STATE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.arch = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
