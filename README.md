# MTA Notifier

A simple set of Python scripts to inform me of the status of the [NYC Subway](http://www.mta.info/).   
The default configuration is to check the status of the 123 and ACE lines and email me 
if the status is not GOOD SERVICE.

This uses a [Mailgun](https://mailgun.com) sandbox server to send emails. 

If you want to set this up for your use, you'll need to:

1. Create a (free) Mailgun account
2. Add the API keys to a api_secrets.json.nogit file or to your environment. 
See **notifier.py** for which things you need to specify.
3. Create and edit a [launchd](http://launchd.info/) file to run **run_now.py** (or a script calling it) 
and set to the frequency you want

The file **clock.py** is used to set up scheduling in [Heroku](http://www.heroku.com), 
allowing this to be run like a cron job but on a cloud server. This is still being tested.