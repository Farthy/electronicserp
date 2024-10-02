import frappe
import unittest

class TestValuationAdjustment(unittest.TestCase):
    def setUp(self):
        item_name = "Test Item " + frappe.generate_hash(length=5)
        self.test_item = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_name,
            "item_group": "Products",
            "stock_uom": "Nos",
            "is_sales_item": 1,
            "is_stock_item": 1,
            "valuation_rate": 100.00
        }).insert(ignore_permissions=True)

        print(f"Created test item: {self.test_item.name}")
        self.valuation_adjustment = frappe.get_doc({
            "doctype": "Valuation Adjustment",
            "adjustment_type": "Increase",
            "adjustment_amount": 10.00,
            "valuation_rate": 100.00, 
            "items": [
                {
                    "item_code": self.test_item.name,
                    "valuation_rate": 100.00, 
                    "current_valuation_rate": 100.00,
                    "adjustment_amount": 10.00 
                }
            ]
        })

        print(f"Valuation Adjustment before insert: {self.valuation_adjustment.as_dict()}") 

    def tearDown(self):
        if hasattr(self, 'valuation_adjustment') and self.valuation_adjustment.name:
            if self.valuation_adjustment.docstatus == 1: 
                self.valuation_adjustment.cancel() 
            frappe.delete_doc("Valuation Adjustment", self.valuation_adjustment.name)
        if hasattr(self, 'test_item') and self.test_item:
            self.test_item.disabled = 1
            self.test_item.save()

    def test_before_insert_sets_current_valuation_rate(self):
        self.valuation_adjustment.insert(ignore_permissions=True)
        self.assertEqual(self.valuation_adjustment.adjustment_amount, 10.00)
        self.assertEqual(self.valuation_adjustment.items[0].item_code, self.test_item.name)
        current_valuation_rate = frappe.get_value("Item", self.test_item.name, "valuation_rate")
        self.assertEqual(current_valuation_rate, 100.00)

    def test_on_submit_updates_valuation_rate(self):
        self.test_item = frappe.get_doc({
            "doctype": "Item",
            "item_code": "Test Item5",
            "item_group": "Products",
            "valuation_rate": 100.0, 
        }).insert(ignore_permissions=True)

        self.valuation_adjustment = frappe.get_doc({
            "doctype": "Valuation Adjustment",
            "items": [{
                "item_code": self.test_item.item_code,
                "valuation_rate": 150 
            }]
        })

        self.valuation_adjustment.insert(ignore_permissions=True)
        self.valuation_adjustment.submit()
        item = frappe.get_doc("Item", self.test_item.item_code)
        self.assertEqual(item.valuation_rate, 150) 

    def test_on_cancel_reverts_valuation_rate(self):
        self.valuation_adjustment.insert()
        self.valuation_adjustment.submit()
        self.valuation_adjustment.cancel()
        item = frappe.get_doc("Item", self.test_item.name)
        self.assertEqual(item.valuation_rate, 100)

    def test_on_submit_logs_error_on_failure(self):
        with self.assertRaises(Exception):
            self.valuation_adjustment.items = None 
            self.valuation_adjustment.submit()
