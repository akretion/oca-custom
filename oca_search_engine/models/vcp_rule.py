# Copyright 2026 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


import os
from pathlib import Path
import yaml

from odoo import models, fields, _


class VcpRule(models.Model):
    _inherit = ["vcp.rule"]

    rule_type = fields.Selection(
        selection_add=[("oca_psc_update", "Update OCA PSC")],
        ondelete={"oca_psc_update": "cascade"},
    )

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

    def _process_rule_oca_psc_update(self, record):
        """Read Github repo 'OCA/repo-maintainer-conf' and call `vcp.oca.psc`
        to update the data in Odoo.
        In this repo, 2 dirs are read:
        - /conf/psc/*.yml: 1 yml per PSC team, listing the members
        - /conf/repo/*.yml: 1 yml per repo, setting the responsible PSC team
        """
        if record._name != "vcp.repository.branch":
            return
        record._download_code()

        mapped_pscs = {}
        psc_files = self._cloc_get_matches(record.local_path)
        for yml_path in psc_files:
            dirname = os.path.basename(os.path.dirname(yml_path))
            file_path = Path(record.local_path + "/" + yml_path)
            with open(file_path, 'r') as file:
                yml_data = yaml.safe_load(file)
                if not yml_data:
                    continue

                for name, item in yml_data.items():
                    if dirname == "psc":
                        mapped_pscs.setdefault(name, {"repos": {}}).update(item)
                    elif dirname == "repo":
                        mapped_pscs.setdefault(item["psc"], {"repos": {}})["repos"][name] = item["name"]
                        mapped_pscs.setdefault(item["psc_rep"], {"repos": {}})["repos"][name] = item["name"]
                    else:
                        raise NotImplementedError(_("Operation not supported."))

        record.env["vcp.oca.psc"]._update_from_source(record, mapped_pscs)

