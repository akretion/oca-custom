# Copyright 2026 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


import os
from pathlib import Path

from odoo import models


class VcpRule(models.Model):
    _inherit = "vcp.rule"

    def _process_rule_odoo_module_prepare_vals(
        self, repository_branch, module_id, manifest_path
    ):
        vals = super()._process_rule_odoo_module_prepare_vals(
            repository_branch, module_id, manifest_path
        )
        readme_path = Path(os.path.dirname(manifest_path), "readme")
        vals["readme_fragments"] = {}
        if readme_path.exists():
            for item in readme_path.iterdir():
                vals["readme_fragments"][item.lower().removesuffix(".md")] = (
                    item.read_text()
                )
        return vals
