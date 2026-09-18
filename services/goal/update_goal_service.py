from models.common_model import StandardResponse
from models.goal_model import UpdateGoalRequest
from utils.sql_manager import execute


def main(request: UpdateGoalRequest) -> StandardResponse:
    priority: int = request.priority
    if priority >= 5:
        priority = 1

    query = '''
        UPDATE "Goal"
        SET priority = %s, active = %s
        WHERE id = %s
    '''

    result, message = execute(
        query,
        (priority, request.active, request.goal_id),
    )

    return StandardResponse(
        success=result is True,
        message=message,
    )
