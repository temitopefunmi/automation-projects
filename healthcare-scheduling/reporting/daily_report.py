def generate_daily_report(appointments, 
output_file="data/daily_report.csv"):
    grouped = appointments.groupby(["provider","status"]).size().unstack(fill_value=0)
    grouped.to_csv(output_file)

