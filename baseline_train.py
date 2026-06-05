import os
import random
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
from sklearn.metrics import classification_report, accuracy_score


SEED = 42
random.seed(SEED)
torch.manual_seed(SEED)


data_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


class GemiDataset(Dataset):
    def __init__(self, base_dir, transform=None):
        self.base_dir = base_dir
        self.transform = transform
        self.image_paths = []
        self.labels = []
        
        
        categories = {'Gemi Var': 1, 'Gemi Yok': 0}
        
        for cat_name, label in categories.items():
            cat_dir = os.path.join(base_dir, cat_name)
            if not os.path.exists(cat_dir):
                continue
            
            for sub_dir in os.listdir(cat_dir):
                sub_dir_path = os.path.join(cat_dir, sub_dir)
                if os.path.isdir(sub_dir_path):
                    for file in os.listdir(sub_dir_path):
                        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                            self.image_paths.append(os.path.join(sub_dir_path, file))
                            self.labels.append(label)

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)
        return image, label


BASE_DIR = "." 
dataset = GemiDataset(base_dir=BASE_DIR, transform=data_transforms)


total_count = len(dataset)
train_count = int(0.7 * total_count)
val_count = int(0.15 * total_count)
test_count = total_count - train_count - val_count

train_set, val_set, test_set = torch.utils.data.random_split(
    dataset, [train_count, val_count, test_count],
    generator=torch.Generator().manual_seed(SEED)
)

train_loader = DataLoader(train_set, batch_size=16, shuffle=True)
test_loader = DataLoader(test_set, batch_size=16, shuffle=False)


class BaselineCNN(nn.Module):
    def __init__(self):
        super(BaselineCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 56 * 56, 64),
            nn.ReLU(),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        return self.classifier(self.features(x))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BaselineCNN().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)


print(f"Veri kümesindeki toplam resim sayısı: {total_count}")
print("Baseline modeli eğitiliyor...")
model.train()
for epoch in range(3):  
    for imgs, lbls in train_loader:
        imgs, lbls = imgs.to(device), lbls.to(device)
        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, lbls)
        loss.backward()
        optimizer.step()


model.eval()
preds, targets = [], []
with torch.no_grad():
    for imgs, lbls in test_loader:
        imgs = imgs.to(device)
        outputs = model(imgs)
        _, predicted = torch.max(outputs, 1)
        preds.extend(predicted.cpu().numpy())
        targets.extend(lbls.numpy())

print("\n=== SPRINT 1 BASELINE METRİKLERİ ===")
print(f"Doğruluk (Accuracy): {accuracy_score(targets, preds):.4f}")
print(classification_report(targets, preds, target_names=['Gemi Yok', 'Gemi Var']))