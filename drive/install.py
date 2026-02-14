import frappe


def after_install():
    """Safe after_install — tables may not exist until migrate runs."""
    _create_fts_index()


def after_migrate():
    """Re-run after every migrate to ensure index exists."""
    _create_fts_index()


def _create_fts_index():
    try:
        # Guard: table must exist before we touch it
        if not frappe.db.table_exists("Drive File"):
            return

        index_check = frappe.db.sql(
            """SHOW INDEX FROM `tabDrive File`
               WHERE Key_name = 'drive_file_title_fts_idx'"""
        )
        if not index_check:
            frappe.db.sql(
                """ALTER TABLE `tabDrive File`
                   ADD FULLTEXT INDEX `drive_file_title_fts_idx` (title)"""
            )
            frappe.db.commit()
    except Exception:
        # Never block install/migrate for an index
        pass