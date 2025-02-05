import frappe
import requests
from dhwani_hrms.schedular.utils import generate_token
from datetime import datetime, timedelta, time as dt_time
import re
import time

EMPLOYEE_IDS = """

86fa8211-0d4e-4af0-9f45-54e31917b2d0,099882ed-bac7-4a60-9feb-abfb66159bab,b1afc813-2df3-42bb-bbb5-8aa61561c30d,2ef9c6ab-dbc2-4571-b6ef-a903c93571d6,1af6c0a4-54a1-42f5-9e0e-14a9f5d2f591,300adda5-43e6-445c-8160-62123d4e69ac,e7e7f612-17ff-41a0-9d1e-d77f1999cf4e,c82b080c-4f62-434c-a075-176cda3736c4,355b9d14-f7e7-4c96-b377-7cf8c72274b5,7fffbb82-452b-48d6-831c-37fdf5e6b772,8390c5a0-5309-4aad-89c9-be531d4d6a27,3d0683db-7da9-4de0-8361-36266d7971f3,f418f377-05b8-4467-9358-ab3c6131475a,a508aba3-7eb5-485e-9a26-d56c8150b571,c673a7b2-9721-467b-9aa5-06b20c7c0a9e,313cb331-49b8-4434-a7a5-eeef1c5907e0,e2f0361b-1a9e-40aa-b094-73fc848c7c5b,0c9009f7-2749-4bec-988b-5ec5ac5826f5,39f0d614-bbf4-4a7d-ad03-5c4f9205bfcc,c2d2307d-3196-43f3-9aac-bebeb5841202,421af395-7988-4c4b-8fb9-8ee6a03e28b4,c716608a-ad7b-4468-989b-a9e66d08aa63,858d8311-433f-4ac7-9505-16974568daa0,539a0d3f-6464-4f45-895d-7dd29d9581aa,ea96d05a-adb1-440a-8561-4b0589c5b449,f9f1b97a-8bd1-48c9-b3dc-811a64e71e79,8f37e2ff-1293-474f-b260-fbd6a6d6af77,124e6e7a-ab76-4963-9dee-e8ea630e1dd6,52f1a0be-338e-451e-982f-7ba354388404,7dc52195-891f-4a47-afa7-fb891bf8c490,745261b1-2a5e-4939-89c7-86b0dc80d138,fd2197c5-4e24-4d11-8756-66bed157b5bd,41c67c15-caae-4818-825f-d0bfc1143a39,08881f2d-1170-4df5-9abc-b7073d169ea8,78635dcb-7092-4ff7-8ef0-fea9bed3cef4,a0311af4-c291-4bfd-acfa-02e3f4e29732,da394c22-3b4f-4432-81f3-d0de7b876484,cb95c07a-2e20-4ba7-8b25-c171f82f64f1,6e6a9842-2411-4748-a8f1-579a69411400,6cf0948a-5641-4ec4-b0ee-024a61034c7c,586427f8-2098-4b43-a037-4d02fcba5590,d9ded02f-5832-44c6-9b93-63243fc2609b,a8570dac-68cf-4264-9378-57104a71ef07,f278c261-9a04-4a47-b598-9028a14481f1,f912cc32-a147-4a7f-bc99-7d298761124f,b45022cb-64b9-45c3-b8e8-99476645e2f7,05f21edf-7d7f-47fd-9437-ba111bca0c8d,069f8f27-7f5e-4134-9504-3c95145e163f,b1ce2cc7-2d77-4aef-9295-043a5e023f5f,20682cee-b311-4077-948d-b3ad98195831,a7a40161-968a-4493-81e3-ba2f86b22e12,29f4e613-2f08-479f-a88d-4fab7cda5302,a80d9557-1009-4012-b9a5-a0f183621b62,49af3e2e-fcac-4708-aca0-7e349f1f6660,051a79f0-c452-4976-9432-afb5dfa498a2,72e2fb7f-bcaf-4ae1-abe6-fb5af829ea6e,3a9bd2f0-cbeb-4866-823e-5e250c7df2d3,3c5ba4b9-8d30-40e9-9dc1-12c8a4e06d45,31d19740-b0c6-427e-b3c7-73760559c267,67a8862e-d9a2-4172-9b32-a2fe262879fb,9e65c78a-1379-48a9-a089-db7a7a84e1be,9d46a35e-b500-453d-a3ae-c174a62822b7,acadbc22-8ed2-4aa7-888e-2826b1f2fdad,7f7b3651-476c-4722-9b70-a09c236177a5,bc989c52-0c96-42b3-b362-c81e36157984,52ed8cf6-c6ca-4c34-92fd-7709695a089b,7c494691-b541-4d0f-98c9-90cc07bd5a70,fd44f610-340b-4a73-9bc6-bbc95729b82e,b9264ab7-dc1e-49e2-bfcf-7a2ed0c2f451,cabe9099-bb26-401b-91e1-1fba20e07360,57d3a2fa-83b1-4cb2-aa50-b5af5e07b847,c173b856-848c-4a4e-b18e-f0e3a855761a,f3985363-b2d7-40d4-b2b0-64cb456f90b1,a483bec3-8c6a-45bb-8615-7f5fbd39e145,8f68137c-d771-4ea0-8b0c-4634a8411257,703ba2b8-c4d0-4b8f-b390-51d895a7e79c,fee83e6f-6dbb-4837-9967-229cf17fe444,e3ca3442-7cde-4ade-a362-77191b3cf066,97209b6e-1dff-4e2b-a0a5-4e700142c22e,bcdfca43-57ab-453f-9ff5-66f92c575756,548ba768-475f-49e0-ab25-47ff26c8e1ba,ed0b3d3b-a4ed-41f9-a037-942cbdd36958,647dba51-042c-465d-a1e3-dee1b8c40081,17846533-596e-404d-b237-6eeea541514a,d064fb84-cc62-4eaa-bc3a-72b702aa4b81,af68d1d1-dd85-40ec-ac6b-08b723178ddf,d3da0522-48d9-48a7-bfe8-9d5b6b45709a,c9abd4b0-7237-4c40-8991-17f6fa0795d4,567a9415-5ce7-4fb3-8df5-8384fbf0f0c3,04202fea-3d53-4aa3-b840-041018d1857b,209155e5-a4b2-4e69-9b0a-22f6cd03c4ab,a6438852-e53c-4a6f-8eda-8236c69f67ba,ccafe7bf-718a-4d8f-abd9-ac2d228aa675,9a5e4ea7-d44e-487a-9c8f-59a84d5c2a34,90cc2389-021e-40a9-924e-dd2b61b5a240,3cf8f102-e061-4421-b027-18b3cfba6d3d,cf9f2eaa-8cbc-47e8-afb1-0f41fa42f014,c8e648dc-4f88-4ca5-9d6d-5011cc356001,31d98e85-e778-459f-9c69-0e40a4582e71,72151b9a-f566-4c23-847e-72b6d25ebf1c,e7b600d8-e801-4caa-ad32-be4b0bc2e05f,fa6bf9c2-e195-4f2e-ad35-7bca312ce779,d1dd228e-53d0-4550-80c8-59f6c2bc6f7b,5a214e2c-f8db-44b1-a34c-e5759b620814,a6d970c2-ee55-4a64-948e-7b2380ff3b7f,0f012160-c106-4876-a422-f16f3f63bf61,be602521-57eb-4f36-bdee-8ac267d87be4,24439996-9836-4362-8959-b957b0ee98b0,f4f41828-ec5f-4c7a-bd95-8903d3758de2,eccf166d-f149-40c9-a3c7-fffd7b814d13,cea66232-1090-4487-b1aa-30473cffd6b9,59a3f041-385f-4e50-82d4-cd65a014b83f,ee9e6e07-a4fe-4898-bb22-17922ac4cfed,dcab5bc4-7b2c-4e0f-bd66-555cea06c1ac,c24e938d-a35b-4f14-9611-2d2a0bd0daec,b42cbbfc-e461-4836-84ef-8f421d832147,c047217b-5e8e-497b-8339-59a727267494,da1ed5f9-8cfb-4338-9c9d-83076d0373b8,f7cb2a30-d56e-4f1a-9e73-b4836888d876,21ac1e94-e949-4614-b526-2d39f6a5741b,df4342de-014c-4786-a9f6-bc35f533d321,752bbc00-97fb-4579-8f74-1f410eec5551,639b676a-a089-4383-b828-6cd7757f6204,6e9be4f1-9eef-4e26-bb0f-ef67db63cbe7,d987c720-d044-47d4-b63f-68fcf3e0a49b,685b515e-80d9-427f-8df3-fb3d3ec7256b,07971693-0d6c-4b56-a114-fd2a4eaae6ca,f65504b6-2719-4587-afa7-aa28fa694020,a02e6a62-1660-47c0-a357-27279617d166,ba1db01d-2f18-46de-9dbe-52a6b93464d0,ac5ed3ff-8c9d-4aca-be73-dbad5d5adb69,fb27de58-50e8-40d3-b168-59fd64eadd38,85564f00-d6cb-48c4-877c-0e5668160365,e52639e6-5625-48f5-95d7-6c6304d23bf7,3530baba-88d9-4900-b451-5c6f1a0fdf6b,9fbdcf3b-053d-48e1-8175-2e87a85601ac,cc7bd6ea-7288-44a5-8be2-6f41cdba9d47,4dcef8f2-7107-4f96-8924-fb816ccf3689,aa706fc0-b8f2-4a40-9abf-a8ed6701ca78,bee76e21-9d0d-478b-8a05-4dd77f5c7c7c,d63c4b84-42a9-4c2e-83c1-fe1055523b4d,5c6591c7-6810-49cf-9ba0-4986a442866a,0ac597e5-f11c-4c8f-b557-f808d1f42c0d,4c9e50c7-6594-4e94-8a23-66b61cb093e1,25eeb8dd-9b6a-4df8-8fa3-8d83d9edba10,ef931821-9efd-42dc-a397-279a213d5b7f,668883c8-ed3e-4975-b74f-40ba1b372c13,789e7fab-f3e7-4568-b0b6-bcab0ea8ee2a,f5bb858e-3a12-4759-9718-3b61cad400ab,f05a0618-f603-42e4-92aa-569b5ac62e09,2cf7ca30-2319-4f81-bb25-78a5dec087eb,dc111f6a-ccbd-45fc-9fc6-ef182fef64cd,d0b8140b-87db-486d-bc7b-64a418c05fba,272d1f77-b5d6-46e2-9952-b639065b8d70,5c6d428c-2f7e-480d-b5d7-66ea3dbc559e,58145880-3858-481b-98f1-3a5d1ddc69e9,58b79c2c-ef78-42e6-a77a-ec4d354c4b4b,82a03f91-19b6-4e81-aa18-4e507161978f,ed44c5f4-1641-4ad8-98f3-a710999ed370
"""


@frappe.whitelist(allow_guest=True)
def get_attendance():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 1)
    current_date = start_date

    from_date_str = "2024-01-01T00:00:00Z"
    to_date_str = "2024-01-01T00:00:00Z"

    return fetch_and_process_attendance(from_date_str, to_date_str)
    # frappe.enqueue(
    #     fetch_and_process_attendance,
    #     from_date_str=from_date_str,
    #     to_date_str=to_date_str,
    #     timeout=3600,  # Longer timeout
    # )

    return "Attendance data fetching enqueued."


def fetch_and_process_attendance(from_date_str, to_date_str):
    bearer_token = frappe.get_value(
        "Dhwani KEKA Settings", "Dhwani KEKA Settings", "access_token"
    )
    """Fetches attendance data from Keka and enqueues processing for each page."""
    # while True:
    url = f"https://dhwaniris.keka.com/api/v1/time/attendance?from={from_date_str}&to={to_date_str}&pageNumber=1&pageSize=200&employeeIds={EMPLOYEE_IDS}"

    try:
        response = get_data(url, bearer_token)
        return response
    except requests.exceptions.RequestException as e:
        frappe.log_error(f"API Request Error: {str(e)}")
        return

        # if response.get("exception"):
        #     frappe.log_error(f"Keka API Error: {str(response.get('exception'))}")
        #     return

        # if not response.get("data"):  # Stop if no data on current page
        #     break

        # frappe.enqueue(process_attendance, response=response, timeout=600)

        # page_number += 1  # Move to the next page


def get_data(url, bearer_token):
    payload = {}
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {str(bearer_token)}",
    }

    try:
        response = requests.request(
            "GET", url, headers=headers, data=payload, timeout=10
        )
        response.raise_for_status()
        frappe.logger("utils").exception(response.text)
        return response.json()

    except requests.exceptions.RequestException as e:
        frappe.log_error(f"API Request Error: {str(e)}")


def process_attendance(response):
    shift_start = dt_time(10, 0, 0)  # 10:00 AM
    shift_end = dt_time(19, 0, 0)
    for attendance_data in response.get("data"):
        if frappe.db.exists(
            "Attendance",
            {
                "attendance_date": attendance_data.get("attendanceDate"),
                "employee": attendance_data.get("employeeNumber"),
            },
        ):
            frappe.logger("att_log").exception(
                f"Attendance Marked For Employee {attendance_data.get('employeeNumber')} and date {attendance_data.get('attendanceDate')}"
            )
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
