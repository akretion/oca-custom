# Copyright 2026 Akretion (https://www.akretion.com).
# @author Arnaud LAYEC <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class VcpRepositoryBranch(models.Model):
    _inherit = ["vcp.repository.branch"]

    # name = fields.Char(string="Name")
    # member_ids = fields.Many2many(
    #     comodel_name="res.partner",
    #     relation="github_psc_member_rel",
    #     column1="psc_id",
    #     column2="member_id",
    # )
    # representative_member_ids = fields.Many2many(
    #     comodel_name="res.partner",
    #     relation="github_psc_representative_member_rel",
    #     column1="psc_id",
    #     column2="representative_member_id",
    # )

    def _download_code(self):
        """Fill in PSC when updating sources of https://github.com/OCA/repo-maintainer-conf"""
        res = super()._download_code()
        if not self._is_repo_maitainer_conf():
            return res
        
    def _is_repo_maitainer_conf(self):
        return self.repository_id.name == "repo-maintainer-conf"
