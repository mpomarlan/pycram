from dataclasses import dataclass
from typing_extensions import List, Optional, Tuple, Callable, Dict
from .enums import JointType, Shape


@dataclass
class Color:
    """
    Dataclass for storing rgba_color as an RGBA value.
    The values are stored as floats between 0 and 1.
    The default rgba_color is white. 'A' stands for the opacity.
    """
    R: float = 1
    G: float = 1
    B: float = 1
    A: float = 1

    @classmethod
    def from_list(cls, color: List[float]):
        """
        Sets the rgba_color from a list of RGBA values.

        :param color: The list of RGBA values
        """
        if len(color) == 3:
            return cls.from_rgb(color)
        elif len(color) == 4:
            return cls.from_rgba(color)
        else:
            raise ValueError("Color list must have 3 or 4 elements")

    @classmethod
    def from_rgb(cls, rgb: List[float]):
        """
        Sets the rgba_color from a list of RGB values.

        :param rgb: The list of RGB values
        """
        return cls(rgb[0], rgb[1], rgb[2], 1)

    @classmethod
    def from_rgba(cls, rgba: List[float]):
        """
        Sets the rgba_color from a list of RGBA values.

        :param rgba: The list of RGBA values
        """
        return cls(rgba[0], rgba[1], rgba[2], rgba[3])

    def get_rgba(self) -> List[float]:
        """
        Returns the rgba_color as a list of RGBA values.

        :return: The rgba_color as a list of RGBA values
        """
        return [self.R, self.G, self.B, self.A]


@dataclass
class Constraint:
    """
    Dataclass for storing a constraint between two objects.
    """
    parent_obj_id: int
    parent_link_name: str
    child_obj_id: int
    child_link_name: str
    joint_type: JointType
    joint_axis_in_child_link_frame: List[int]
    joint_frame_position_wrt_parent_origin: List[float]
    joint_frame_position_wrt_child_origin: List[float]
    joint_frame_orientation_wrt_parent_origin: Optional[List[float]] = None
    joint_frame_orientation_wrt_child_origin: Optional[List[float]] = None


@dataclass
class Point:
    x: float
    y: float
    z: float

    @classmethod
    def from_list(cls, point: List[float]):
        """
        Sets the point from a list of x, y, z values.

        :param point: The list of x, y, z values
        """
        return cls(point[0], point[1], point[2])


@dataclass
class AxisAlignedBoundingBox:
    """
    Dataclass for storing an axis-aligned bounding box.
    """
    min_x: float
    min_y: float
    min_z: float
    max_x: float
    max_y: float
    max_z: float

    @classmethod
    def from_min_max(cls, min_point: List[float], max_point: List[float]):
        """
        Sets the axis-aligned bounding box from a minimum and maximum point.

        :param min_point: The minimum point
        :param max_point: The maximum point
        """
        return cls(min_point[0], min_point[1], min_point[2], max_point[0], max_point[1], max_point[2])

    def get_min_max_points(self) -> Tuple[Point, Point]:
        """
        Returns the axis-aligned bounding box as a tuple of minimum and maximum points.

        :return: The axis-aligned bounding box as a tuple of minimum and maximum points
        """
        return self.get_min_point(), self.get_max_point()

    def get_min_point(self) -> Point:
        """
        Returns the axis-aligned bounding box as a minimum point.

        :return: The axis-aligned bounding box as a minimum point
        """
        return Point(self.min_x, self.min_y, self.min_z)

    def get_max_point(self) -> Point:
        """
        Returns the axis-aligned bounding box as a maximum point.

        :return: The axis-aligned bounding box as a maximum point
        """
        return Point(self.max_x, self.max_y, self.max_z)

    def get_min_max(self) -> Tuple[List[float], List[float]]:
        """
        Returns the axis-aligned bounding box as a tuple of minimum and maximum points.

        :return: The axis-aligned bounding box as a tuple of minimum and maximum points
        """
        return self.get_min(), self.get_max()

    def get_min(self) -> List[float]:
        """
        Returns the minimum point of the axis-aligned bounding box.

        :return: The minimum point of the axis-aligned bounding box
        """
        return [self.min_x, self.min_y, self.min_z]

    def get_max(self) -> List[float]:
        """
        Returns the maximum point of the axis-aligned bounding box.

        :return: The maximum point of the axis-aligned bounding box
        """
        return [self.max_x, self.max_y, self.max_z]


@dataclass
class CollisionCallbacks:
    on_collision_cb: Callable
    no_collision_cb: Optional[Callable] = None


@dataclass
class MultiBody:
    base_visual_shape_index: int
    base_position: List[float]
    base_orientation: List[float]
    link_visual_shape_indices: List[int]
    link_positions: List[List[float]]
    link_orientations: List[List[float]]
    link_masses: List[float]
    link_inertial_frame_positions: List[List[float]]
    link_inertial_frame_orientations: List[List[float]]
    link_parent_indices: List[int]
    link_joint_types: List[JointType]
    link_joint_axis: List[List[float]]
    link_collision_shape_indices: List[int]


@dataclass
class VisualShape:
    rgba_color: Color
    visual_frame_position: List[float]


@dataclass
class BoxVisualShape(VisualShape):
    half_extents: List[float]
    visual_geometry_type: Optional[Shape] = Shape.BOX


@dataclass
class SphereVisualShape(VisualShape):
    radius: float
    visual_geometry_type: Optional[Shape] = Shape.SPHERE


@dataclass
class CapsuleVisualShape(VisualShape):
    radius: float
    length: float
    visual_geometry_type: Optional[Shape] = Shape.CAPSULE


@dataclass
class CylinderVisualShape(CapsuleVisualShape):
    visual_geometry_type: Optional[Shape] = Shape.CYLINDER


@dataclass
class MeshVisualShape(VisualShape):
    mesh_scale: List[float]
    mesh_file_name: str
    visual_geometry_type: Optional[Shape] = Shape.MESH


@dataclass
class PlaneVisualShape(VisualShape):
    normal: List[float]
    visual_geometry_type: Optional[Shape] = Shape.PLANE


@dataclass
class LinkState:
    constraint_ids: Dict['Link', int]


@dataclass
class ObjectState:
    state_id: int
    attachments: Dict['Object', 'Attachment']
