# Copyright 2026 AKRETION
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from ...oca_search_engine.tools.res_partner_serializer import CompaniesSerializer


class SeIndex(models.Model):
    _inherit = ["se.index"]

    serializer_type = fields.Selection(
        selection_add=[
        ],
        ondelete={
        },
    )

    @api.constrains("model_id", "serializer_type")
    def _check_model(self):
        partner_model = 
        for se_index in self:
            if (
                se_index.serializer_type == "companies_exports"
                and se_index.model_id != partner_model
            ):
                raise ValidationError(_("'Serializer Type' must match 'Model'"))

    def _get_serializer(self):
        self.ensure_one()
        if self.serializer_type == "companies_exports":
            return CompaniesSerializer()
        else:
            return super()._get_serializer()
