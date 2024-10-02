Find tests in test_valuation_adjustment file which is in the Valuation_Adjustment Doctype and test.py in the Services folder



![Screenshot from 2024-09-13 16-04-23](https://github.com/user-attachments/assets/96a6a58b-69c3-4a92-a4a9-11615e886072)

Valuation adjustment implementation is important as valuation rate may change at some point due to dynamic of the business and you may be required to review the pricess of commodies, I have implemented it through code that allows to adjust the valuation and you can also undo the valuation, and this changes the valuation prices in the following documents:: Item, Bin, Stock Ledger Entry

![Screenshot from 2024-09-13 16-03-44](https://github.com/user-attachments/assets/1ec9585b-759a-450c-9e56-3c0b8d8d5f93)

![Screenshot from 2024-09-13 16-02-03](https://github.com/user-attachments/assets/79ba67bc-4e60-4ab7-9424-a06647feb563)

Implemetation of email sending, coz i did a bit of workflow on material request, where there is store manager that creates the material request and on creation of the material request, the status becomes pending and sends an email to the General manager for approval, when a material request is created it creates a task to for the generaral manager

![Screenshot from 2024-09-13 16-01-13](https://github.com/user-attachments/assets/80b4e1e5-11ba-49b7-8063-cd6880f95641)
touched Role Permission manager a bit. where i created a user and gave him the role profile of the general manager and gave him permission on the Material Request Document, even the store manager was given some permissions, like on the material request he can only create and not ammend/write

![WhatsApp Image 2024-09-13 at 7 40 41 PM](https://github.com/user-attachments/assets/868a2829-7b0f-4679-90c0-49290e81b8b5)

here is a picture of the email i get once the request has been made.

![Screenshot from 2024-09-13 16-00-11](https://github.com/user-attachments/assets/0b0ab6c4-ddff-41d0-a00a-adf951d13fa0)

![Screenshot from 2024-09-13 15-58-59](https://github.com/user-attachments/assets/57547b73-a3e4-480b-8cf8-fee62e01ec6a)

![Screenshot from 2024-09-13 15-58-41](https://github.com/user-attachments/assets/104a7dea-cc6e-4dd8-84f8-3e694e174fee)

![Screenshot from 2024-09-13 15-58-25](https://github.com/user-attachments/assets/551c8b99-ebe8-474e-8dcb-817bab768194)
