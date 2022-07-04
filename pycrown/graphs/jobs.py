from dagster import graph

from pycrown.ops import treecrown

# parameters:
# - name: bucket
# value: "overstory-customer-test"
# - name: chmpath
# value: "treecrown-test/20200917_skysat_werthenstein_clipped_chm.tif"
# - name: chmout
# value: "20200917_skysat_werthenstein_clipped_chm.tif"
# - name: height_min
# value: "16"
# - name: outbucket
# value: "overstory-customer-test"
# - name: outpath_points
# value: "treecrown-test/20200917_skysat_werthenstein_chm_tree_points.geojson"
# - name: outpath_segments
# value: "treecrown-test/20200917_skysat_werthenstein_chm_tree_contours.geojson"


@graph
def pycown_run(bucket, chmpath, chmout, height_min, outbucket, outpath_points, outpath_segments, dsm_name,
               dtm_name, point_cloud_name):

    treecrown.download_blob(bucket, chmpath, chmout)
    treecrown.run(chmout, height_min, outbucket, outpath_points, outpath_segments, dsm_name, dtm_name, point_cloud_name)



pycrown_run_job = pycown_run.to_job()