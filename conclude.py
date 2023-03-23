import os
import json
import chardet
import pygments
import regex as re
from pygments.util import ClassNotFound
from pygments.lexers import get_lexer_for_filename

def extract_content(file_path):
    """从文件中提取代码内容"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 获取文件类型
    file_type = os.path.splitext(file_path)[1]

    # 移除注释和打印函数
    content = remove_comments(content, file_type)

    return content

def extract_files(dir_path, config):
    """从目录中提取所有符合条件的代码文件"""

    # 获取目录下所有文件和子目录
    all_files = os.listdir(dir_path)

    file_contents = []

    for file in all_files:
        file_path = os.path.join(dir_path, file)

        # 如果是目录，则递归提取其中的代码文件
        if os.path.isdir(file_path):
            file_contents += extract_files(file_path, config)
        else:
            # 如果是代码文件，则提取其中的代码内容
            file_type = os.path.splitext(file_path)[1]
            if file_type in config['file_types']:
                content = extract_content(file_path)
                file_contents.append(content)

    return file_contents

def remove_comments(content, file_type):
    """移除代码文件中的注释和打印函数"""

    # 定义支持的编程语言及其对应的注释符号和打印函数
    language_dict = {
        'text/x-python': {
            'single_comment': '#',
            'multi_comment_start': '"""',
            'multi_comment_end': '"""',
            'print_func': 'print('
        },
        'text/x-java': {
            'single_comment': '//',
            'multi_comment_start': '/*',
            'multi_comment_end': '*/',
            'print_func': 'System.out.print('
        },
        'text/x-c++src': {
            'single_comment': '//',
            'multi_comment_start': '/*',
            'multi_comment_end': '*/',
            'print_func': 'cout << '
        },
        'text/x-gosrc': {
            'single_comment': '//',
            'multi_comment_start': '/*',
            'multi_comment_end': '*/',
            'print_func': 'fmt.Print('
        },
        'text/x-lua': {
            'single_comment': '--',
            'multi_comment_start': '--[[',
            'multi_comment_end': ']]',
            'print_func': 'print('
        },
        'text/x-csrc': {
            'single_comment': '//',
            'multi_comment_start': '/*',
            'multi_comment_end': '*/',
            'print_func': 'printf('
        },
        'application/xml': {
            'single_comment': None,
            'multi_comment_start': '<!--',
            'multi_comment_end': '-->',
            'print_func': None
        },
        'text/javascript': {
            'single_comment': '//',
            'multi_comment_start': '\/\*',
            'multi_comment_end': '\*\/',
            'print_func': 'console.log('
        },
        'text/html': {
            'single_comment': None,
            'multi_comment_start': '<!--',
            'multi_comment_end': '-->',
            'print_func': None
        },
        'text/css': {
            'single_comment': None,
            'multi_comment_start': '\/\*',
            'multi_comment_end': '\*\/',
            'print_func': None
        },
        'text/x-php': {
            'single_comment': '//',
            'multi_comment_start': '\/\*',
            'multi_comment_end': '\*\/',
            'print_func': 'echo '
        },
        'text/x-perl': {
            'single_comment': '#',
            'multi_comment_start': '=pod',
            'multi_comment_end': '=cut',
            'print_func': 'print '
        },
        'application/json': {
            'single_comment': None,
            'multi_comment_start': None,
            'multi_comment_end': None,
            'print_func': None
        }
    }

    # 获取该编程语言的注释符号和打印函数
    single_comment = language_dict[file_type]['single_comment']
    multi_comment_start = language_dict[file_type]['multi_comment_start']
    multi_comment_end = language_dict[file_type]['multi_comment_end']
    print_func = language_dict[file_type]['print_func']

    # 移除单行注释、多行注释和文档注释
    if single_comment:
        content = re.sub(fr'{single_comment}.*$', '', content, flags=re.MULTILINE)
    if multi_comment_start and multi_comment_end:
        content = re.sub(fr'{re.escape(multi_comment_start)}[\s\S]+?{re.escape(multi_comment_end)}', '', content)
    if multi_comment_start and not multi_comment_end:
        content = re.sub(fr'{re.escape(multi_comment_start)}.*$', '', content, flags=re.MULTILINE)

    # 移除打印函数
    if print_func:
        content = re.sub(fr'{re.escape(print_func)}.*?(?=\))\)', '', content)

    return content



def extract_content(path):
    """提取指定路径下的文件内容"""
    with open(path, 'rb') as f:
        content = f.read()
        encoding = chardet.detect(content)['encoding']
    with open(path, 'r', encoding=encoding or 'utf-8', errors='ignore') as f:
        content = f.read()
    # 获取文件类型，用于移除注释和打印函数
    file_type = get_lexer_for_filename(path).mimetypes[0]
    if file_type is None or file_type.split('/')[0] not in ['text', 'application'] or file_type.split('/')[-1] in ['md', 'markdown']:
        # 排除掉非主流编程语言文件和Markdown文件以及其他非文本文件
        return None
    if file_type in ['text/html', 'text/css', 'application/xml']:
        # 对于HTML、CSS和XML等语言，保留缩进符和换行符
        content = remove_comments(content, file_type)
    else:
        # 对于其他语言，移除缩进符和换行符，并精简字符
        content = remove_comments(content, file_type)
        content = content.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        # 移除emoji等非标准文本
        content = re.sub(r'\p{So}|\p{Cf}|\p{Cs}|\p{Cn}', '', content)
    return content


def extract_files(dir_path, config):
    """提取指定目录下的所有代码文件"""
    file_contents = []
    for root, dirs, files in os.walk(dir_path):
        # 过滤掉隐藏文件夹和文件
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        if config['exclude']:
            # 排除指定后缀的文件
            files = [f for f in files if not f.startswith('.') and f != 'conclude.py' and not f.endswith(tuple(config['exclude']))]
        if config['include']:
            # 只包含指定后缀的文件
            files = [f for f in files if not f.startswith('.') and f != 'conclude.py' and f.endswith(tuple(config['include']))]
        for file in files:
            try:
                lexer = get_lexer_for_filename(file, stripall=True)
            except ClassNotFound:
                continue
            path = os.path.join(root, file)
            content = extract_content(path)
            if content is None:
                # 如果返回的内容为空，则跳过
                continue
            rel_path = os.path.relpath(path, start=dir_path)
            file_contents.append({
                'f': file,
                'p': rel_path,
                'c': content
            })
    return file_contents


if __name__ == '__main__':
    # 获取脚本所在目录的路径
    dir_path = os.path.dirname(os.path.abspath(__file__))

    # 如果已存在conclude.json和conclude_readable.json文件，则先删除
    json_file = os.path.join(dir_path, 'conclude.json')
    if os.path.exists(json_file):
        os.remove(json_file)
    readable_file = os.path.join(dir_path, 'conclude_readable.json')
    if os.path.exists(readable_file):
        os.remove(readable_file)

    # 读取配置文件
    config_file = os.path.join(dir_path, 'config.json')
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 提取文件内容
    file_contents = extract_files(dir_path, config)

    # 将结果储存在JSON文件中，带缩进和换行的conclude_readable.json
    with open(readable_file, 'w', encoding='utf-8') as f:
        json.dump(file_contents, f, ensure_ascii=False, indent=4)

    # 将结果储存在JSON文件中，不带缩进和换行的conclude.json
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(file_contents, f, ensure_ascii=False, separators=(',', ':'))

    print('Done!')