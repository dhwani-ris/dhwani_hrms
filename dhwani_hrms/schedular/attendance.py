import frappe
import requests
from dhwani_hrms.schedular.utils import generate_token
from datetime import datetime, timedelta, time
import re


@frappe.whitelist(allow_guest=True)
def get_attendance():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 8, 30)

    current_date = start_date
    while current_date <= end_date:
        next_date = current_date + timedelta(days=59)  # 60 days total
        next_date = min(next_date, end_date)  # Don't go past the end date

        from_date_str = current_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        to_date_str = next_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        url = f"https://dhwaniris.keka.com/api/v1/time/attendance?from={from_date_str}&to={to_date_str}&pageNumber=1&pageSize=200"

        bearer_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjFBRjQzNjk5RUE0NDlDNkNCRUU3NDZFMjhDODM5NUIyMEE0MUNFMTgiLCJ4NXQiOiJHdlEybWVwRW5HeS01MGJpaklPVnNncEJ6aGciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2xvZ2luLmtla2EuY29tIiwibmJmIjoxNzM2NDMxNTkxLCJpYXQiOjE3MzY0MzE1OTEsImV4cCI6MTczNjUxNzk5MSwiYXVkIjpbImtla2FhcGkiLCJodHRwczovL2xvZ2luLmtla2EuY29tL3Jlc291cmNlcyJdLCJzY29wZSI6WyJrZWthYXBpIl0sImFtciI6WyJrZWthYXBpIl0sImNsaWVudF9pZCI6Ijc2OWJkOTA5LTQzNWMtNDIzNi1hZDc5LTU3MGY2ZGFkZDZmYyIsInN1YiI6IjMwMDgzOGI1LWI3OTEtNDU5NS04MjFhLTE1NTA3M2Q5MzNlMCIsImF1dGhfdGltZSI6MTczNjQzMTU5MSwiaWRwIjoibG9jYWwiLCJ0ZW5hbnRfaWQiOiI5ZjBiMDVkYi0zNzJlLTQ0YzUtYWFmYS0yNzQ3MWI3MWE4NjgiLCJ0ZW5hbnRpZCI6IjlmMGIwNWRiLTM3MmUtNDRjNS1hYWZhLTI3NDcxYjcxYTg2OCIsImFwcF9uYW1lIjoiRnJhcHBlIC0gU3RhZ2luZyIsInN1YmRvbWFpbiI6ImRod2FuaXJpcy5rZWthLmNvbSIsImp0aSI6IjkzNUE0OUZEMTQ0NTU1OTZBRDM3MTE0MzQ0MDU0QjBDIn0.Tl6Xq4TqGzo-HJeXNMR0wA1JpFErWFD7c54XDrgSyxvoirAcvtQUvsnOVS5PC-ISfFV1L_Txx0bVZdPW3plKt6a1WAOQGAWry2NygRkW4s2qkLZL6UJo_cQr-QzPwPoO625LNV8k9F_KULZqOLNJq7ddOgrRF5C1Cj0XoFX4WejmiVFBwBJjk8zPVvYOZ9KKZva46o8p7muE5sFNLkGcUN_hFU70tmzYdidvEdIlK1htAx4JRa9qW5N3VaqAnnGBCgN-Tos_oKjXznOV3MkdTRhCJC5iSyCrwTm7ddj2VI_TFueIuwJ2C8-pkWrrT6vu1H5Z-5JnOJZ2AHjFZ5rswg"
        response = get_data(url, bearer_token)

        if response.get("exception"):
            frappe.log_error(
                f"Keka API Error: {response.get('exception')}"
            )  # Log the error for debugging
            return "Error fetching attendance data. Check error logs."  # Stop and signal an error.

        frappe.enqueue(  # Enqueue the processing function
            process_attendance, response=response, timeout=600  # Set timeout as needed
        )

        current_date = next_date + timedelta(days=1)  # Move to the next 60-day period

    return "Done"


def get_data(url, bearer_token):
    payload = {}
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {bearer_token}",
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


def process_attendance(response):
    shift_start = time(10, 0, 0)  # 10:00 AM
    shift_end = time(19, 0, 0)
    for attendance_data in response.get("data"):
        if frappe.db.exists(
            "Attendance",
            {
                "attendance_date": attendance_data.get("attendanceDate"),
                "employee": attendance_data.get("employeeNumber"),
            },
        ):
            pass
        else:
            att_doc = frappe.new_doc("Attendance")
            att_doc.attendance_date = format_date(attendance_data.get("attendanceDate"))
            att_doc.employee = attendance_data.get("employeeNumber")
            att_doc.company = "DhwaniRIS"
            att_doc.status = "Absent"
            att_doc.shift = "General Shift"

            if attendance_data.get("firstInOfTheDay"):
                att_doc.status = "Present"
                in_time = format_datetime(
                    attendance_data.get("firstInOfTheDay").get("timestamp")
                )
                att_doc.in_time = in_time
                att_doc.late_entry = in_time.time() > shift_start
            if attendance_data.get("lastOutOfTheDay"):
                out_time = format_datetime(
                    attendance_data.get("lastOutOfTheDay").get("timestamp")
                )
                working_hours = (out_time - in_time).total_seconds() / 3600  # In hours
                att_doc.out_time = out_time
                att_doc.early_exit = out_time.time() < shift_end

                att_doc.working_hours = working_hours
            try:
                att_doc.save(ignore_permissions=True)
                att_doc.submit()
            except Exception as e:
                frappe.log_error(str(e))
    return "Done"


def format_date(date_str):

    timestamp = date_str

    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

    # Format to desired output
    formatted_date = dt.strftime("%Y-%m-%d")

    return formatted_date


def format_datetime(timestamp):
    # If the timestamp has fractional seconds, limit it to 6 digits
    if "." in timestamp:
        base_time, frac_seconds = timestamp.split(".")
        frac_seconds = frac_seconds[:6]  # Truncate or pad to 6 digits
        timestamp = f"{base_time}.{frac_seconds}Z"
    else:
        timestamp = (
            timestamp.rstrip("Z") + ".000000Z"
        )  # Add default fractional seconds if missing

    # Parse the timestamp with the proper format
    return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
