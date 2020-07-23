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

import pickle as pkl
import os
from glob import glob
import numpy as np
from os.path import join, exists, basename
from tqdm import tqdm

class CAPE_utils():
    def __init__(self, mesh_lib='psbody.mesh',
                 dataset_dir=''):
        super().__init__()
        self.dataset_dir = dataset_dir
        self.faces = np.load(join(dataset_dir, 'misc', 'smpl_tris.npy'))
        self.mesh_lib = mesh_lib
     

    def load_single_frame(self, npz_fn):
        '''
        given path to a single data frame, return the contents in the data
        '''
        data = np.load(npz_fn)
        return data['v_cano'], data['v_posed'], data['pose'], data['transl']

    
    def calc_clo_disp(self, v_cano, minimal_cano):
    	# calc disps
        return v_cano - minimal_cano


    def demo(self, subj='00032', seq_name='shortlong_hips'):
        '''
        This demo explains the terms saved in the data and shows
        how to get clothing displacements, with an visualization.
        '''
        from psbody.mesh import Mesh, MeshViewer, MeshViewers
        
        gender = pkl.load(open(join(self.dataset_dir, 'misc', 'subj_genders.pkl'), 'rb'))[subj]
        minimal_fn = join(dataset_dir, 'minimal_body_shape', subj, '{}_minimal.npy'.format(subj))
        minimal_cano = np.load(minimal_fn) # minimal clothed body shape, canonical pose
        
        data_dir = join(dataset_dir, 'sequences', subj, seq_name)
        data_choice = os.listdir(data_dir)[0] # just load 1 data frame for demo
        data_path = join(data_dir, data_choice) 
        print("\n=======================\n")
        print('Visualizing: {}, {}\n'.format(subj, data_choice))
            
        '''
        clo_cano: vertices of clothed, canonical (with pose dependent clo deformation)
        clo_posed: vertices of clothed, posed, translated
        pose_params: 72-dimensional SMPL pose parameter of this frame
        transl: translation of the clothed_posed mesh in the global coordinate
        '''
        clo_cano, clo_posed, pose_params, transl = self.load_single_frame(data_path)

        # compute clothing displacements. This should be done ** in the canonical pose **.
        clo_disps = self.calc_clo_disp(clo_cano, minimal_cano)
        mesh_clothed_colored = Mesh(clo_cano, self.faces)

        # visualize the color-encoded per-vertex clothing displacements
        print("On screen: minimally clothed body in canonical pose VS. clothed body in canonical pose, color encoded by the norm of clothing displacements.")
        print("\n=======================\n")
        vc = np.linalg.norm(clo_disps, axis=-1)
        mesh_clothed_colored.set_vertex_colors_from_weights(vc) 
        mvs = MeshViewers(shape=(1,2), keepalive=True)
        mvs[0][0].static_meshes = [Mesh(minimal_cano, self.faces)]
        mvs[0][1].static_meshes = [mesh_clothed_colored]

    
    def extract_mesh_seq(self, subj, seq_name, option='posed'):
        '''
        extract the vertices from npz files and write the mesh to .obj files
        '''
        mesh_dir = join(self.dataset_dir, 'meshes', subj, seq_name, option)
        os.makedirs(mesh_dir, exist_ok=True)

        seq_dir = join(self.dataset_dir, 'sequences', subj, seq_name)
        seq_flist = glob(join(seq_dir, '*.npz'))

        print('Extracting meshes of {} {} ({})..'.format(subj, seq_name, option))

        for fn in tqdm(seq_flist):
            v_cano, v_posed, pose_params, transl = self.load_single_frame(fn)
            verts = v_posed if option == 'posed' else v_cano

            mesh_frame_name = basename(fn).replace('npz', 'obj')
            
            if self.mesh_lib == 'trimesh':
                import trimesh
                mm = trimesh.Trimesh(verts, self.faces, process=False)
                mm.export(join(mesh_dir, mesh_frame_name))
            elif self.mesh_lib == 'psbody.mesh':
                from psbody.mesh import Mesh
                Mesh(verts, self.faces).write_obj(join(mesh_dir, mesh_frame_name))


    def visualize_sequence(self, subj, seq_name, option='posed'):
        '''
        extracts vertex info from npz files, write to obj, and 
        render seq (front view) into a video to visualize, using ffmpeg
        args:
            subj: subject id, e.g. 00032
            seq_name: sequence name in the format of "garment_motion", e.g. shortlong_punching
            option: 'posed' or 'canonical', whether to visualize the posed meshes or canonical meshes
        '''      
        video_savedir = join(self.dataset_dir, 'visualization', subj)
        os.makedirs(video_savedir, exist_ok=True)
        video_fn = join(video_savedir, '{}_{}.mp4'.format(seq_name, option))
        
        # check if the meshes are already extracted; if not, extract first
        mesh_dir = join(self.dataset_dir, 'meshes', subj, seq_name, option)
        if not exists(mesh_dir):
            self.extract_mesh_seq(subj, seq_name, option)
        elif len(os.listdir(mesh_dir)) == 0:
            self.extract_mesh_seq(subj, seq_name, option)

        # Render a video from the mesh sequence using psbody.mesh package and ffmpeg
        # You can customize and use other tools to do the rendering
        from vis_mesh_seq import render_video
        render_video(mesh_dir, video_fn)
        

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--subj', type=str, help='6-digit subject id, e.g. 00032', default='00032')
    parser.add_argument('--seq_name', type=str, help='sequence name, as found in the second column of seq_list.txt')
    parser.add_argument('--option', type=str, default='posed', choices=['posed', 'canonical'], help='canonical or posed, used to extract the data into meshes')
    parser.add_argument('--dataset_dir', type=str, default='', help='path to CAPE dataset root dir')
    parser.add_argument('--mesh_lib', type=str, choices=['trimesh', 'psbody.mesh'],
                        help='your preferred mesh processing python library, trimesh or psbody.mesh', default='trimesh')
    parser.add_argument('--demo_disps', action='store_true', help='run the demo showing clothing displacements')
    parser.add_argument('--extract', action='store_true', help='extract mesh files from the sequence, and render it into a video')
    parser.add_argument('--vis', action='store_true', help='render the specified sequence into a video; if meshes of the sequences do not exist, will extract it first')

    args = parser.parse_args()

    if args.dataset_dir == '':
        script_dir = os.path.dirname(os.path.realpath(__file__))
        dataset_dir = os.path.dirname(script_dir)
    else:
        dataset_dir = args.dataset_dir

    cape = CAPE_utils(args.mesh_lib, dataset_dir)

    if args.vis:
        cape.visualize_sequence(args.subj, args.seq_name, option=args.option)

    if args.extract:
    	cape.extract_mesh_seq(args.subj, args.seq_name, option=args.option)
    
    if args.demo_disps:
        cape.demo(args.subj, args.seq_name)