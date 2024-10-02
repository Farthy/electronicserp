import frappe
import unittest
from unittest.mock import patch, ANY  # Import ANY from unittest.mock

class TestYourModule(unittest.TestCase):

    # Test case for get_users_details function
    def test_get_users_details(self):
        with patch('frappe.db.get_value') as mock_get_value:
            mock_get_value.return_value = {
                'mobile_no': '123456789',
                'first_name': 'John',
                'email': 'senelwafarthy@gmail.com'
            }

            user_details = frappe.get_attr('electronics.services.rest.get_users_details')('General Manager')

            self.assertEqual(user_details['mobile_no'], '123456789')
            self.assertEqual(user_details['first_name'], 'John')
            self.assertEqual(user_details['email'], 'senelwafarthy@gmail.com')
            mock_get_value.assert_called_once_with('User', {'role_profile_name': 'General Manager'}, ['mobile_no', 'first_name', 'email'], as_dict=True)

    # Test case for create_user_permission function
    def test_create_user_permission(self):
        with patch('frappe.get_doc') as mock_get_doc, patch('frappe.log_error') as mock_log_error, patch('frappe.throw') as mock_throw:
            mock_doc = mock_get_doc.return_value
            mock_doc.insert.return_value = None

            user_permission_name = frappe.get_attr('electronics.services.rest.create_user_permission')('senelwafarthy@gmail.com', 'REF123', 'Task')

            mock_get_doc.assert_called_once_with({
                "doctype": "User Permission",
                "user": 'senelwafarthy@gmail.com',
                "allow": 'Task',
                "for_value": 'REF123'
            })
            mock_throw.assert_not_called()
            mock_log_error.assert_not_called()

    # Test case for create_task function
    def test_create_task(self):
        with patch('frappe.get_doc') as mock_get_doc, patch('frappe.throw') as mock_throw, patch('frappe.log_error') as mock_log_error, patch('frappe.msgprint') as mock_msgprint, patch('electronics.services.rest.create_user_permission') as mock_create_user_permission:
            mock_doc = mock_get_doc.return_value
            mock_doc.name = 'TASK-001'

            task_name = frappe.get_attr('electronics.services.rest.create_task')(
                subject="Test Task",
                priority="Medium",
                description="Test task description",
                assigned_user="senelwafarthy@gmail.com",
                reference_no="REF123",
                doctype="Material Request"
            )

            mock_get_doc.assert_called_once_with({
                "doctype": "Task",
                "subject": "Test Task",
                "status": "Pending Review",
                "priority": "Medium",
                "description": "Test task description",
                "assigned_user": "senelwafarthy@gmail.com",
                "reference_no": "REF123",
                "reference_document": "Material Request"
            })

            mock_create_user_permission.assert_called_once_with("senelwafarthy@gmail.com", "TASK-001", "Task")
            mock_msgprint.assert_called_once_with("Task Number TASK-001 created successfully.")
            mock_throw.assert_not_called()
            mock_log_error.assert_not_called()

    # Test case for send_email function
    def test_send_email(self):
        with patch('frappe.sendmail') as mock_sendmail:
            frappe.get_attr('electronics.services.rest.send_email')(
                email_address="senelwafarthy@gmail.com",
                body="Test email body",
                subject="Test Email Subject"
            )

            mock_sendmail.assert_called_once_with(
                recipients="senelwafarthy@gmail.com",
                cc='',
                subject="Test Email Subject",
                content="Test email body",
                reference_doctype='',
                reference_name='',
                now=True
            )

    # Test case for create_task_and_notify_manager function
    def test_create_task_and_notify_manager(self):
        with patch('electronics.services.rest.get_users_details') as mock_get_users_details, patch('electronics.services.rest.create_task') as mock_create_task, patch('electronics.services.rest.send_email') as mock_send_email, patch('frappe.throw') as mock_throw:
            mock_get_users_details.return_value = {
                'email': 'senelwafarthy@gmail.com',
                'first_name': 'Jane'
            }
            mock_create_task.return_value = 'TASK-001'

            result = frappe.get_attr('electronics.services.rest.create_task_and_notify_manager')(
                docname="MR-001",
                description="Material Request pending approval"
            )

            self.assertTrue(result)
            mock_get_users_details.assert_called_once_with('General Manager')
            mock_create_task.assert_called_once_with(
                subject="Pending Material Request Approval",
                priority="High",
                description="Material Request pending approval",
                assigned_user="senelwafarthy@gmail.com",
                reference_no="MR-001",
                doctype="Material Request"
            )
            mock_send_email.assert_called_once_with(
                'senelwafarthy@gmail.com',
                ANY,  # Use mock.ANY to match the dynamic email body content
                'Pending Task for Material Request MR-001'
            )
            mock_throw.assert_not_called()

if __name__ == '__main__':
    unittest.main()
