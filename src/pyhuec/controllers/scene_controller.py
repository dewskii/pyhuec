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
from pyhuec.models.protocols import SceneControllerProtocol, SceneRepositoryProtocol


class SceneController(SceneControllerProtocol):
    """Scene controller for handling API endpoint requests."""

    def __init__(self, scene_repository: SceneRepositoryProtocol) -> None:
        """
        Initialize scene controller.

        Args:
            scene_repository: Repository for scene data access
        """
        self._scene_repository = scene_repository

    async def handle_get_scene(self, scene_id: str) -> SceneResponseDTO:
        """
        Handle GET /scene/{id} request.

        Args:
            scene_id: UUID of the scene

        Returns:
            Scene details
        """
        return await self._scene_repository.get_scene(scene_id)

    async def handle_get_scenes(self) -> SceneListResponseDTO:
        """
        Handle GET /scene request.

        Returns:
            List of all scenes
        """
        return await self._scene_repository.get_scenes()

    async def handle_create_scene(
        self, create: SceneCreateDTO
    ) -> SceneCreateResponseDTO:
        """
        Handle POST /scene request.

        Args:
            create: Scene creation data

        Returns:
            Creation response with new scene ID
        """
        return await self._scene_repository.create_scene(create)

    async def handle_update_scene(
        self, scene_id: str, update: SceneUpdateDTO
    ) -> SceneUpdateResponseDTO:
        """
        Handle PUT /scene/{id} request.

        Args:
            scene_id: UUID of the scene
            update: Scene update data

        Returns:
            Update response
        """
        return await self._scene_repository.update_scene(scene_id, update)

    async def handle_recall_scene(
        self, scene_id: str, recall: SceneRecallDTO
    ) -> SceneUpdateResponseDTO:
        """
        Handle PUT /scene/{id}/recall request.

        Args:
            scene_id: UUID of the scene
            recall: Scene recall data

        Returns:
            Update response
        """
        return await self._scene_repository.recall_scene(scene_id, recall)

    async def handle_delete_scene(self, scene_id: str) -> SceneDeleteResponseDTO:
        """
        Handle DELETE /scene/{id} request.

        Args:
            scene_id: UUID of the scene

        Returns:
            Deletion response
        """
        return await self._scene_repository.delete_scene(scene_id)
