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
from pyhuec.models.protocols import SceneControllerProtocol


class SceneController(SceneControllerProtocol):
    """Protocol for Scene controller operations (API endpoint handlers)."""

    async def handle_get_scene(self, scene_id: str) -> SceneResponseDTO:
        """Handle GET /scene/{id} request."""
        ...

    async def handle_get_scenes(self) -> SceneListResponseDTO:
        """Handle GET /scene request."""
        ...

    async def handle_create_scene(
        self, create: SceneCreateDTO
    ) -> SceneCreateResponseDTO:
        """Handle POST /scene request."""
        ...

    async def handle_update_scene(
        self, scene_id: str, update: SceneUpdateDTO
    ) -> SceneUpdateResponseDTO:
        """Handle PUT /scene/{id} request."""
        ...

    async def handle_recall_scene(
        self, scene_id: str, recall: SceneRecallDTO
    ) -> SceneUpdateResponseDTO:
        """Handle PUT /scene/{id}/recall request."""
        ...

    async def handle_delete_scene(self, scene_id: str) -> SceneDeleteResponseDTO:
        """Handle DELETE /scene/{id} request."""
        ...
