# yaml_2_excel

This is a tool for compiling all config.yaml and kpi.yaml files inside one branch directory into one single Excel (.xlxs) file.

### Directory structure:
The branch directory must have structure like described bellow both the config.yaml and kpi.yaml must exist in each execution folder:
<pre>
/branch_dir
│
├── execution_dir_1
│   ├── config.yaml
│   ├── kpi.yaml
│   └── ...
│
├── execution_dir_2
│   ├── config.yaml
│   ├── kpi.yaml
│   └── ...
│ 
└── ...
</pre>

### Quick start:
Command structute:
```
python hahaha.py -o blabla -a blabla/blabla
```

If either config.yaml or kpi.yaml is missing, the execution directory which contains that file will be ignored.

### Maintenance:
Created by Loc Hoang Nguyen, Research Team, Grid Inc
