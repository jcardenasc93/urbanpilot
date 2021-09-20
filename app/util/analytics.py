""" This module holds all the analytics tasks """

from collections import Counter, OrderedDict
from flask import Blueprint, current_app
from sqlalchemy import desc
import click

from app.models import CustomerModel, LocationRank, db


analytics = Blueprint("analytics", __name__)


class RankZipcodesAnalytics:
    SOURCE = CustomerModel
    OUTPUT = LocationRank

    @classmethod
    def get_zipcodes_info(cls):
        zipcodes_info = (
            cls.SOURCE.query.with_entities(cls.SOURCE.zipcode, cls.SOURCE.city)
            .filter(cls.SOURCE.city != None)
            .yield_per(1000)
        )
        zipcodes_info = (zipcode for zipcode in zipcodes_info)
        return zipcodes_info

    @classmethod
    def clean_up_rank(cls):
        """Drops entire rows"""
        cls.OUTPUT.query.with_for_update(of=cls.OUTPUT).delete()
        db.session.commit()

    @classmethod
    def update_zipcodes_rank(cls, ranks: OrderedDict):
        """Inserts a new rank with a bulk insert"""
        new_rank = []
        # Clean previous data
        cls.clean_up_rank()
        for k, v in ranks.items():
            zipcode, city, frecuency = k[0], k[1], v
            new_rank.append(dict(zipcode=zipcode, city=city, frecuency=frecuency))

        # Bulk insert
        db.session.bulk_insert_mappings(cls.OUTPUT, new_rank)
        db.session.commit()

    @classmethod
    def get_location_rank(cls, number: int = 1000):
        """Retrieves the first <number> items from LocationRank"""
        return (
            LocationRank.query.order_by(desc(LocationRank.frecuency))
            .limit(number)
            .all()
        )


@analytics.cli.command("rank_zipcodes")
@click.option("--top")
def rank_zipcodes(top=None):
    print("Retrieving data from DB...")
    zipcodes_info = RankZipcodesAnalytics.get_zipcodes_info()
    zipcodes_list = [(zipcode[0], zipcode[1]) for zipcode in zipcodes_info]
    count = Counter(zipcodes_list).most_common()
    print("Updating ranks for each location")
    # Update ranks
    RankZipcodesAnalytics.update_zipcodes_rank(OrderedDict(count))
    print("Done!")
    print("The new rank is:")
    rank_short = RankZipcodesAnalytics.get_location_rank(int(top) if top else None)
    print("\n".join([str(rank) for rank in rank_short]))
