from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status

from models.mission_model import CreateMissionRequest
from utils.request_context import get_user_id
from utils.sql_manager import execute


def split_contribution(request: CreateMissionRequest) -> list[dict]:
	validate_percentages(request)
	mission_pay = Decimal(str(request.pay))
	lines: list[dict] = []

	for payer in request.pay_by:
		for project in request.contribution:
			amount = (
				mission_pay
				* Decimal(payer.pay_percentage)
				* Decimal(project.contribute_percentage)
				/ Decimal(10000)
			).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

			lines.append({
				"pay_by": payer.pay_by,
				"pay_percentage": payer.pay_percentage,
				"contribute_to": project.contribute_to,
				"contribute_percentage": project.contribute_percentage,
				"amount": amount,
			})

	return lines


def main(request: CreateMissionRequest) -> list[dict]:
	user_id = get_user_id()
	if user_id is None:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Authentication is required",
			headers={"WWW-Authenticate": "Bearer"},
		)

	lines = [
		{"user_id": user_id, **line}
		for line in split_contribution(request)
	]
	placeholders = ", ".join(["(%s, %s, %s, %s, %s, %s, %s, %s, %s)"] * len(lines))
	query = (
		'INSERT INTO "Mission" '
		'(title, pay, user_id, pay_by, pay_percentage, contribute_to, '
		'contribute_percentage, amount, requires_audit) VALUES '
		f"{placeholders}"
	)
	params = tuple(
		value
		for line in lines
		for value in (
			request.title,
			request.pay,
			line["user_id"],
			line["pay_by"],
			line["pay_percentage"],
			line["contribute_to"],
			line["contribute_percentage"],
			line["amount"],
			request.requires_audit,
		)
	)
	result, message = execute(query, params)
	if result is not True:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=message or "Unable to save mission contributions",
		)

	return lines


def validate_percentages(request: CreateMissionRequest) -> None:
	if not request.pay_by or not request.contribution:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail="pay_by and contribution must each contain at least one item",
		)

	if any(item.pay_percentage < 0 or item.pay_percentage > 100 for item in request.pay_by):
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail="pay_percentage must be between 0 and 100",
		)

	if any(item.contribute_percentage < 0 or item.contribute_percentage > 100 for item in request.contribution):
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail="contribute_percentage must be between 0 and 100",
		)

	if sum(item.pay_percentage for item in request.pay_by) != 100:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail="pay_percentage values must total 100",
		)

	if sum(item.contribute_percentage for item in request.contribution) != 100:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail="contribute_percentage values must total 100",
		)
from models.common_model import StandardResponse
