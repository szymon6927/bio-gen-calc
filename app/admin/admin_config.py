import flask_admin as admin
from flask_admin.contrib.sqla import ModelView

# Customized admin interface
class CustomView(ModelView):
    list_template = 'list.html'
    create_template = 'create.html'
    edit_template = 'edit.html'


class UserAdmin(CustomView):
    column_searchable_list = ('name',)
    column_filters = ('name', 'email')



def create_admin_interface():
    # Create admin interface
    admin_interface = admin.Admin(name="Gene-Calc", base_template='layout.html', template_mode='bootstrap3')
    admin_interface.add_view(UserAdmin(User, db.session))
    admin_interface.add_view(CustomView(Page, db.session))

    return admin_interface


