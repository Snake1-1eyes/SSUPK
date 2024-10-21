# db_router.py
class VmhDbRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'vmh':
            return 'vmh_mgerm'
        return 'default'
