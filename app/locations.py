""" Views implementation """

from flask import Blueprint, jsonify
from .models import LocationRank
from .schema import RankSchema

# Instance blueprint
rank = Blueprint("rank", __name__)

# Schemas definition
rank_schema = RankSchema(many=True)


@rank.route("/rank", methods=["GET"])
def get_rank():
    rank = LocationRank.query.all()
    response = rank_schema.dump(rank)
    return jsonify(response), 200
