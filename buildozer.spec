[app]
 !keytool -genkey -v \
-keystore inner_radiance.keystore \
-alias innerradiance \
-keyalg RSA \
-keysize 2048 \
-validity 10000
title = InnerRadiance
package.name = innerradiance
package.domain = org.inner

source.dir = .
source.include_exts = py,json

version = 0.1

requirements = python3,kivy

orientation = portrait
fullscreen = 1

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
