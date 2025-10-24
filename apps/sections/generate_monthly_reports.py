from apps.sections.models import SectionMonthlyReport, SectionReport

months_list = [
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


def generate_monthly_reports():
    section_reports = SectionReport.objects.all()
    for section_report in section_reports:
        for month in months_list:
            SectionMonthlyReport.objects.get_or_create(
                section_report=section_report,
                month=month,
                year=section_report.year,
            )
    print("Monthly reports generated successfully.")
