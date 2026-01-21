from pyhuec.models.dto.scene_dto import (
    SceneCreateDTO,
    SceneCreateResponseDTO,
    SceneDeleteResponseDTO,
    SceneListResponseDTO,
    SceneRecallDTO,
    SceneResponseDTO,
    SceneUpdateDTO,
    SceneUpdateResponseDTO,
)
from pyhuec.models.protocols import SceneRepositoryProtocol


class SceneRepository(SceneRepositoryProtocol):
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
        self, scene_id: str, update: SceneUpdateDTO
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
        self, scene_id: str, recall: SceneRecallDTO
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
