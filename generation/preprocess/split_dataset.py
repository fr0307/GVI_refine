import os
import shutil
import random
from pathlib import Path


def split_dataset(source_dir, train_dir, dev_dir, train_ratio=0.8):
    # 确保目标文件夹存在
    for folder in [train_dir, dev_dir]:
        os.makedirs(folder, exist_ok=True)

    # 获取所有 .c 文件
    all_files = list(Path(source_dir).glob("*.c"))

    # 归类文件
    ori_0, ori_1, ref_1 = [], [], []
    for file in all_files:
        filename = file.name
        if filename.startswith("ori"):
            if filename.endswith("_0.c"):
                ori_0.append(file)
            elif filename.endswith("_1.c"):
                ori_1.append(file)
        elif filename.startswith("ref") and filename.endswith("_1.c"):
            ref_1.append(file)

    assert len(ori_0) == len(ori_1) + len(ref_1), "Error: origin data is imbalance"

    # 打乱数据
    random.shuffle(ori_0)
    random.shuffle(ori_1)
    random.shuffle(ref_1)

    # 计算 dev set 大小
    dev_size_per_label = int(len(ori_0) * (1 - train_ratio))

    # 划分 dev set（仅包含 ori 文件）
    dev_files = ori_0[:dev_size_per_label] + ori_1[:dev_size_per_label]

    # 剩下的文件用于 train set
    train_files = ori_0[dev_size_per_label:] + ori_1[dev_size_per_label:] + ref_1

    # 确保 train set 仍然平衡
    assert len([f for f in train_files if f.name.endswith("_0.c")]) == len(
        [f for f in train_files if f.name.endswith("_1.c")]), "Error: training set is imbalance"

    # 复制文件到 dev 目录
    for file in dev_files:
        shutil.copy(file, dev_dir)

    # 复制文件到 train 目录
    for file in train_files:
        shutil.copy(file, train_dir)

    print(f"Dataset split succeed: train_set={len(train_files)}, dev_set={len(dev_files)}")


if __name__ == '__main__':
    source_directory = "./raw_code/devign"
    train_directory = "./raw_code/devign/train"
    dev_directory = "./raw_code/devign/dev"
    split_dataset(source_directory, train_directory, dev_directory)
