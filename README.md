# Financial-report-by-sms
This code generates a finance management report based on your 'رمز پویا' messages.<br />
It only works on 'Sepah bank' and 'Blu bank' messages.<br />
First go and install SMS Backup & Restore from here https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore&pcampaignid=web_share<br />
Install it on your phone and only backup the conversation sending رمز پویا<br />
For Blu bank its '+989999987641' and for Sepah bank its '986715014'. You can backup both if you use both.<br />
Take the file to your computer and put it in the same folder as the code, and rename it to 'sms_data.xml'.<br />
Get rid of all the non-informative lines, each line should start with '  <sms protocol='. remove the rest.<br />
Now for the libraries, install the followings:<br />
```
pip install xmltodict
```
```
pip install regex
```
```
pip install datetime
```
```
pip install python-bidi
```
```
pip install persian
```
```
pip install reportlab
```
Also copy persian_reshaper.py to python/lib folder. this file is needed to show Persian fonts properly.<br />
Mentioned directory can often be found at C:\Program Files\Python311\Lib, or C:\Python\Lib, if not, search "python.exe" and you may find it with ease.<br />
