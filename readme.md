## Dataset transformation

Download the full dataset and extract it. Folder structure should become:

```
user@pc:~/lisa-traffic-light-dataset$ tree -d
.
├── Annotations
│   ├── daySequence1
│   ├── daySequence2
│   ├── dayTrain
│   │   ├── dayClip1
│   │   ├── dayClip10
│   │   ├── dayClip11
│   │   ├── dayClip12
│   │   ├── dayClip13
│   │   ├── dayClip2
│   │   ├── dayClip3
│   │   ├── dayClip4
│   │   ├── dayClip5
│   │   ├── dayClip6
│   │   ├── dayClip7
│   │   ├── dayClip8
│   │   └── dayClip9
│   ├── nightSequence1
│   ├── nightSequence2
│   └── nightTrain
│       ├── nightClip1
│       ├── nightClip2
│       ├── nightClip3
│       ├── nightClip4
│       └── nightClip5
├── daySequence1
│   └── frames
├── daySequence2
│   └── frames
├── dayTrain
│   ├── dayClip1
│   │   └── frames
│   ├── dayClip10
│   │   └── frames
│   ├── dayClip11
│   │   └── frames
│   ├── dayClip12
│   │   └── frames
│   ├── dayClip13
│   │   └── frames
│   ├── dayClip2
│   │   └── frames
│   ├── dayClip3
│   │   └── frames
│   ├── dayClip4
│   │   └── frames
│   ├── dayClip5
│   │   └── frames
│   ├── dayClip6
│   │   └── frames
│   ├── dayClip7
│   │   └── frames
│   ├── dayClip8
│   │   └── frames
│   └── dayClip9
│       └── frames
├── nightSequence1
│   └── frames
├── nightSequence2
│   └── frames
├── nightTrain
│   ├── nightClip1
│   │   └── frames
│   ├── nightClip2
│   │   └── frames
│   ├── nightClip3
│   │   └── frames
│   ├── nightClip4
│   │   └── frames
│   └── nightClip5
│       └── frames
├── sample-dayClip6
│   └── frames
└── sample-nightClip1
    └── frames

75 directories
```

chmod +x convert_dataset.sh 
./convert_dataset.sh 