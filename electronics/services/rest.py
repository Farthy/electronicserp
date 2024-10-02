import frappe
import csv
import io


@frappe.whitelist()
def get_users_details(role_profile_name):
    user_details = frappe.db.get_value(
        "User",
        {'role_profile_name': role_profile_name},
        ['mobile_no', 'first_name', 'email'],
        as_dict=True
    )

    return user_details
@frappe.whitelist()
def create_user_permission(email, reference_number, doctype):
    try:
        user_permission = frappe.get_doc({
            "doctype": "User Permission",
            "user": email,
            "allow": doctype,
            "for_value": reference_number
        })
        user_permission.insert(ignore_permissions=True)
        return user_permission.name
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "User Permission Creation Error")
        frappe.throw(f"An error occurred while creating the user permission: {str(e)}")


def create_task(subject, priority, description, assigned_user, reference_no, doctype):
    try:
        task = frappe.get_doc({
            "doctype": "Task",
            "subject": subject,
            "status": "Pending Review",
            "priority": priority,
            "description": description,
            "assigned_user": assigned_user,
            "reference_no": reference_no,
            "reference_document": doctype
        })
        task.insert(ignore_permissions=True)
        create_user_permission(assigned_user, task.name, "Task")
        frappe.msgprint(f"Task Number {task.name} created successfully.")
        return task.name
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Task Creation Error")
        frappe.throw(f"An error occurred while creating the task: {str(e)}")

    
def send_email(email_address, body, subject):

    frappe.sendmail(
        recipients = email_address,
        cc = '',
        subject = subject,
        content = body,
        reference_doctype = '',
        reference_name = '',
        now = True
    )

@frappe.whitelist()
def create_task_and_notify_manager(docname, description):

    try:
        user_details = get_users_details('General Manager')
        if not user_details:
            frappe.throw("General Manager not found")

        email = user_details.get('email')
        first_name = user_details.get('first_name')
        task_name = create_task(
            subject="Pending Material Request Approval",
            priority="High",
            description=description,
            assigned_user=email,
            reference_no=docname,
            doctype="Material Request"
        )
        
        if task_name:
            base_url = frappe.utils.get_url()
            task_url = f"{base_url}/app/task/{task_name}"
            subject = f"Pending Task for Material Request {docname}"
            email_message = f"""
                Hello <b>{first_name}</b>, <br/><br/>
                You have a pending material request that needs your approval.<br/>
                <a href="{task_url}">Click here to view the task</a><br/><br/>
                Thank you.
            """
            send_email(email, email_message, subject)
            return True

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error creating task and sending email")
        frappe.throw(f"Error creating task or sending email: {str(e)}")

    return False