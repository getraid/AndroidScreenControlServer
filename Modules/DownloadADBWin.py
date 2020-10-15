import dload
import sys


def Download():
    sys.path.append("..")
    dload.save_unzip(
        "https://dl.google.com/android/repository/platform-tools-latest-windows.zip", "Modules/.")
