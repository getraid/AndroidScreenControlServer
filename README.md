# Android ScreenControl Server
(name pending)

Requires Python 3.X (Written with Python 3.8)  

Install depedencies with `pip install -r "requirements.txt"`

Make sure to use `python AndroidScreenControlServer.py` instead of `py AndroidScreenControlServer.py`, if the program doesn't run properly


To disable console output, rename file from `AndroidScreenControlServer.py` to `AndroidScreenControlServer.pyw`

If you want to use this with **IOS or other devices without ADB**, you can simply set `UseADB` in the `config.ini` file to `False` and set your `WebserverHost` to `0.0.0.0`.
Now your server will simply run under your local ip adress, which you can call from your internet browser.
You will be limited to PC actions only though, as you can't communicate to the device directly.

tbd...

Issues:
* Upon stopping server, bunch of errors are thrown. Haven't figured out why yet
