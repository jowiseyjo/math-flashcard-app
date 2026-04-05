[app]
title = FlashcardApp
package.name = flashcard
package.domain = org.education

version = 0.1

source.dir = .
source.include_exts = py,kv,png,jpg,mp3,wav

requirements = python3,kivy

orientation = portrait

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

android.permissions = INTERNET
