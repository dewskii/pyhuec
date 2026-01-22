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
from pyhuec.transport.http_client import HttpClient


class SceneRepository(SceneRepositoryProtocol):
    """Repository for Scene data access operations."""

    def __init__(self, http_client: HttpClient):
        """Initialize the repository with an HTTP client."""
        self._client = http_client

    async def get_scene(self, scene_id: str) -> SceneResponseDTO:
        """
        Retrieve a single scene by ID.

        Args:
            scene_id: UUID of the scene

        Returns:
            SceneResponseDTO with scene details
        """
        response = await self._client.get(f"/clip/v2/resource/scene/{scene_id}")
        return SceneResponseDTO(**response)

    async def get_scenes(self) -> SceneListResponseDTO:
        """
        Retrieve all scenes.

        Returns:
            SceneListResponseDTO with list of all scenes
        """
        response = await self._client.get("/clip/v2/resource/scene")
        return SceneListResponseDTO(**response)

    async def create_scene(self, create: SceneCreateDTO) -> SceneCreateResponseDTO:
        """
        Create a new scene.

        Args:
            create: SceneCreateDTO with scene configuration

        Returns:
            SceneCreateResponseDTO with created scene ID
        """
        response = await self._client.post(
            "/clip/v2/resource/scene",
            data=create.model_dump(exclude_none=True)
        )
        return SceneCreateResponseDTO(**response)

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
        response = await self._client.put(
            f"/clip/v2/resource/scene/{scene_id}",
            data=update.model_dump(exclude_none=True)
        )
        return SceneUpdateResponseDTO(**response)

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
        response = await self._client.put(
            f"/clip/v2/resource/scene/{scene_id}",
            data=recall.model_dump(exclude_none=True)
        )
        return SceneUpdateResponseDTO(**response)

    async def delete_scene(self, scene_id: str) -> SceneDeleteResponseDTO:
        """
        Delete a scene.

        Args:
            scene_id: UUID of the scene

        Returns:
            SceneDeleteResponseDTO with confirmation
        """
        response = await self._client.delete(f"/clip/v2/resource/scene/{scene_id}")
        return SceneDeleteResponseDTO(**response)
