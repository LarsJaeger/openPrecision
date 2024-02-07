from __future__ import annotations

import functools
import uuid
from typing import List
from neomodel import db

from open_precision.core.model.waypoint import Waypoint
from open_precision.core.model.location import Location


@functools.cache
def create_loc_store_node():
	current_uuid = str(uuid.uuid4())
	params = {"uuid": current_uuid}
	db.cypher_query("CREATE (a:Collection {uuid: $uuid})", params)
	return current_uuid


def add_to_location_store(loc: Location, name: str):
	add_to_store(loc, name)


def get_location(name: str) -> List:
	collection = create_loc_store_node()
	query = """MATCH (a:Collection{uuid: $collection})-[c:CONTAINS{name:$name}]->(b) RETURN b"""
	params = {"name": name, "collection": collection}
	results, meta = db.cypher_query(query, params, resolve_objects=True)
	return results


def get_location_names() -> List:
	collection = create_loc_store_node()
	query = (
		"""MATCH (n:Collection {uuid: $collection})-[c:CONTAINS]->(b) RETURN c.name"""
	)
	results, meta = db.cypher_query(
		query, {"collection": collection}, resolve_objects=True
	)
	return [res[0] for res in results]


def delete_from_location_store(name: str):
	remove_from_store(name)


def add_to_store(loc: Location, name: str):
	collection = create_loc_store_node()
	wp = Waypoint(location=loc)
	wp.save()
	results, meta = db.cypher_query(
		"MATCH (a:Collection {uuid: $collection}), (b:Waypoint {uuid: $uuid}) CREATE (a)-[c:CONTAINS{name:$name}]->(b)",
		params={"uuid": wp.uuid, "name": name, "collection": collection},
	)


def remove_from_store(name: str):
	collection = create_loc_store_node()
	results, meta = db.cypher_query(
		"MATCH (a:Collection {uuid: $collection})-[b:CONTAINS]->(c) REMOVE b",
		{"name": name, "collection": collection},
	)
