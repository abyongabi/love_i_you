from models.common_model import StandardResponse
from models.goal_model import CreateGoalRequest
from utils.request_context import get_user_id
from utils.sql_manager import execute


def main(request: CreateGoalRequest) -> StandardResponse:
	user_id: int = get_user_id()

	query = 'INSERT INTO "Goal" (title, budget, user_id) VALUES (%s, %s, %s)'
	result, message = execute(query, (request.title, request.budget, user_id))

	return StandardResponse(
		success=result is True,
		message=message,
	)
