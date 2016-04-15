# Script to immediately check the MTA status
import notifier
m = notifier.Notifier()

# Default lines are 123 and ACE
# Default notifications are for DELAYS, PLANNED WORK, SERVICE CHANGE
m.get_status(['123', 'ACE'])

send_email = True
send_text = False

if send_email:
    m.send_email_message()