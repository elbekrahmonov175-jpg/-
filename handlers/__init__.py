from aiogram import Router


def get_handlers_router() -> Router:
    router = Router()
    
    # Импортируем и подключаем каждый модуль
    from . import start
    from . import income
    from . import expense
    from . import balance
    from . import stats
    from . import history
    from . import debts
    
    router.include_router(start.router)
    router.include_router(income.router)
    router.include_router(expense.router)
    router.include_router(balance.router)
    router.include_router(stats.router)
    router.include_router(history.router)
    router.include_router(debts.router)
    
    return router
