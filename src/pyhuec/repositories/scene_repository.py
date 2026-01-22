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
    """Scene data access."""

    def __init__(self, http_client: HttpClient):
        """Initialize repository.

        Args:
            http_client: HTTP client
        """
        self._client = http_client

    async def get_scene(self, scene_id: str) -> SceneResponseDTO:
        """Get scene by ID.

        Args:
            scene_id: Scene UUID

        Returns:
            Scene details
        """
        response = await self._client.get(f"/clip/v2/resource/scene/{scene_id}")
        return SceneResponseDTO(**response["data"][0])

    async def get_scenes(self) -> SceneListResponseDTO:
        """Get all scenes.

        Returns:
            All scenes
        """
        response = await self._client.get("/clip/v2/resource/scene")
        return SceneListResponseDTO(**response)

    async def create_scene(self, create: SceneCreateDTO) -> SceneCreateResponseDTO:
        """Create scene.

        Args:
            create: Scene configuration

        Returns:
            Created scene ID
        """
        response = await self._client.post(
            "/clip/v2/resource/scene", data=create.model_dump(exclude_none=True)
        )
        return SceneCreateResponseDTO(**response)

    async def update_scene(
        self, scene_id: str, update: SceneUpdateDTO
    ) -> SceneUpdateResponseDTO:
        """Update scene.

        Args:
            scene_id: Scene UUID
            update: Scene update

        Returns:
            Update confirmation
        """
        response = await self._client.put(
            f"/clip/v2/resource/scene/{scene_id}",
            data=update.model_dump(exclude_none=True),
        )
        return SceneUpdateResponseDTO(**response)

    async def recall_scene(
        self, scene_id: str, recall: SceneRecallDTO
    ) -> SceneUpdateResponseDTO:
        """Activate scene.

        Args:
            scene_id: Scene UUID
            recall: Recall parameters

        Returns:
            Update confirmation
        """
        response = await self._client.put(
            f"/clip/v2/resource/scene/{scene_id}",
            data=recall.model_dump(exclude_none=True),
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
