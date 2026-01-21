from typing import List, Optional
from pyhuec.models.dto.scene_dto import SceneResponseDTO
from pyhuec.models.protocols.scene_protocol import SceneServiceProtocol


class SceneService(SceneServiceProtocol):
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