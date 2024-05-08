from datetime import datetime, timedelta


HOLIDAYS = [
    "2024-01-01", "2024-01-15", "2024-05-27", "2024-06-19",
    "2024-07-04", "2024-07-05", "2024-09-02", "2024-11-28",
    "2024-11-29", "2024-12-23", "2024-12-24", "2024-12-25",
    "2024-12-26", "2024-12-27", "2024-12-28", "2024-12-29",
    "2024-12-30", "2024-12-31", "2025-01-01", "2025-01-20",
    "2025-05-26", "2025-06-19", "2025-07-04", "2025-09-01",
    "2025-11-27", "2025-12-25"
]

ADJUSTED_POST_DATE = [
    "2024-06-03", "2024-09-03", "2024-12-02"
]

def return_dates(list_of_dates):
    """
    Use datetime.date objects for easier comparisons.
    """

    return [datetime.strptime(date, "%Y-%m-%d").date() for date in list_of_dates]


def schedule_review_post(date):
    """
    Determine and return the new posting date avoiding weekends and holidays.
    """

    if date.weekday() >= 5:  # Saturday or Sunday
        date += timedelta(days=7 - date.weekday())  # Move to next Monday

    while date in return_dates(HOLIDAYS):  # Check if it's a holiday and adjust
        date += timedelta(days=1)

    return date


def monthly_review(date):
    """
    Monthly review posted on the first of the month, adjusted for weekends and holidays.
    """

    # Check if it's the first of the month
    if date.day == 1 or date.date() in return_dates(ADJUSTED_POST_DATE):
        if date.day != schedule_review_post(date).day:
            newdate = schedule_review_post(date).strftime("%Y-%m-%d")
            ADJUSTED_POST_DATE.append(newdate)
            return None

        review_month = ((date) - timedelta(days=5)).strftime("%B")
        print(f"Monthly Review for {review_month}")

        return review_month


def weekly_review(date):
    """
    Weekly review posted on Monday, adjusted for holidays.
    """

    yesterday = (date - timedelta(days=1)).date()

    if date.date() in return_dates(HOLIDAYS):
        return None

    if date.weekday() == 0 or yesterday in return_dates(HOLIDAYS):
        # Determine last Monday to Sunday range
        last_monday = date - timedelta(days=date.weekday() + 7)
        last_sunday = last_monday + timedelta(days=6)

        # Adjust the posting day if necessary
        post_date = date if date.weekday() == 0 else date + timedelta(days=1)
        post_date = schedule_review_post(post_date)

        timerange = f"{last_monday.strftime('%m/%d')} - {last_sunday.strftime('%m/%d')}"
        print(f"Weekly Review: for: {timerange}")

        return timerange


if __name__ == '__main__':
    # Simulate running daily
    for i in range(30):
        date = datetime(2024, 12, 1) + timedelta(days=i)
        print(date)
        monthly_review(date)
        weekly_review(date)
