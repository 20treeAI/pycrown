from dagster import op

from pycrown.ops.gcs import download_blob, upload_blob


@op
def run(bucket, chm_name, height_min, outbucket=None, outpoints=None, outsegments=None, return_PC=False):
    from pycrown import PyCrown
    import geopandas as gpd

    chm = chm_name.split('/')[-1]
    download_blob(bucket,chm_name,chm)

    #tree crown can work with CHM, DTM, DSM but here we just use the CHM for everything
    F_CHM = chm
    F_DTM = chm
    F_DSM = chm

    PC = PyCrown(F_CHM, F_DTM, F_DSM, outpath='./')

    PC.filter_chm(5, ws_in_pixels=True, circular=False)
    PC.tree_detection(PC.chm, ws=5, hmin=height_min)

    #crown delineation algorithms: ['dalponte_cython', 'dalponte_numba','dalponteCIRC_numba', 'watershed_skimage']
    PC.crown_delineation(algorithm='dalponteCIRC_numba', th_tree=15.,
                     th_seed=0.7, th_crown=0.55, max_crown=10.)
    print(f"Number of trees detected: {len(PC.trees)}")
    PC.correct_tree_tops()
    PC.get_tree_height_elevation(loc='top')
    PC.get_tree_height_elevation(loc='top_cor')
    PC.screen_small_trees(hmin=height_min, loc='top')
    print(f"Number of trees detected: {len(PC.trees)}")

    #Converts tree crown raster to individual polygons and stores them in the tree dataframe
    #also adds area size per tree
    PC.crowns_to_polys_raster()

    PC.screen_small_trees_area(area_min=2)
    PC.quality_control()
    print(f"Final number of trees detected: {len(PC.trees)}")

    PC.export_tree_locations(loc='top')
    PC.export_tree_locations(loc='top_cor')
    PC.export_tree_crowns(crowntype='crown_poly_raster')

    #we want geojson
    df_crown_poly = gpd.read_file('tree_crown_poly_raster.shp')
    df_crown_top_points = gpd.read_file('tree_location_top_cor.shp')

    if len(outbucket)<1:
        outbucket=None

    if outpoints:
        if outbucket:
            df_crown_top_points.to_file("tree_crown_top.geojson", driver='GeoJSON')
            try:
                print('try upload_blob()')
                upload_blob(outbucket,'tree_crown_top.geojson', outpoints)
            except:
                print('failed. trying direct gpd to gcs')

                print('tree_location_top_cor.shp there?')

                df_crown_top_points = gpd.read_file('tree_location_top_cor.shp')

                df_crown_top_points.to_file(f"gs://{outbucket}/{outpoints}", driver='GeoJSON')
        else:
            df_crown_top_points.to_file(outpoints, driver='GeoJSON')

    if outsegments:
        if outbucket:
            df_crown_poly.to_file("tree_crown_contour.geojson", driver='GeoJSON')
            upload_blob(outbucket,'tree_crown_contour.geojson', outsegments)
        else:
            df_crown_poly.to_file(outsegments, driver='GeoJSON')

    if return_PC:
        return PC