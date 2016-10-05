# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: Odoo Community Association (OCA)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class GithubConnectorConfigSettings(models.TransientModel):
    _name = 'github.connector.config.settings'
    _inherit = 'res.config.settings'

    def _default_company(self):
        return self.env.user.company_id

    company_id = fields.Many2one(
        'res.company', 'Company', required=True, default=_default_company)
    github_max_try = fields.Char(
        related='company_id.github_max_try',
        groups='github_connector.group_github_connector_manager')
    git_code_local_path = fields.Char(
        related='company_id.git_code_local_path',
        groups='github_connector.group_github_connector_manager')
    git_partial_commit = fields.Boolean(
        related='company_id.git_partial_commit',
        groups='github_connector.group_github_connector_manager')

    @api.onchange('company_id')
    def onchange_company_id(self):
        if not self.company_id:
            return
        company_id = self.company_id
        github_max_try = company_id.github_max_try
        git_code_local_path = company_id.git_code_local_path
        git_partial_commit = company_id.git_partial_commit
