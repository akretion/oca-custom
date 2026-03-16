# Copyright 2026 Akretion (http://www.akretion.com).
# @author Arnaud LAYEC <arnaud.layec@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from ..schemas import Persons

class TestOcaPersonsSearchEngine(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_companies_json_output(self):
        """Test output generation methods: very simple tests,
        just to ensure the code does not throw errors"""
        member = self.env["res.partner"].create([{
            "name": "Happy Member",
            "is_company": False,
            "country_id": self.env.ref("base.fr").id,
            "free_member": True,
            "is_published": True,
        }])
        self.assertEqual(member.membership_state, "free")
        data = Persons.from_record(member).model_dump(mode="json")

        # Test a few data
        member = self.env.ref("membership_extension.membership_category_member")
        self.assertEqual(data["country"]["code"], "FR")
        self.assertEqual(
            data["roles"],
            member.read(["name"])
        )
