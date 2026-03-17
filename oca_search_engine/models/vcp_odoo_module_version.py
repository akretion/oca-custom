# Copyright 2026 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models


class VcpOdooModuleVersion(models.Model):
    _name = "vcp.odoo.module.version"
    _inherit = ["vcp.odoo.module.version", "se.indexable.record"]
    
    def _add_to_oca_search_engine(self):
        self._add_to_index(self.env.ref("oca_search_engine.oca_typesense_index_module"))

    def create(self, vals):
        records = super().create(vals)
        self._add_to_oca_search_engine()
        return records
