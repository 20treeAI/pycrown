from dagster import Enum, EnumValue, Field, resource, Noneable, make_values_resource


values_resource = make_values_resource(
    bucket=Field(
        str,
        is_required=True,
        description="The bucket the input data is stored in.",
    ),
    chm_name=Field(
        str,
        is_required=True,
        description="The relative path inside of the bucket to the CHM.",
    ),
    height_min=Field(
        float,
        default_value=15.,
        description="The minimum height of what can be considered a tree, anything below this is filtered out.",
    ),
    outbucket=Field(
        str,
        is_required=True,
        description="The bucket to output the tree top points and/or canopy segmentation into.",
    ),
    outpoints=Field(
        str,
        is_required=True,
        description="Relative path to save the tree top points to in the outbucket.",
    ),
    outsegments=Field(
        str,
        is_required=True,
        description="Relative path to save the tree canopy segmentation to in the outbucket.",
    ),
    return_PC=Field(
        bool,
        default_value=False,
        description="If True, returns the PyCrown object.",
    ),
    dsm_name=Field(
        Noneable(str),
        default_value=None,
        description="The relative path inside of the bucket to the DSM, optional.",
    ),
    dtm_name=Field(
        Noneable(str),
        default_value=None,
        description="The relative path inside of the bucket to the DTM, optional.",
    ),
    point_cloud_name=Field(
        Noneable(str),
        default_value=None,
        description="The relative path inside of the bucket to the point cloud, optional.",
    ),
    median_filter_size=Field(
        int,
        default_value=5,
        description="The size of the median filter, a smaller number may allow more trees to be "
                    "picked up at the cost of more false positives. Default=5.",
    ),
    tree_detection_window_size=Field(
        int,
        default_value=5,
        description="The size of the window used to detect trees. Default=5.",
    ),
    algorithm=Field(
        Enum(
            "algorithm",
            [
                EnumValue("dalponte_cython"),
                EnumValue("dalponte_numba"),
                EnumValue("dalponteCIRC_numba"),
                EnumValue("watershed_skimage"),
                EnumValue("hirschmuller08_laplacian")
            ],
        ),
        default_value="dalponte_numba",
        description="The crown delineation algorithm to use. Choose from: "
                    "['dalponte_cython', 'dalponte_numba', 'dalponteCIRC_numba', 'watershed_skimage']",
    ),
    th_crown=Field(
        float,
        default_value=0.55,
<<<<<<< HEAD
        description="Factor 2 for the minimum height of the tree crown. Default=0.55",
=======
        description="The size of the window used to detect trees. Default=0.55",
>>>>>>> added required fixes for Dagster to work locally with PyCrown
    ),
    th_seed=Field(
        float,
        default_value=0.7,
<<<<<<< HEAD
        description="Factor 1 for the minimum height of the tree crown. Default=0.7",
=======
        description="The size of the window used to detect trees. Default=0.7",
>>>>>>> added required fixes for Dagster to work locally with PyCrown
    ),
    area_min=Field(
        int,
        default_value=2,
        description="The size of the smallest tree in pixels. Default=2.",
    ),
    max_crown=Field(
        float,
        default_value=10.,
<<<<<<< HEAD
        description="The minimum area of what can be considered a tree, anything below this is filtered out, in pixels."
                    " Default=10.",
=======
        description="The maximum size of a tree crown, in pixels.",
>>>>>>> added required fixes for Dagster to work locally with PyCrown
    ),
)
def pycrown_parameters(init_context):
    return dict(init_context.resource_config)