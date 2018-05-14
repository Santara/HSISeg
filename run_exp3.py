import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HSISeg.settings")
django.setup()
from semiSuper.PN_semi_cluster_dist_exp import run_PN_on_cluster_dist_sampling, run_PN_on_cluster_sampling, run_PN_on_dist_sampling
from semiSuper.exp_preprocessing import get_preprocessed_data

clust_labelled_img, preprocessed_img, target_mat = get_preprocessed_data()

run_PN_on_cluster_dist_sampling(clust_labelled_img, preprocessed_img, target_mat)

run_PN_on_cluster_sampling(clust_labelled_img, preprocessed_img, target_mat)

run_PN_on_dist_sampling(clust_labelled_img, preprocessed_img, target_mat)