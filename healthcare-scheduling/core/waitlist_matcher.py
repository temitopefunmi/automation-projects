def find_best_waitlist_match(waitlist_df, slot):
    provider = slot["provider"]
    appt_time = slot["appt_datetime"]

    candidates = waitlist_df[
        (waitlist_df["provider_requested"] == provider) &
        (waitlist_df["status"] == "waiting")
    ]

    candidates = candidates[
        (candidates["preferred_times"] == "any") |
        
(candidates["preferred_times"].str.contains(str(appt_time.date())))
    ]

    candidates = candidates.sort_values("urgency", ascending=False)

    return None if candidates.empty else candidates.iloc[0].to_dict()

