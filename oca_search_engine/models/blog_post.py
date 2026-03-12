# Copyright 2026 Akretion (https://www.akretion.com).
# @author Arnaud LAYEC <arnaud.layec@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api

class BlogPost(models.Model):
    _inherit = ["blog.post"]

    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)._refresh_sponsor_search_engine()

    def write(self, vals):
        res = super().write(vals)
        self._refresh_sponsor_search_engine()
        return res
    
    def _refresh_sponsor_search_engine(self):
        self.author_id._add_to_oca_search_engine()
        return self
