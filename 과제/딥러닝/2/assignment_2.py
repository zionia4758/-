import torch.nn as nn
import torch.utils.data
import torchvision.datasets as datasets
import torchvision.transforms as transforms
import numpy as np
from PIL import Image

from tqdm import tqdm

torch.manual_seed(0)
torch.cuda.manual_seed(0)
torch.cuda.manual_seed_all(0)


class Generator(nn.Module):
    def __init__(self, ):
        super(Generator, self).__init__()
        self.main = nn.Sequential(
            nn.ConvTranspose2d(100, 64 * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(64 * 8),
            nn.ReLU(),
            nn.ConvTranspose2d(64 * 8, 64 * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(64 * 4),
            nn.ReLU(),
            nn.ConvTranspose2d(64 * 4, 64 * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(64 * 2),
            nn.ReLU(),
            nn.ConvTranspose2d(64 * 2, 64, 4, 2, 1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 3, 4, 2, 1, bias=False),
            nn.Tanh()
        )

    def forward(self, input):
        # input data는 [batch size, 100, 1, 1]의 형태로 주어야합니다.
        return self.main(input)


class Discriminator(nn.Module):
    # 모델의 코드는 여기서 작성해주세요

    def __init__(self):
        super(Discriminator, self).__init__()
        self.conv1=nn.Conv2d(3,16,5,1,1)
        self.pool=nn.MaxPool2d(2,2)
        self.conv2=nn.Conv2d(16,32,3,1,1)
        self.conv3=nn.Conv2d(32,64,3,1,1)
        #64*7*7
        #32*15*15
        self.fc1=nn.Linear(64*7*7, 16*16)
        self.fc2=nn.Linear(16*16,1)
        self.activation=nn.LeakyReLU(0.2)
        self.sigmoid=nn.Sigmoid()
        self.dropout=nn.Dropout(0.3)


    def forward(self, input):
        x1=self.pool(self.activation(self.conv1(input)))
        x1=self.dropout(x1)
        x2=self.pool(self.activation(self.conv2(x1)))
        x2=self.dropout(x2)
        x3=self.pool(self.activation(self.conv3(x2)))
        x3=self.dropout(x3)
        #print(x3.shape)
        x_flatten=torch.flatten(x3,1)
        #print(x_flatten.shape)
        x4=self.activation(self.fc1(x_flatten))
        x4=self.dropout(x4)
        output=self.sigmoid(self.fc2(x4))


        return output


if __name__ == "__main__":
    # 학습코드는 모두 여기서 작성해주세요


    transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5),(0.5))
        ])



    data_path = 'training_data/'

    dataset = datasets.ImageFolder(root=data_path,
                                   transform=transform
                                   )
    print(torch.cuda.is_available())
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(device)
    if True:
        generator = Generator().to(device)
        discriminator = Discriminator().to(device)
    else:
        generator = Generator()
        discriminator = Discriminator()
        model=torch.load('models/wieght15.pt')
        generator.load_state_dict(model['generator'])
        generator.to(device)
        discriminator.load_state_dict(model['discriminator'])
        discriminator.to(device)

    criterion=torch.nn.BCELoss()
    g_optimizer=torch.optim.Adam(generator.parameters(),lr=0.001,betas=(0.9,0.999))
    d_optimizer=torch.optim.Adam(discriminator.parameters(), lr=0.001,betas=(0.9,0.999))

    epochs=75
    total_batch_num=len(dataset)
    batch_size=64

    train_dataloader=torch.utils.data.DataLoader(dataset,batch_size=batch_size,shuffle=True)
    for epoch in range(epochs):
        print(epoch)
        generator.train()
        discriminator.train()
        avg_g_cost=0
        avg_d_cost=0
        for step,batch in enumerate(train_dataloader):
            if step%(160*5)==0:
                print(str(step*batch_size)+" / "+str(total_batch_num))
            b_x,_=batch
            b_x=b_x.to(device)

            #b_x=b_x.view(3,64,64).to(device)
            num_img=len(b_x)
            real_label=torch.ones((num_img,1)).to(device)
            fake_label=torch.zeros((num_img,1)).to(device)

            real_logit=discriminator(b_x)
            d_real_loss=criterion(real_logit,real_label)    

            z=torch.randn((num_img,100,1,1),requires_grad=False).to(device)

            fake_data=generator(z)
            fake_logit=discriminator(fake_data)
            d_fake_loss=criterion(fake_logit,fake_label)

            d_loss=d_real_loss+d_fake_loss
            d_optimizer.zero_grad()
            d_loss.backward()
            d_optimizer.step()
            
            z=torch.randn((num_img,100,1,1),requires_grad=False).to(device)
            fake_data=generator(z)
            fake_logit=discriminator(fake_data)
            g_loss=criterion(fake_logit,real_label)
            d_optimizer.zero_grad()
            g_optimizer.zero_grad()
            g_loss.backward()
            g_optimizer.step()

            avg_d_cost+=d_loss
            avg_g_cost+=g_loss
        avg_d_cost/=total_batch_num
        avg_g_cost/=total_batch_num
        print(avg_d_cost.item(),avg_g_cost.item())

        if False:
            if epoch%10==0:
                if epoch!=0:
                    print("save model and fake image")
                    torch.save({'generator' : generator.state_dict(),
                    'discriminator': discriminator.state_dict()},'models/wieght'+str(int(epoch)+15)+'.pt')
                    generator.eval()
                    test_noise = torch.randn(3000, 100, 1, 1, device=device)
                    with torch.no_grad():
                        test_fake = generator(test_noise).detach().cpu()

                        for index, img in enumerate(test_fake):
                            fake = np.transpose(img.detach().cpu().numpy(), [1, 2, 0])
                            fake = (fake * 127.5 + 127.5).astype(np.uint8)
                            im = Image.fromarray(fake)
                            im.save("./fake_img{}/fake_sample{}.jpeg".format(int(epoch)+15,index))

    if False:
        torch.save({'generator' : generator.state_dict(),'discriminator': discriminator.state_dict()},'models/wieght15.pt')
    # FID score 측정에 사용할 fake 이미지를 생성하는 코드 입니다.
    # generator의 학습을 완료한 뒤 마지막에 실행하여 fake 이미지를 저장하시기 바랍니다.
    generator.eval()
    test_noise = torch.randn(3000, 100, 1, 1, device=device)
    with torch.no_grad():
        test_fake = generator(test_noise).detach().cpu()

        for index, img in enumerate(test_fake):
            fake = np.transpose(img.detach().cpu().numpy(), [1, 2, 0])
            fake = (fake * 127.5 + 127.5).astype(np.uint8)
            im = Image.fromarray(fake)
            im.save("./fake_img/fake_sample{}.jpeg".format(index))
