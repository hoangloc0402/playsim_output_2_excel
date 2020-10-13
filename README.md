## playsim_output_2_excel

A tool for compiling all config.yaml and kpi.yaml files inside one branch directory into one single Excel (.xlxs) file.

### Directory structure:
The branch directory must have the following structure, both config.yaml & kpi.yaml file must exist in each execution folder:
<pre>
/branch_dir
│
├── execution_dir_1
│   ├── config.yaml
│   ├── kpi.yaml
│   └── ...
├── execution_dir_2
│   ├── config.yaml
│   ├── kpi.yaml
│   └── ...
└── ...
</pre>

### Quick start:
Command:
```
    python compile_yaml.py /home/loc/playsim/master -o /home/loc/output -f filename.xlsx
```
<ul>
  <li> [-o] [--output_path]: path to the output directory. If not specified, the file will be exported to the branch directory.</li>
  <li> [-f] [--file_name]: name for the output excel file. Default name is <strong>'playsim_yaml_compiled.xlsx'</strong>.</li>
</ul>
<br>
If either config.yaml or kpi.yaml is missing, the execution directory which contains that file will be ignored.
<br>
All missing values will be replaced with 'N/A'.

### Maintenance:
Created by Loc Hoang Nguyen, Research Team, Grid Inc
