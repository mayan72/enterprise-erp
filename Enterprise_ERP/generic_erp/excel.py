import pandas as pd
from datetime import date

# ---------- PRODUCTS ----------
products_df = pd.DataFrame([
    {
        "Product Code": "Groc-P-001",
        "Product Name": "Suger",
        "Category": "Grocery item",
        "Unit Price": 2.50,
        "GST %": 5,
        "Active": "Yes"
    },
    {
        "Product Code": "Groc-P-002",
        "Product Name": "Dal",
        "Category": "Grocery item",
        "Unit Price": 6.00,
        "GST %": 12,
        "Active": "Yes"
    },
])

products_df.to_excel("medical_products.xlsx", index=False)


# # ---------- STOCK ----------
# stock_df = pd.DataFrame([
#     {
#         "Product Code": "MED-P-001",
#         "Product Name": "Paracetamol 500mg",
#         "Batch No": "BATCH-21",
#         "Expiry Date": "2026-06-30",
#         "Quantity": 500,
#         "Purchase Price": 1.80,
#         "Supplier Name": "Apollo Distributors"
#     },
#     {
#         "Product Code": "MED-P-002",
#         "Product Name": "Amoxicillin 250mg",
#         "Batch No": "BATCH-34",
#         "Expiry Date": "2025-12-31",
#         "Quantity": 300,
#         "Purchase Price": 4.50,
#         "Supplier Name": "MedPlus Suppliers"
#     },
# ])

# stock_df.to_excel("medical_stock.xlsx", index=False)


# # ---------- BILLING ----------
# billing_df = pd.DataFrame([
#     {
#         "Bill No": "B-1001",
#         "Bill Date": date.today().isoformat(),
#         "Patient Name": "Ravi Kumar",
#         "Product Name": "Paracetamol 500mg",
#         "Quantity": 10,
#         "Unit Price": 2.50,
#         "Amount": 25.00,
#         "Payment Mode": "Cash"
#     },
#     {
#         "Bill No": "B-1002",
#         "Bill Date": date.today().isoformat(),
#         "Patient Name": "Anita Sharma",
#         "Product Name": "Amoxicillin 250mg",
#         "Quantity": 5,
#         "Unit Price": 6.00,
#         "Amount": 30.00,
#         "Payment Mode": "UPI"
#     },
# ])

# billing_df.to_excel("medical_billing.xlsx", index=False)

print("Excel files created successfully:")
print("- medical_products.xlsx")
# print("- medical_stock.xlsx")
# print("- medical_billing.xlsx")
