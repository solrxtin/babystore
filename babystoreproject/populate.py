import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'babystoreproject.settings')

import django
django.setup()
from  app.models import Department, Item

items = [ 
    {"name":  "water bottle", "price": 1000, "brand": '', "quantity": 5,},
    {"name":  "backpack", "price": "6000", "brand": "Nike", "quantity": 5},
]
departments = { 
    "Back to School": {"items": items},
}

def populate():
    
    for department_name, department_item in departments.items():
        department = Department.objects.get(name= department_name)    
        department_items  = Item.objects.get_or_create(department=department.id)
        
        for item in department_items:
            i = add_item(department, item['brand'], item['name'], item['price'], item['quantity'] )
    
    
    for department in departments:
        for items in Item.objects.filter(department=department):
            print(f'{str(department)}--{str(items)}')



def add_item(department, brand, name, price, quantity):
    department = department__item
    print(i)
    newly_added_item = Item.objects.create(
        id = department.id,
        department=department,
        name = name,
        price = price, 
        quantity = quantity
    )
    if brand != '':
        newly_added_item.brand = brand
    newly_added_item.save()
    return newly_added_item

if __name__ == '__main__':
    populate()
