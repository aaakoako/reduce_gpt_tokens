## reduce_gpt_tokens

This project is aimed at summarizing and converting the code in a specified folder into a format that is readable by GPT while minimizing the number of tokens as much as possible.   

该项目旨在将指定文件夹中的代码总结并转换为GPT可读取的格式，同时尽量减少tokens数量。

### Configuration

The `config.json` file can be modified with the following parameters:

- `dir_path`: the folder path to summarize and compress
- `output_path`: the folder path to store the result file
- `include`: the file extensions to include
- `exclude`: the file extensions to exclude


### 配置

可以使用config.json文件修改以下参数:

- `dir_path`: 需要总结和压缩的文件夹路径
- `output_path`: 输出结果文件夹路径
- `include`: 要包含的文件扩展名
- `exclude`: 要排除的文件扩展名

Example configuration:

示例配置：

```
{
    "dir_path": "./",
    "output_path": "./",
    "include": [".py", ".java", ".cpp", ".go", ".lua", ".c", ".xml", ".js", ".html", ".css"],
    "exclude": [".pyc", ".class"]
}
```
### Usage

To use this project, first modify the `config.json` file with the desired configuration, and then run the `conclude.py` file. The output file will be generated in the specified `output_path` folder.  

### 用法


使用该项目，首先修改config.json文件中的配置参数，然后运行conclude.py文件。输出文件将生成在指定的output_path文件夹中。


### Note


Before using this project, make sure that you have installed Python environment and the required Python libraries.


### 注意事项


在使用之前确保安装好了python环境和使用到的python库
