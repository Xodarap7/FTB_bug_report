# -*- coding: utf-8 -*-
{
    "name": "FTB_bug_report",
    "summary": "Module for users feedback",
    "description": "",
    "author": "FTB",
    "website": "https://fliptheboard.ru",
    "category": "Customer Relationship Management",
    "version": "1.0",
    "depends": ["base", "mail"],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "data/stages_data.xml",
        "views/feedback_views.xml"
    ],
}
