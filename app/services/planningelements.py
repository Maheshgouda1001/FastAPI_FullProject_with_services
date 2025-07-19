from sqlalchemy import select
from sqlalchemy.orm import Session
from collections import defaultdict
from app.schema.authenticate import RolesOut, JWTUserDetails, AllPlansOut, PlanItems
from app.model.authenticate import User
from app.model.userroles import UserRoles
from app.model.userrolemapping import UserRoleMapping
from app.model.planningelement import PlanningElements
from app.model.planrolemapping import PlanRoleMapping
from app.model.userplanmapping import UserPlanMapping

async def get_user_roles(user: JWTUserDetails, db: Session):
    try:
        db_user = db.query(User).filter(User.cwid == user.cwid).first()
        if not db_user:
            raise ValueError("User not found")
        roles = (
            db.query(UserRoles.role)
            .join(UserRoleMapping, UserRoles.id == UserRoleMapping.role_id)
            .filter(UserRoleMapping.user_id == db_user.id)
            .all()
        )
        role_names = [r.role for r in roles]
        return RolesOut(roles=role_names)
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error fetching user roles: {e}")

def get_plans(user: JWTUserDetails, db: Session):
    try:
        user_record = db.query(User.id).filter(User.cwid == user.cwid).first()
        if not user_record:
            raise ValueError("User not found")
        user_id = user_record.id
        role_ids_subquery = (
            select(UserRoleMapping.role_id)
            .filter(UserRoleMapping.user_id == user_id)
            .subquery()
        )
        default_query = (
            db.query(
                UserRoles.role.label("role"),
                PlanningElements.plan.label("plan"),
                PlanRoleMapping.editable.label("editable"),
                PlanningElements.opening_date.label("opening_date"),
                PlanningElements.closing_date.label("closing_date")
            )
            .join(PlanRoleMapping, PlanRoleMapping.role_id == UserRoles.id)
            .join(PlanningElements, PlanningElements.id == PlanRoleMapping.plan_id)
            .filter(PlanRoleMapping.role_id.in_(role_ids_subquery))
        )
        user_query = (
            db.query(
                UserRoles.role.label("role"),
                PlanningElements.plan.label("plan"),
                UserPlanMapping.editable.label("editable"),
                PlanningElements.opening_date.label("opening_date"),
                PlanningElements.closing_date.label("closing_date")
            )
            .join(UserPlanMapping, UserPlanMapping.role_id == UserRoles.id)
            .join(PlanningElements, PlanningElements.id == UserPlanMapping.plan_id)
            .filter(UserPlanMapping.role_id.in_(role_ids_subquery), UserPlanMapping.user_id == user_id)
        )
        union_query = default_query.union_all(user_query)
        results = union_query.all()
        return build_grouped_plan_response(results)
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error fetching planning elements: {e}")

def get_all_plans(user: JWTUserDetails, db: Session):
    try:
        all_plans = db.query(PlanningElements.id, PlanningElements.plan).all()
        plans = [PlanItems(id=plan[0], plan=plan[1]) for plan in all_plans]
        return AllPlansOut(plans=plans)
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error fetching all plans: {e}")

def build_grouped_plan_response(results):
    grouped = defaultdict(list)
    for item in results:
        grouped[item.role].append({
            "plan": item.plan,
            "role": item.role,
            "editable": item.editable,
            "opening_date": item.opening_date,
            "closing_date": item.closing_date
        })
    return {"plan": dict(grouped)}
