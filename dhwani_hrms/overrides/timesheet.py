import frappe
from frappe import _
from frappe.utils import getdate
from datetime import timedelta


# dhwani_hrms.overrides.timesheet.before_submit
def before_sumbit(self, method):
    if self.workflow_state == "Approved":
        settings = frappe.get_single("Timesheet Settings")

        min_hours_day = settings.minimum_hours_per_day
        max_hours_day = settings.maximum_hours_per_day
        min_hours_week = settings.minimum_hours_per_week
        max_hours_week = settings.maximum_hours_per_week

        validate_daily_hours(self, min_hours_day, max_hours_day)
        # validate_weekly_hours(self, min_hours_week, max_hours_week)


def validate_daily_hours(self, min_hours_day, max_hours_day):
    hours = self.total_hours
    if min_hours_day and hours < min_hours_day:
        frappe.throw(
            _(
                f"Total hours today are less than minimum working hours per day: {min_hours_day}"
            )
        )
    if max_hours_day and hours > max_hours_day:
        frappe.throw(
            _(
                f"Total hours today are more than minimum working hours per day: {max_hours_day}"
            )
        )


def validate_weekly_hours(self, min_hours_week, max_hours_week):
    if not self.time_logs:
        return  # Skip if no time logs

    first_log_date = getdate(self.time_logs[0].from_time)

    # Calculate week start date (Sunday)
    week_start_date = first_log_date - timedelta(days=first_log_date.weekday())
    week_end_date = week_start_date + timedelta(days=6)

    weekly_hours = 0
    for log in self.time_logs:
        log_date = getdate(log.from_time)
        if week_start_date <= log_date <= week_end_date:
            weekly_hours += log.hours

    if min_hours_week and weekly_hours < min_hours_week:
        frappe.throw(
            _(
                "Total hours in week starting {0}  are less than minimum working hours per week: {1}"
            ).format(week_start_date.strftime("%Y-%m-%d"), min_hours_week)
        )

    if max_hours_week and weekly_hours > max_hours_week:
        frappe.throw(
            _(
                "Total hours in week starting {0} exceed maximum working hours per week: {1}"
            ).format(week_start_date.strftime("%Y-%m-%d"), max_hours_week)
        )


# dhwani_hrms.overrides.timesheet.get_all_employees
@frappe.whitelist(allow_guest=True)
def get_employees(**kwargs):
    return frappe.session.user
