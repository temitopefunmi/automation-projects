import pandas as pd
from .validators import validate_appointments, validate_waitlist

def load_manual_files(appt_path, waitlist_path):
    appts = pd.read_csv(appt_path, parse_dates=['appt_datetime'])
    waitlist = pd.read_csv(waitlist_path)

    validate_appointments(appts)
    validate_waitlist(waitlist)

    return appts, waitlist

