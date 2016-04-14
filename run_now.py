# Script to immediately check the MTA status
import notifier
m = notifier.Notifier()

# Default lines are 123 and ACE
# Default notifications are for DELAYS and PLANNED WORK
m.get_status(['123', 'ACE'])
#m.send_email_message() # Uncomment to send email