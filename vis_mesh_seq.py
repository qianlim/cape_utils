# -*- coding: utf-8 -*-

# Max-Planck-Gesellschaft zur Förderung der Wissenschaften e.V. (MPG) is
# holder of all proprietary rights on this computer program.
# You can only use this computer program if you have closed
# a license agreement with MPG or you get the right to use the computer
# program from someone who is authorized to grant you that right.
# Any use of the computer program without a valid license is prohibited and
# liable to prosecution.
#
# Copyright©2020 Max-Planck-Gesellschaft zur Förderung
# der Wissenschaften e.V. (MPG). acting on behalf of its Max Planck Institute
# for Intelligent Systems. All rights reserved.
#
# Contact: ps-license@tuebingen.mpg.de

def render_video(mesh_dir, video_fn, overwrite=False):
    from psbody.mesh import Mesh, MeshViewer
    from os.path import join, exists, splitext
    from glob import glob
    import tempfile
    from subprocess import call
    from pickle import load
    import numpy as np
    from tqdm import tqdm

    if exists(video_fn):
        if overwrite:
            print("File {0} exists, removing it and remaking it".format(video_fn))
            call(['rm', '-rf', video_fn])
        else:
            print("File {0} exists, not re-rendering".format(video_fn))
            return

    files_seq = sorted(glob(join(mesh_dir, '*.obj')))

    if len(files_seq) == 0:
        print('No files to render in {}'.format(mesh_dir))
        return

    # Load the meshes
    print("Loading meshes from {}..".format(mesh_dir))
    meshes = []
    for fn in files_seq:
        meshes.append(Mesh(filename=fn))

    from shutil import rmtree
    from tempfile import mkdtemp
    tmp_folder = str(mkdtemp())
    if exists(tmp_folder):
        rmtree(tmp_folder)
    from os import mkdir
    mkdir(tmp_folder)

    mv = MeshViewer(window_width=1000, window_height=800)

    print('Rendering extracted meshes (tmp file, auto-removed later)..')
    for k, mesh in enumerate(tqdm(meshes)):
        mv.set_dynamic_meshes([mesh])
        mv.save_snapshot(join(tmp_folder, '{:0>6d}.png'.format(k)), blocking=True)

    cmd = ['ffmpeg', '-i', '{0}/%06d.png'.format(tmp_folder), '-vcodec', 'h264', '-pix_fmt', 'yuv420p', '-r', '15', '-an', '-b:v', '5000k', video_fn]
    call(cmd)
    rmtree(tmp_folder)