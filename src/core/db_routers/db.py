"""
List of Database class Routers
"""

class ScannersDBRouter:
    """
    A router to control `scanners_db` operations on models in the apis.scanners.*
    applications
    """

    route_app_labels = {
        'apis.scanners.cvescannerv2', 'apis.scanners.dirby', 'apis.scanners.hosts', 'apis.scanners.sslyze',
        'apis.scanners.wafw00f', 'apis.scanners.wapiti', 'apis.scanners.whatweb', 'apis.scanners.scanvus',
        'apis.scanners.screenshot', 'apis.scanners.zap'
    }

    def db_for_read(self, model, **hints):
        """
        Attempts to read apis.scanners.* models go to `scanners_db`
        """
        if model._meta.app_label in self.route_app_labels:
            return 'scanners_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write apis.scanners.* models go to `scanners_db`
        """
        if model._meta.app_label in self.route_app_labels:
            return 'scanners_db'
        return None

    def allow_relations(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the apis.scanners.* apps is involved
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the apis.scanners.* apps only appear in the
        `scanners_db` database
        """
        if app_label in self.route_app_labels:
            return db == 'scanners_db'
        return None


class UsersDBRouter:
    """
    A router to control `users_db` operations on models in the auth, contenttypes,
    and apis.users applications
    """
    route_app_labels = {'auth', 'contenttypes', 'apis.users'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth, contenttypes and apis.users models go to
        `users_db`
        """
        if model._meta.app_label in self.route_app_labels:
            return 'users_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth, contenttypes and apis.users models go to
        `users_db`
        """
        if model._meta.app_label in self.route_app_labels:
            return 'users_db'
        return None

    def allow_relations(self, obj1, obj2, **hints):
        """
        Allow relations if a model in auth, contenttypes and apis.users is
        involved
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth, contenttypes and apis.users apps only appear
        in the `users_db` database
        """
        if app_label in self.route_app_labels:
            return db == 'users_db'
        return None


class VulnerabilitiesDBRouter:
    """
    A router to control `vulnerabilities_db` operations on models in the
    apis.vulnerabilities applications
    """

    route_app_labels = {}

    def db_for_read(self, model, **hints):
        """
        Attempts to read apis.vulnerabilities models go to `vulnerabilities_db`
        """
        if model._meta.app_label in self.route_app_labels:
            return 'vulnerabilities_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write apis.vulnerabilities models go to `vulnerabilities_db`
        """
        if model._meta.app_label in self.route_app_labels:
            return 'vulnerabilities_db'
        return None

    def allow_relations(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the apis.vulnerabilities apps is involved
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the apis.vulnerabilities app only appear in the
        `vulnerabilities_db` database
        """
        if app_label in self.route_app_labels:
            return db == 'vulnerabilities_db'
        return None
