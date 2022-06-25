import os
import torch

from pytorch_fid.fid_score import *

os.environ['KMP_DUPLICATE_LIB_OK']='True'

real_img_path = 'training_data/celeba/'
fake_img_path = 'fake_img/'

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

torch.manual_seed(0)
torch.cuda.manual_seed(0)
torch.cuda.manual_seed_all(0)

if __name__ == "__main__":
    fid = calculate_fid_given_paths(
        paths=[real_img_path, fake_img_path],
        batch_size=128,
        device=device,
        dims=2048
    )

    print("fid score : {}".format(fid))
