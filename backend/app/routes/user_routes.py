from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db, User, SavedRoute
from app.auth import get_current_user

router = APIRouter(prefix="/api/user", tags=["user"])


class SavedRouteCreate(BaseModel):
    name: str
    description: str = ""
    route_data: dict
    conservation_impact: dict = {}
    enrichment: dict = {}


class SavedRouteResponse(BaseModel):
    id: int
    name: str
    description: str
    route_data: dict
    conservation_impact: dict
    enrichment: dict
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


@router.post("/routes", response_model=SavedRouteResponse)
async def save_route(
    route: SavedRouteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Save a route for the current user."""
    saved_route = SavedRoute(
        user_id=current_user.id,
        name=route.name,
        description=route.description,
        route_data=route.route_data,
        conservation_impact=route.conservation_impact,
        enrichment=route.enrichment,
    )
    db.add(saved_route)
    db.commit()
    db.refresh(saved_route)
    return saved_route


@router.get("/routes", response_model=List[SavedRouteResponse])
async def list_routes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all saved routes for the current user."""
    routes = db.query(SavedRoute).filter(SavedRoute.user_id == current_user.id).all()
    return routes


@router.get("/routes/{route_id}", response_model=SavedRouteResponse)
async def get_route(
    route_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific saved route."""
    route = db.query(SavedRoute).filter(
        SavedRoute.id == route_id,
        SavedRoute.user_id == current_user.id,
    ).first()
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found",
        )
    return route


@router.put("/routes/{route_id}", response_model=SavedRouteResponse)
async def update_route(
    route_id: int,
    route_update: SavedRouteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a saved route."""
    route = db.query(SavedRoute).filter(
        SavedRoute.id == route_id,
        SavedRoute.user_id == current_user.id,
    ).first()
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found",
        )

    route.name = route_update.name
    route.description = route_update.description
    route.route_data = route_update.route_data
    route.conservation_impact = route_update.conservation_impact
    route.enrichment = route_update.enrichment
    db.commit()
    db.refresh(route)
    return route


@router.delete("/routes/{route_id}")
async def delete_route(
    route_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a saved route."""
    route = db.query(SavedRoute).filter(
        SavedRoute.id == route_id,
        SavedRoute.user_id == current_user.id,
    ).first()
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found",
        )

    db.delete(route)
    db.commit()
    return {"message": "Route deleted"}
