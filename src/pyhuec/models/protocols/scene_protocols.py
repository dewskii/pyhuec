"""
Protocol definitions for Scene operations.
These protocols define the interface contracts for scene repositories and services.
"""

from typing import List, Optional, Protocol
from pyhuec.models.dto import (
    SceneResponseDTO,
    SceneCreateDTO,
    SceneUpdateDTO,
    SceneRecallDTO,
    SceneListResponseDTO,
    SceneCreateResponseDTO,
    SceneUpdateResponseDTO,
    SceneDeleteResponseDTO,
    ResourceIdentifierDTO,
)


class SceneRepositoryProtocol(Protocol):
    """Protocol for Scene data access operations."""
    
    async def get_scene(self, scene_id: str) -> SceneResponseDTO:
        """
        Retrieve a single scene by ID.
        
        Args:
            scene_id: UUID of the scene
            
        Returns:
            SceneResponseDTO with scene details
        """
        ...
    
    async def get_scenes(self) -> SceneListResponseDTO:
        """
        Retrieve all scenes.
        
        Returns:
            SceneListResponseDTO with list of all scenes
        """
        ...
    
    async def create_scene(self, create: SceneCreateDTO) -> SceneCreateResponseDTO:
        """
        Create a new scene.
        
        Args:
            create: SceneCreateDTO with scene configuration
            
        Returns:
            SceneCreateResponseDTO with created scene ID
        """
        ...
    
    async def update_scene(
        self, 
        scene_id: str, 
        update: SceneUpdateDTO
    ) -> SceneUpdateResponseDTO:
        """
        Update a scene's configuration.
        
        Args:
            scene_id: UUID of the scene
            update: SceneUpdateDTO with desired changes
            
        Returns:
            SceneUpdateResponseDTO with confirmation
        """
        ...
    
    async def recall_scene(
        self, 
        scene_id: str, 
        recall: SceneRecallDTO
    ) -> SceneUpdateResponseDTO:
        """
        Activate/recall a scene.
        
        Args:
            scene_id: UUID of the scene
            recall: SceneRecallDTO with recall parameters
            
        Returns:
            SceneUpdateResponseDTO with confirmation
        """
        ...
    
    async def delete_scene(self, scene_id: str) -> SceneDeleteResponseDTO:
        """
        Delete a scene.
        
        Args:
            scene_id: UUID of the scene
            
        Returns:
            SceneDeleteResponseDTO with confirmation
        """
        ...


class SceneServiceProtocol(Protocol):
    """Protocol for Scene business logic operations."""
    
    async def activate_scene(
        self, 
        scene_id: str, 
        duration: Optional[int] = None
    ) -> bool:
        """
        Activate a scene.
        
        Args:
            scene_id: UUID of the scene
            duration: Optional transition duration in milliseconds
            
        Returns:
            True if successful
        """
        ...
    
    async def create_scene(
        self,
        name: str,
        room_id: str,
        actions: List[dict],
    ) -> str:
        """
        Create a new scene.
        
        Args:
            name: Scene name
            room_id: UUID of the room/zone
            actions: List of light actions
            
        Returns:
            UUID of created scene
        """
        ...
    
    async def update_scene_name(self, scene_id: str, name: str) -> bool:
        """
        Rename a scene.
        
        Args:
            scene_id: UUID of the scene
            name: New scene name
            
        Returns:
            True if successful
        """
        ...
    
    async def update_scene_actions(
        self, 
        scene_id: str, 
        actions: List[dict]
    ) -> bool:
        """
        Update scene light actions.
        
        Args:
            scene_id: UUID of the scene
            actions: New list of light actions
            
        Returns:
            True if successful
        """
        ...
    
    async def get_scene_info(self, scene_id: str) -> SceneResponseDTO:
        """
        Get detailed scene information.
        
        Args:
            scene_id: UUID of the scene
            
        Returns:
            SceneResponseDTO with complete scene details
        """
        ...
    
    async def list_scenes(self, room_id: Optional[str] = None) -> List[SceneResponseDTO]:
        """
        List all available scenes, optionally filtered by room.
        
        Args:
            room_id: Optional UUID to filter scenes by room
            
        Returns:
            List of SceneResponseDTO
        """
        ...
    
    async def delete_scene(self, scene_id: str) -> bool:
        """
        Delete a scene.
        
        Args:
            scene_id: UUID of the scene
            
        Returns:
            True if successful
        """
        ...
    
    async def recall_dynamic_palette(self, scene_id: str) -> bool:
        """
        Activate scene with dynamic palette mode.
        
        Args:
            scene_id: UUID of the scene
            
        Returns:
            True if successful
        """
        ...


class SceneControllerProtocol(Protocol):
    """Protocol for Scene controller operations (API endpoint handlers)."""
    
    async def handle_get_scene(self, scene_id: str) -> SceneResponseDTO:
        """Handle GET /scene/{id} request."""
        ...
    
    async def handle_get_scenes(self) -> SceneListResponseDTO:
        """Handle GET /scene request."""
        ...
    
    async def handle_create_scene(
        self, 
        create: SceneCreateDTO
    ) -> SceneCreateResponseDTO:
        """Handle POST /scene request."""
        ...
    
    async def handle_update_scene(
        self, 
        scene_id: str, 
        update: SceneUpdateDTO
    ) -> SceneUpdateResponseDTO:
        """Handle PUT /scene/{id} request."""
        ...
    
    async def handle_recall_scene(
        self, 
        scene_id: str, 
        recall: SceneRecallDTO
    ) -> SceneUpdateResponseDTO:
        """Handle PUT /scene/{id}/recall request."""
        ...
    
    async def handle_delete_scene(
        self, 
        scene_id: str
    ) -> SceneDeleteResponseDTO:
        """Handle DELETE /scene/{id} request."""
        ...
