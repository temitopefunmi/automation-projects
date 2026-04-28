def fill_cancelled_slot(appointments_df, waitlist_df, slot, candidate):
    appointments_df.loc[
        appointments_df["appointment_id"] == slot["appointment_id"],
        ["patient_name", "status"]
    ] = [candidate["patient_name"], "scheduled"]

    waitlist_df.loc[
        waitlist_df["waitlist_id"] == candidate["waitlist_id"],
        "status"
    ] = "confirmed"

    return appointments_df, waitlist_df

