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
        'res.company', 'Company', required=True, default=_default_company
    )
    github_login = fields.Char(related='company_id.github_login')
    github_password = fields.Char(related='company_id.github_password')
    github_max_try = fields.Char(related='company_id.github_max_try', default='5')
    git_source_code_local_path = fields.Char(related='company_id.git_source_code_local_path', default='/tmp/')
    git_partial_commit_during_analyze = fields.Boolean(related='company_id.git_partial_commit_during_analyze', default=True)

    @api.onchange('company_id')
    def onchange_company_id(self):
        if not self.company_id:
            return
        company_id = self.company_id
        github_login = company_id.github_login
        github_password = company_id.github_password
        github_max_try = company_id.github_max_try
        git_source_code_local_path = company_id.git_source_code_local_path
        git_partial_commit_during_analyze = company_id.git_partial_commit_during_analyze
