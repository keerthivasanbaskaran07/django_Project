from django.contrib.auth.models import Group, Permission

def create_group_permissions(sender, **kwargs):
    try:
        #create groups
        readers_group,created = Group.objects.get_or_create(name="Readers")
        Authors_group,created = Group.objects.get_or_create(name="Authors")
        editors_group,created = Group.objects.get_or_create(name="Editors")


        # create Permissions
        readers_permissions = [
            Permission.objects.get(codename = "view_post")
        ]

        authors_permissions = [
            Permission.objects.get(codename = "view_post"),
            Permission.objects.get(codename = "add_post"),
            Permission.objects.get(codename = "change_post"),
            Permission.objects.get(codename = "delete_post"),
        ]

        
        can_published,created = Permission.objects.get_or_create(codename = "can_publish",content_type_id = 9, name="can publish post")
        editors_permissions = [
            can_published,
            Permission.objects.get(codename = "view_post"),
            Permission.objects.get(codename = "add_post"),
            Permission.objects.get(codename = "change_post"),
            Permission.objects.get(codename = "delete_post"),
        ]

        # Assigning the permission to group
        readers_group.permissions.set(readers_permissions)
        Authors_group.permissions.set(authors_permissions)
        editors_group.permissions.set(editors_permissions)
        print("Groups and Permmision Create Successfully")
    except Exception as e:
        print(f"An Error Accured {e}")

    