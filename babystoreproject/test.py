items = [ 
    {"department": "Back to School", "name":  "water bottle", "price": 1000, "quantity": 5},
    {"department": "Back to School", "name":  "backpack", "price": "6000", "brand": "Nike", "quantity": 5},
    {"department": "Toys", "name":  "backpack", "price": "6000", "brand": "Nike", "quantity": 5},
]

departments = []
for item in items:
    for department in item['department']:
        departments.append(department)

for department in departments:
    print(department)

print(departments)