

def get_user(user_id, flag):
    from application.views.user_view import GetUserView
    return GetUserView(locals()).as_view()

def get_users():
    from application.views.user_view import GetUsersView
    return GetUsersView(locals()).as_view()

def delete_user(user_id, flag):
    from application.views.user_view import DeleteUserView
    return DeleteUserView(locals()).as_view()

def modify_user(body):
    from application.views.user_view import ModifyUserView
    return ModifyUserView(locals()).as_view()

def modify_user_by_id(user_id,body):
    from application.views.user_view import ModifyUserViewByID
    return ModifyUserViewByID(locals()).as_view()

def add_user(body):
    from application.views.user_view import AddUserView
    return AddUserView(locals()).as_view()

def get_usergroup(usergroup_id, flag):
    from application.views.usergroup_view import GetUserGroupView
    return GetUserGroupView(locals()).as_view()

def get_all_usergroup():
    from application.views.usergroup_view import GetAllUserGroupView
    return GetAllUserGroupView(locals()).as_view()

def modify_usergroup_by_id(usergroup_id, body):
    from application.views.usergroup_view import ModifyUserGroupView
    return ModifyUserGroupView(locals()).as_view()

def delete_usergroup(usergroup_id, flag):
    from application.views.usergroup_view import DeleteUserGroupView
    return DeleteUserGroupView(locals()).as_view()

def add_usergroup(body):
    from application.views.usergroup_view import AddUserGroupView
    return AddUserGroupView(locals()).as_view()

def refill(usergroup_id, flag):
    from application.views.usergroup_view import RefillUserGroupView
    return RefillUserGroupView(locals()).as_view()