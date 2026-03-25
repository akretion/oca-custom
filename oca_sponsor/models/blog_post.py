# Copyright 2026 Akretion (https://www.akretion.com).
# @author Arnaud LAYEC <arnaud.layec@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api

class BlogPost(models.Model):
    """Any modification of a sponsor's blog post needs review"""
    _inherit = ["blog.post"]

    @api.model_create_multi
    def create(self, vals_list):
        self._refresh_sponsor_search_engine()
        return super().create(vals_list)

    def write(self, vals):
        self._refresh_sponsor_search_engine()
        return super().write(vals)
