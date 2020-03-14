

def get_user(user_id, flag):
    from application.views.user_view import GetUserView
    return GetUserView(locals()).as_view()


def delete_user(user_id, flag):
    from application.views.user_view import DeleteUserView
    return DeleteUserView(locals()).as_view()

def modify_user(body):
    from application.views.user_view import ModifyUserView
    return ModifyUserView(locals()).as_view()

def add_user(body):
    from application.views.user_view import AddUserView
    return AddUserView(locals()).as_view()