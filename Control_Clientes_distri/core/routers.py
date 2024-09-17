class CustomDatabaseRouter:
    """
    Router para seleccionar la base de datos en función del atributo de la solicitud.
    """

    def db_for_read(self, model, **hints):
        # Retorna la base de datos en función del atributo de la solicitud
        return hints.get('request', {}).get('_database', 'default')

    def db_for_write(self, model, **hints):
        # Retorna la base de datos en función del atributo de la solicitud
        return hints.get('request', {}).get('_database', 'default')

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
