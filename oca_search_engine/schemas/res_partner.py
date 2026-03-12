# Copyright 2026 AKRETION
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from __future__ import annotations

from extendable_pydantic import StrictExtendableBaseModel

class CommonResPartner(StrictExtendableBaseModel):
    id: int
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    is_published: bool

    @classmethod
    def from_record(cls, record):
        return cls.model_construct(
            id=record.id,
            name=record.name or None,
            email=record.email or None,
            phone=record.phone or None,
        )

class Companies(CommonResPartner):
    # editable fields
    website: str | None = None
    is_integrator: bool | None = None
    countries: list[dict(code:str, label:str)]
    logo_urls: dict(alt:str, l:str, m:str, s:str)
    # github indicators
    contributors_count: int | None = None
    contributors_index: int | None = None
    members_count: int | None = None
    modules_count: int | None = None
    # technical website fields
    url_key: str | None = None
    redirect_url_key: list[str] | None = None
    # sponsorship
    sponsorship: dict(
        "description_long": str,
        "description_short": str,
        "description_why_oca": str,
        "level": dict(
            "id": int,
            "rank": int,
            "name": str
        ),
        "industries": list[
            dict(
                "description": str,
                "name": str
            )
        ],
        "stories": dict(
            "title": str
            "teaser": str
            "relative_url": str,
            "cover_url": str,
        ),
    )

    @classmethod
    def from_record(cls, record):
        res = super().from_record(record)
        return res | cls.model_construct(
            # editable fields
            website=record.website or None,
            is_integrator=record.is_integrator or None,
            countries=[
                {"code": x["code"], "label": x["name"]}
                for x in record.website_country_ids.read(["code", "name"])
            ],
            logo_urls={
                "alt": record.name,
                "l": record._get_avatar_url(size=1920),
                "m": record._get_avatar_url(size=512),
                "s": record._get_avatar_url(size=128)
            },
            # github indicators
            contributors_count=record.contributors_count or None,
            contributors_index=record.contributors_index or None,
            members_count=record.members_count or None,
            modules_count=record.modules_count or None,
            # technical website fields
            url_key=record._get_slug() or None,
            redirect_url_key=record.slug_history_ids.mapped("name") or None,
            # sponsorship
            sponsorship={
                "description_long": record.website_description_sponsor,
                "description_short": record.website_short_description,
                "description_why_oca": record.website_description_why_oca,
                "level": {
                    "id": record.grade_id.id,
                    "name": record.grade_id.name,
                    "name": record.grade_id.sequence,
                },
                "industries": [
                    {
                        "name": industry["name"],
                        "description": industry["description"]
                    }
                    for industry in record.website_industry_ids.read(["name", "description"])
                ],
                "stories": [
                    {
                        "title": blog_post.name,
                        "teaser": blog_post.teaser,
                        "relative_url": blog_post.website_url,
                        "cover_url": blog_post._get_background_url(), # can also pass 'height' and 'width'
                    }
                    for blog_post in record.blog_post_ids
                ],
            }
        )
