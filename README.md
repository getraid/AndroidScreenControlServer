# Android ScreenControl Server
The idea was to use a cheap FireHD Tablet to use as a StreamDeck or generally as a direct connection PC HMI device.  

I found out later, that while it worked, I didn't really have a use for it. So I stopped development on this tool as well.  
It should theoretically still work (besides maybe missing/outdated dependencies).  

---

Requires Python 3.X (Written with Python 3.8)  

Install depedencies with `pip install -r "requirements.txt"`

Attention: One package is not included in the `requirements.txt`, because it has a typo in a command that I'm using here.
So I made a git fork with some merges from @Hamz-a.
To install this, you need to have git installed as well.
- `pip install git+https://github.com/getraid/pure-python-adb.git#egg=pure-python-adb`

Make sure to use `python AndroidScreenControlServer.py` instead of `py AndroidScreenControlServer.py`, if the program doesn't run properly


To disable console output, rename file from `AndroidScreenControlServer.py` to `AndroidScreenControlServer.pyw`

If you want to use this with **IOS or other devices without ADB**, you can simply set `UseADB` in the `config.ini` file to `False` and set your `WebserverHost` to `0.0.0.0`.
Now your server will simply run under your local ip adress, which you can call from your internet browser.
You will be limited to PC actions only though, as you can't communicate to the device directly.

tbd...

Issues:
* Upon stopping server, bunch of errors are thrown. Haven't figured out why yet
