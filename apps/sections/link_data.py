from apps.sections.models import SectionReport
from apps.districts.models import KAGDistrictMonthlyReport

def link_data():
    section_reports = SectionReport.objects.all()

    for section_report in section_reports:
        existing_reports = KAGDistrictMonthlyReport.objects.filter(
            section=section_report.section,
            year=section_report.year,
        ).filter(section_report__isnull=True)
        
        existing_reports.update(section_report=section_report)
        print(f"Linked {existing_reports.count()} reports for Section {section_report.section.id} Year {section_report.year}")