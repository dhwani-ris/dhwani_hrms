app_name = "dhwani_hrms"
app_title = "Dhwani Hrms"
app_publisher = "Alok Shukla"
app_description = "Custom App For Dhwani HRMS"
app_email = "alok.shukla@dhwaniris.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
#     {
#         "name": "dhwani_hrms",
#         # "logo": "/assets/dhwani_hrms/logo.png",
#         "title": "Dhwani Hrms",
#         "route": "/dhwani_hrms",
#         # "has_permission": "dhwani_hrms.api.permission.has_app_permission"
#     }
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/dhwani_hrms/css/dhwani_hrms.css"
# app_include_js = "/assets/dhwani_hrms/js/dhwani_hrms.js"
app_include_js = [
    "/assets/dhwani_hrms/js/dhwani_hrms.js",
]
# include js, css files in header of web template
app_include_css = "/assets/dhwani_hrms/css/custombutton.css"
# web_include_css = "/assets/dhwani_hrms/css/dhwani_hrms.css"
# web_include_js = "/assets/dhwani_hrms/js/dhwani_hrms.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "dhwani_hrms/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Timesheet": "public/js/timesheet.js",
    "Leave Application": "public/js/leave_application.js",
    "Attendance Request": "public/js/attendance_request.js",
    "Employee": "public/js/employee.js",
    "Project": "public/js/project.js",
    "Attendance": "public/js/attendance.js",
    "Employee Checkin": "public/js/employee_checkin.js",
    "Compensatory Leave Request": "public/js/compensatory_leave_request.js",
}

doctype_list_js = {
    "Employee": "public/js/employee_list.js",
    "Project": "public/js/project_list.js",
    "Timesheet": "public/js/timesheet_list.js",
    "Attendance": "public/js/attendance_list.js",
    "Employee Checkin": "public/js/employee_checkin_list.js",
    "Attendance Request": "public/js/attendance_request_list.js",
    "Leave Application": "public/js/leave_application_list.js",
    "Compensatory Leave Request": "public/js/compensatory_leave_request_list.js",
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "dhwani_hrms/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "dhwani_hrms.utils.jinja_methods",
# 	"filters": "dhwani_hrms.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "dhwani_hrms.install.before_install"
# after_install = "dhwani_hrms.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "dhwani_hrms.uninstall.before_uninstall"
# after_uninstall = "dhwani_hrms.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "dhwani_hrms.utils.before_app_install"
# after_app_install = "dhwani_hrms.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "dhwani_hrms.utils.before_app_uninstall"
# after_app_uninstall = "dhwani_hrms.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "dhwani_hrms.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Attendance Request": {
        "on_cancel": "dhwani_hrms.dhwani_hrms.doc_events.attendance_request.on_cancel",
        "on_submit": "dhwani_hrms.dhwani_hrms.doc_events.attendance_request.on_submit",
        "validate": "dhwani_hrms.dhwani_hrms.doc_events.attendance_request.validate",
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"dhwani_hrms.tasks.all"
# 	],
# 	"daily": [
# 		"dhwani_hrms.tasks.daily"
# 	],
# 	"hourly": [
# 		"dhwani_hrms.tasks.hourly"
# 	],
# 	"weekly": [
# 		"dhwani_hrms.tasks.weekly"
# 	],
# 	"monthly": [
# 		"dhwani_hrms.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "dhwani_hrms.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "dhwani_hrms.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "dhwani_hrms.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["dhwani_hrms.utils.before_request"]
# after_request = ["dhwani_hrms.utils.after_request"]

# Job Events
# ----------
# before_job = ["dhwani_hrms.utils.before_job"]
# after_job = ["dhwani_hrms.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"dhwani_hrms.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
# fixtures = [
#     {"dt": "Custom Field", "filters": [["module", "in", ["Dhwani Hrms"]]]},
# ]
