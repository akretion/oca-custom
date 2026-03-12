# Copyright 2026 Akretion (https://www.akretion.com).
# @author Arnaud LAYEC <arnaud.layec@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api

class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "se.indexable.record"]

    def _add_to_oca_search_engine(self):
        """Add *OR* synch fields again, when md5 changes are detected"""
        to_synch = self.filtered(lambda x: x._filter_add_to_oca_search_engine())
        to_synch._add_to_index(self.env.ref("oca_search_engine.oca_typesense_index_module"))
    
    def _filter_add_to_oca_search_engine(self):
        return (
            self.is_integrator
            or self.is_sponsor and self.is_published
        )

    #====== CRUD ======#
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._add_to_oca_search_engine()
        return records

    def write(self, vals):
        # TODO: ALY - 2026-03-11: ne semble finalement pas utile de filtrer par 'sponsor_fields', à retirer
        # sponsor_fields = self._get_sponsor_editable_fields()
        if not self.env.user._is_internal(): # and any(x in vals for x in sponsor_fields):
            self._set_sponsor_to_validate(vals)
        res = super().write(vals)
        self._add_to_oca_search_engine()
        return res

    def _set_sponsor_to_validate(self, vals):
        """When the `res.partner` is modified by the sponsor itself (from
             the portal, through self-service process), its data stop being synched
             and the synch must be manually re-enable, as a review process of the changes,
             from the backend (by any Internal User).
            When modified by an Internal User, this process is skipped.
        """
        self.is_published = False

    # def _get_sponsor_editable_fields(self):
    #     """Fields editable by the sponsor itself"""
    #     return [
    #         "website_description_sponsor",
    #         "website_short_description",
    #         "website_description_why_oca",
    #         "grade_id",
    #     ]
