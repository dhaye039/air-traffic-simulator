from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

# Custom permissions
content_type = ContentType.objects.get_for_model(Permission)
canInsertData = Permission.objects.create(
    codename='canInsertData',
    name='Can Insert Data',
    content_type=content_type,
)
canDeleteData = Permission.objects.create(
    codename='canDeleteData',
    name='Can Delete Data',
    content_type=content_type,
)

# # Create a new user group for inserting data
# group1 = Group.objects.create(name='InsertPrivilegeUsers')
# # Add custom permissions to the group
# group1.permissions.add(canInsertData)
# # give permissions to every group member
# permission = Permission.objects.get(codename='canInsertData')
# for user in group1.user_set.all():
#     user.user_permissions.add(permission)

# # Create a new user group for deleting data
# group2 = Group.objects.create(name='DeletePrivilegeUsers')
# # Add custom permissions to the group
# group2.permissions.add(canInsertData)
# # give permissions to every group member
# permission = Permission.objects.get(codename='canDeleteData')
# for user in group2.user_set.all():
#     user.user_permissions.add(permission)