from unfold.sites import UnfoldAdminSite


class ManagerAdminSite(UnfoldAdminSite):
    site_header = "PERES BONHEUR"
    site_title = "PERES BONHEUR"
    index_title = "PERES BONHEUR"


manager_admin_site = ManagerAdminSite(name="manager")
