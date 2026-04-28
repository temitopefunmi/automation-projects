def get_cancelled_appointments(appointments_df):
    return appointments_df[appointments_df["status"] == "cancelled"]

