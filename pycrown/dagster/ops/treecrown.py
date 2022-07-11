<<<<<<< HEAD
import geopandas as gpd
from dagster import op

from pycrown import PyCrown
=======
from dagster import op

>>>>>>> added required fixes for Dagster to work locally with PyCrown
from pycrown.dagster.ops.gcs import download_blob, upload_blob


@op(required_resource_keys={
    "inputs"
})
def run(context):
<<<<<<< HEAD
=======
    from pycrown import PyCrown
    import geopandas as gpd
<<<<<<< HEAD
>>>>>>> added required fixes for Dagster to work locally with PyCrown

    chm = context.resources.inputs["chm_name"].split('/')[-1]
    download_blob(context.resources.inputs["bucket"], context.resources.inputs["chm_name"],chm)
=======
    inputs = context.resources.inputs
    chm = inputs["chm_name"].split('/')[-1]
    download_blob(inputs["bucket"], inputs["chm_name"],chm)
>>>>>>> WIP - parking code for review

    # Use DTM, DSM and LAS in processing if provided, otherwise use the CHM for all.
    F_CHM = chm

    # Set DSM to CHM if not provided, otherwise we can use DSM for a better result.
    if inputs["dsm_name"] is not None:
        dsm = inputs["dsm_name"].split('/')[-1]
        download_blob(inputs["bucket"], inputs["dsm_name"], dsm)
        F_DSM = dsm
    else:
        F_DSM = chm

    # Set DTM to CHM if not provided, otherwise we can use DTM for a better result.
    if inputs["dtm_name"] is not None:
        dtm = inputs["dtm_name"].split('/')[-1]
        download_blob(inputs["bucket"], inputs["dtm_name"], dtm)
        F_DTM = dtm
    else:
        F_DTM = chm

    # Load .las file if provided.
    if inputs["point_cloud_name"] is not None:
        las = inputs["point_cloud_name"].split('/')[-1]
        download_blob(inputs["bucket"], inputs["point_cloud_name"], las)
        F_LAS = las
    else:
        F_LAS = None

    PC = PyCrown(F_CHM, F_DTM, F_DSM, las_file=F_LAS, outpath='./')

    PC.filter_chm(int(inputs["median_filter_size"]), circular=False, ws_in_pixels=True)
    print(inputs["tree_detection_window_size"])
    PC.tree_detection(PC.chm, ws=inputs["tree_detection_window_size"], ws_in_pixels=True,
                      hmin=inputs["height_min"])
    PC.clip_trees_to_bbox(inbuf=5)
    #crown delineation algorithms: ['dalponte_cython', 'dalponte_numba','dalponteCIRC_numba', 'watershed_skimage']
    PC.crown_delineation(algorithm=inputs["algorithm"], th_tree=inputs["height_min"],
                     th_seed=inputs["th_seed"], th_crown=inputs["th_crown"],
                         max_crown=inputs["max_crown"])
    print(f"Number of trees detected: {len(PC.trees)}")

<<<<<<< HEAD
<<<<<<< HEAD
=======
    # if context.resources.inputs["point_cloud_name"] is not None:
>>>>>>> added required fixes for Dagster to work locally with PyCrown
=======
>>>>>>> WIP - parking code for review
    PC.correct_tree_tops()
    PC.get_tree_height_elevation(loc='top')
    PC.get_tree_height_elevation(loc='top_cor')
    PC.screen_small_trees(hmin=inputs["height_min"], loc='top')
    print(f"Number of trees detected: {len(PC.trees)}")

    # Converts tree crown raster to individual polygons and stores them in the tree dataframe.
    # Also adds area size per tree.
    PC.crowns_to_polys_raster()

    if inputs["point_cloud_name"] is not None:
        PC.crowns_to_polys_smooth(store_las=True, thin_perc=0.5, first_return=False)

    # Remove trees whose area is below area_min.
    PC.screen_small_trees_area(area_min=inputs["area_min"])
    PC.quality_control()
    print(f"Final number of trees detected: {len(PC.trees)}")

    PC.export_tree_locations(loc='top')
    PC.export_tree_locations(loc='top_cor')
    PC.export_tree_crowns(crowntype='crown_poly_raster')

    if inputs["point_cloud_name"] is not None:
        PC.export_tree_crowns(crowntype='crown_poly_smooth')

<<<<<<< HEAD
<<<<<<< HEAD
    # TODO: we want geojson
=======
    #we want geojson
>>>>>>> added required fixes for Dagster to work locally with PyCrown
=======
    # Convert shapes created by export_tree_crowns and locations to GeoJSONs.
>>>>>>> WIP - parking code for review
    df_crown_poly = gpd.read_file('tree_crown_poly_raster.shp')
    df_crown_top_points = gpd.read_file('tree_location_top_cor.shp')

    if len(inputs["outbucket"])<1:
        inputs["outbucket"]=None

    # Upload to GCS.
    if inputs["outpoints"]:
        if inputs["outbucket"]:
            df_crown_top_points.to_file("tree_crown_top.geojson", driver='GeoJSON')
            try:
                print('try upload_blob()')
                upload_blob(inputs["outbucket"],'tree_crown_top.geojson', inputs["outpoints"])
            except:
                print('failed. trying direct gpd to gcs')

                print('tree_location_top_cor.shp there?')

                df_crown_top_points = gpd.read_file('tree_location_top_cor.shp')

                df_crown_top_points.to_file(f'gs://{inputs["outbucket"]}/{inputs["outpoints"]}',
                                            driver='GeoJSON')
        else:
            df_crown_top_points.to_file(inputs["outpoints"], driver='GeoJSON')

    if inputs["outsegments"]:
        if inputs["outbucket"]:
            df_crown_poly.to_file("tree_crown_contour.geojson", driver='GeoJSON')
            upload_blob(inputs["outbucket"],'tree_crown_contour.geojson', inputs["outsegments"])
        else:
            df_crown_poly.to_file(inputs["outsegments"], driver='GeoJSON')

    if inputs["return_PC"]:
        return PC