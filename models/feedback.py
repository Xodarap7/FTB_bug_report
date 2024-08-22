from odoo import fields, models, _

TICKET_TYPES = [
    ("proposual", _("Proposual")),
    ("report", _("Report")),
    ("edit_game", _("Edit Game")),
    ("add_game", _("Add Game")),
]
PROPOSUAL_TYPES = [
    ("improvement", _("Suggestion for improvement")),
    ("bug_report", _("Bug Report")),
]


class FTBFeedback(models.Model):
    _name = "ftb_bug_report.ticket"
    _description = "Ticket"

    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
    ]

    # Common fields
    name = fields.Char(string="Name", compute="_compute_name")

    ticket_code = fields.Char(string="Ticket Code")

    ticket_type = fields.Selection(TICKET_TYPES, string="Ticket Type")

    proposual_type = fields.Selection(
        PROPOSUAL_TYPES,
        string="Proposual Type",
        help="Vision if Ticket Type is Proposual",
    )

    stage_id = fields.Many2one(
        comodel_name="ftb_bug_report.ticket.stage",
        string="Stage",
        default=lambda self: self.env.ref("FTB_bug_report.stage_consideration"),
        tracking=True,
    )

    update_stage_date = fields.Date(string="Date of last status changed")

    author = fields.Char(string="Author Name")

    description = fields.Char(string="Description")

    # Proposual fields
    bug_link = fields.Char(string="Link on page with bug")

    # Report fields
    user_link = fields.Char(string="Link on user profile")

    # Edit game fields
    game_link = fields.Char(string="Link on Game")

    # Add game fields
    bgg_link = fields.Char(string="BGG Link")

    hg_link = fields.Char(string="HG Link")

    def to_consideration_button(self):
        new_stage = self.env.ref("FTB_bug_report.stage_consideration")
        self._change_stage(new_stage)

    def to_work_button(self):
        new_stage = self.env.ref("FTB_bug_report.stage_in_progress")
        self._change_stage(new_stage)

    def to_done_button(self):
        new_stage = self.env.ref("FTB_bug_report.stage_done")
        self._change_stage(new_stage)

    def to_rejected_button(self):
        new_stage = self.env.ref("FTB_bug_report.stage_rejected")
        self._change_stage(new_stage)

    def _change_stage(self, stage):
        self.stage_id = stage
        self.update_stage_date = fields.Date.today()

    def _compute_name(self):
        for rec in self:
            description = (
                ""
                if not rec.description
                else rec.description[:20]
                if len(rec.description) > 20
                else rec.description
            )
            rec.name = f"[{rec.ticket_code}] {dict(self._fields['ticket_type'].selection).get(rec.ticket_type) or ''}-{description+'...'}"


class FTBFeedbackTicket(models.Model):
    _name = "ftb_bug_report.ticket.stage"
    _description = "Ticket stage"

    name = fields.Char(
        string="Name",
    )
