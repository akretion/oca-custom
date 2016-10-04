# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: Odoo Community Association (OCA)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    github_login = fields.Char('Github Login')
    github_password = fields.Char('Github Password')
    github_max_try = fields.Char('Github Max Try', default='5')
    git_source_code_local_path = fields.Char('Git Source Code Local Path', default='/tmp/')
    git_partial_commit_during_analyze = fields.Boolean('Git Partial Commit During Analyze', default=True)
