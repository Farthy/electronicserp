# Copyright (c) 2024, farthy and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ValuationAdjustment(Document):
	def before_insert(self):
		for item in self.items:
			item_code = item.item_code
			valuation_rate = frappe.db.get_value("Item", {"name": item_code}, "valuation_rate")
			if valuation_rate:
				item.current_valuation_rate = valuation_rate

	def on_submit(self):
		try:
			for item in self.items:
				item_code = item.item_code
				new_valuation_rate = item.valuation_rate
				valuation_rate_adjustment_docs = frappe.db.get_all("Valuation Rate Adjustment Document", fields=["name"])
				for doc in valuation_rate_adjustment_docs:
					doctype_name = doc['name']

					records_to_update = frappe.db.get_all(doctype_name, filters={"item_code": item_code}, fields=["name"])
					for record in records_to_update:
						doc_to_update = frappe.get_doc(doctype_name, record['name'])
						if hasattr(doc_to_update, "valuation_rate"):
							doc_to_update.valuation_rate = new_valuation_rate
							doc_to_update.db_update()

			frappe.db.commit()
			return {"message": "Valuation rates updated for all items successfully."}
		except Exception as e:
			frappe.log_error(message=str(e), title="Valuation Rate Adjustment Error")
			return {"error": "An error occurred during the valuation rate update process. Please check the error log for details."}

	def on_cancel(self):
		try:
			for item in self.items:
				item_code = item.item_code
				new_valuation_rate = item.current_valuation_rate
				valuation_rate_adjustment_docs = frappe.db.get_all("Valuation Rate Adjustment Document", fields=["name"])
				
				for doc in valuation_rate_adjustment_docs:
					doctype_name = doc['name']
			
					records_to_update = frappe.db.get_all(doctype_name, filters={"item_code": item_code}, fields=["name"])
					for record in records_to_update:
						doc_to_update = frappe.get_doc(doctype_name, record['name'])
						if hasattr(doc_to_update, "valuation_rate"):
							doc_to_update.valuation_rate = new_valuation_rate
							doc_to_update.db_update()

			frappe.db.commit()
			return {"message": "Valuation rates reverted to current valuation rate for all items successfully."}
		except Exception as e:
			frappe.log_error(message=str(e), title="Valuation Rate Revert Error")
			return {"error": "An error occurred during the valuation rate revert process. Please check the error log for details."}

	
			



