from __future__ import division  # Use floating point for math calculations

import math

from flask import Blueprint

from CTFd.models import Challenges, Solves, db
from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.challenges import CHALLENGE_CLASSES, BaseChallenge
from CTFd.plugins.migrations import upgrade
from CTFd.utils.modes import get_model

class PenaltyChallenge(Challenges):
    __mapper_args__ = {"polymorphic_identity": "penalty"}
    id = db.Column(
        db.Integer, db.ForeignKey("challenges.id", ondelete="CASCADE"), primary_key=True
    )
    initial = db.Column(db.Integer, default=0)
    minimum = db.Column(db.Integer, default=0)
    penalty = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kwargs):
        super(PenaltyChallenge, self).__init__(**kwargs)
        self.value = kwargs["initial"]

class PenaltyValueChallenge(BaseChallenge):
    id = "penalty"
    name = "penalty"
    templates = {  # Handlebars templates used for each aspect of challenge editing & viewing
        "create": "/plugins/penalty_challenges/assets/create.html",
        "update": "/plugins/penalty_challenges/assets/update.html",
        "view": "/plugins/penalty_challenges/assets/view.html",
    }
    scripts = {  # Scripts that are loaded when a template is loaded
        "create": "/plugins/penalty_challenges/assets/create.js",
        "update": "/plugins/penalty_challenges/assets/update.js",
        "view": "/plugins/penalty_challenges/assets/view.js",
    }
    # Route at which files are accessible. This must be registered using register_plugin_assets_directory()
    route = "/plugins/penalty_challenges/assets/"