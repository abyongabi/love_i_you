import logging

from models.common_model import StandardResponse
from models.mission_model import CreateMissionRequest
from utils.request_context import get_user_id
from utils.sql_manager import execute


def main(request: CreateMissionRequest) -> StandardResponse:
	user_id: int = get_user_id()

	mission_id: int = create_mission(request, user_id)

	contributions: list = calculate_contributions(request, mission_id)

	return StandardResponse(success=create_contributions(contributions))


def create_mission(request: CreateMissionRequest, user_id: int) -> int:
	query = 'INSERT INTO "Mission" (title, pay, user_id, active) VALUES (%s, %s, %s, %s) RETURNING id'
	result, _ = execute(query, (request.title, request.pay, user_id, True))
	if len(result) > 0:
		logging.info(f"Successfullt created mission {request.title} with id {result[0]}")
		return result[0]
	raise ValueError


def calculate_contributions(request: CreateMissionRequest, mission_id: int) -> list:
	contributions: list = []

	for pay_by in request.pay_by:
		for contribution in request.contribution:
			contributions.append({
				"mission_id": mission_id,
				"contribute_to": contribution.contribute_to,
				"pay_by": pay_by.pay_by,
				"pay_amount": (request.pay * contribution.contribute_percentage * pay_by.pay_percentage) / 1_00_00
			})

	return contributions


def create_contributions(contributions: list) -> bool:
	insert_count: int = 0

	query = 'INSERT INTO "Contribution" (mission_id, pay_by, contribute_to, pay_amount) VALUES (%s, %s, %s, %s) RETURNING id'
	for contribution in contributions:
		result, _ = execute(query, (contribution["mission_id"], contribution["pay_by"], contribution["contribute_to"], contribution["pay_amount"]))
		if len(result) > 0:
			logging.info(f"Successfully created contribution record for {contribution["pay_by"]} for mission {contribution["mission_id"]}")
			insert_count += 1

	return insert_count == len(contributions)
