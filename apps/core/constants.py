import calendar
from datetime import datetime, date

USER_POSITIONS = [
    "Church Member",
    "Pastor",
    "Men Department Leader",
    "Women Department Leader",
    "Teens Department Leader",
    "Church Secretary",
    "Church Treasurer",
]

GENDER_CHOICES = ["Male", "Female"]
STATUS_CHOICES = ["Active", "Inactive", "Suspended"]
GROUP_LEADER_POSITIONS = [
    "Chairperson",
    "Vice Chairperson",
    "Secretary",
    "Treasurer",
    "Welfare Officer",
    "Member",
]

MONTHS_LIST = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

YEARS_LIST = [2025, 2026, 2027, 2028, 2029, 2030]


def get_month_number(month_name: str) -> int:
    try:
        # Normalize to capitalize first letter only, e.g. "january" → "January"
        month_name = month_name.capitalize()
        return list(calendar.month_name).index(month_name)
    except ValueError:
        return -1  # return -1 if invalid


def get_month_name(month_number: int) -> str:
    return calendar.month_name[month_number]


def format_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()
