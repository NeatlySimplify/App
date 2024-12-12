from app.queries import (
    create_user_async_edgeql,
    createBankAccount_async_edgeql,
    delete_user_async_edgeql,
    deleteBankAccount_async_edgeql,
    update_user_async_edgeql,
    login_user_async_edgeql,
    retrieve_balance_async_edgeql,
    updateBankAccount_async_edgeql
    )


class User:
    create = create_user_async_edgeql.create_user()
    update = update_user_async_edgeql.update_user()
    delete = delete_user_async_edgeql.delete_user()
    retrieveUser = login_user_async_edgeql.login_user()
    retrieveBalance = retrieve_balance_async_edgeql.retrieve_balance()
    createBankAccount = createBankAccount_async_edgeql.createBankAccount()
    deleteBankAccount = deleteBankAccount_async_edgeql.deleteBankAccount()
    updateBankAccount = updateBankAccount_async_edgeql.updateBankAccount()


class Client:
    pass


class Service:
    pass


class Scheduler:
    pass


class Auditable:
    pass


class Templates:
    pass


class Action:
    payment = ''


class Admin:
    pass