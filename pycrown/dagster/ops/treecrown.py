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
>>>>>>> added required fixes for Dagster to work locally with PyCrown

    chm = context.resources.inputs["chm_name"].split('/')[-1]
    download_blob(context.resources.inputs["bucket"], context.resources.inputs["chm_name"],chm)

    # Use DTM, DSM and LAS in processing if provided, otherwise use the CHM for all.
    F_CHM = chm

    # Set DSM to CHM if not provided, otherwise we can use DSM for a better result.
    if context.resources.inputs["dsm_name"] is not None:
        dsm = context.resources.inputs["dsm_name"].split('/')[-1]
        download_blob(context.resources.inputs["bucket"], context.resources.inputs["dsm_name"], dsm)
        F_DSM = dsm
    else:
        F_DSM = chm

    # Set DTM to CHM if not provided, otherwise we can use DTM for a better result.
    if context.resources.inputs["dtm_name"] is not None:
        dtm = context.resources.inputs["dtm_name"].split('/')[-1]
        download_blob(context.resources.inputs["bucket"], context.resources.inputs["dtm_name"], dtm)
        F_DTM = dtm
    else:
        F_DTM = chm

    # Load .las file if provided.
    if context.resources.inputs["point_cloud_name"] is not None:
        las = context.resources.inputs["point_cloud_name"].split('/')[-1]
        download_blob(context.resources.inputs["bucket"], context.resources.inputs["point_cloud_name"], las)
        F_LAS = las
    else:
        F_LAS = None

    PC = PyCrown(F_CHM, F_DTM, F_DSM, las_file=F_LAS, outpath='./')

    PC.filter_chm(context.resources.inputs["median_filter_size"], ws_in_pixels=True, circular=False)
    PC.tree_detection(PC.chm, ws=context.resources.inputs["tree_detection_window_size"],
                      hmin=context.resources.inputs["height_min"])
    PC.clip_trees_to_bbox(inbuf=5)
    #crown delineation algorithms: ['dalponte_cython', 'dalponte_numba','dalponteCIRC_numba', 'watershed_skimage']
    PC.crown_delineation(algorithm=context.resources.inputs["algorithm"], th_tree=context.resources.inputs["height_min"],
                     th_seed=context.resources.inputs["th_seed"], th_crown=context.resources.inputs["th_crown"],
                         max_crown=context.resources.inputs["max_crown"])
    print(f"Number of trees detected: {len(PC.trees)}")

<<<<<<< HEAD
=======
    # if context.resources.inputs["point_cloud_name"] is not None:
>>>>>>> added required fixes for Dagster to work locally with PyCrown
    PC.correct_tree_tops()

    PC.get_tree_height_elevation(loc='top')
    PC.get_tree_height_elevation(loc='top_cor')
    PC.screen_small_trees(hmin=context.resources.inputs["height_min"], loc='top')
    print(f"Number of trees detected: {len(PC.trees)}")

    #Converts tree crown raster to individual polygons and stores them in the tree dataframe
    #also adds area size per tree
    PC.crowns_to_polys_raster()

    if context.resources.inputs["point_cloud_name"] is not None:
        PC.crowns_to_polys_smooth(store_las=True)

    PC.screen_small_trees_area(area_min=context.resources.inputs["area_min"])
    PC.quality_control()
    print(f"Final number of trees detected: {len(PC.trees)}")

    PC.export_tree_locations(loc='top')
    PC.export_tree_locations(loc='top_cor')
    PC.export_tree_crowns(crowntype='crown_poly_raster')

    if context.resources.inputs["point_cloud_name"] is not None:
        PC.export_tree_crowns(crowntype='crown_poly_smooth')

<<<<<<< HEAD
    # TODO: we want geojson
=======
    #we want geojson
>>>>>>> added required fixes for Dagster to work locally with PyCrown
    df_crown_poly = gpd.read_file('tree_crown_poly_raster.shp')
    df_crown_top_points = gpd.read_file('tree_location_top_cor.shp')

    if len(context.resources.inputs["outbucket"])<1:
        context.resources.inputs["outbucket"]=None

    if context.resources.inputs["outpoints"]:
        if context.resources.inputs["outbucket"]:
            df_crown_top_points.to_file("tree_crown_top.geojson", driver='GeoJSON')
            try:
                print('try upload_blob()')
                upload_blob(context.resources.inputs["outbucket"],'tree_crown_top.geojson', context.resources.inputs["outpoints"])
            except:
                print('failed. trying direct gpd to gcs')

                print('tree_location_top_cor.shp there?')

                df_crown_top_points = gpd.read_file('tree_location_top_cor.shp')

                df_crown_top_points.to_file(f'gs://{context.resources.inputs["outbucket"]}/{context.resources.inputs["outpoints"]}',
                                            driver='GeoJSON')
        else:
            df_crown_top_points.to_file(context.resources.inputs["outpoints"], driver='GeoJSON')

    if context.resources.inputs["outsegments"]:
        if context.resources.inputs["outbucket"]:
            df_crown_poly.to_file("tree_crown_contour.geojson", driver='GeoJSON')
            upload_blob(context.resources.inputs["outbucket"],'tree_crown_contour.geojson', context.resources.inputs["outsegments"])
        else:
            df_crown_poly.to_file(context.resources.inputs["outsegments"], driver='GeoJSON')

    if context.resources.inputs["return_PC"]:
        return PC