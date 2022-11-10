import os
from lxml import etree
from tqdm import tqdm
import datetime
import argparse

report = ''

def is_file_xml(path):
    return True if os.path.splitext(path)[1].upper() == '.XML' else False

def get_xml_fp_lst(path):
    global report
    fp_lst = []
    root_dir = ''

    if os.path.isfile(path):
        root_dir = os.path.dirname(path)
        if is_file_xml(path):
            fp_lst.append(path)
    elif os.path.isdir(path):
        root_dir = path
        for root, dirs, files in os.walk(path):
            for file in files:
                fp = os.path.join(root, file)
                if is_file_xml(fp):
                    fp_lst.append(fp)
    else:
        raise ValueError(f'"{path}" is neither file nor folder!')

    if len(fp_lst) == 0:
        raise ValueError(f'No XML file was found.')

    return fp_lst, root_dir

def ts():
    return datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

def ts_us():
    return datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

def format_xml(fp_xml):
    global report
    try:
        tree = etree.parse(fp_xml)
    except etree.XMLSyntaxError as e:
        err_msg = f'{ts()} Error="{e}" on FilePath="{fp_xml}"\n'
        report += err_msg
        return err_msg
    else:
        return etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='utf-8')

def validate_xml(fp_xml):
    global report
    try:
        tree = etree.parse(fp_xml)
    except etree.XMLSyntaxError as e:
        err_msg = f'{ts} Error {e} on File Path {fp_xml}\n'
        report += err_msg

def get_valid_dir(path):
    if os.path.isdir(path):
        return path
    else: 
        raise ValueError(f'"{path}" is not a folder!')

def write_report(dir_out):
    fp_out = os.path.join(dir_out, f'report({ts_us()}).txt')
    global report
    with open(fp_out, 'w') as f:
        f.write(report)

def create_fp_lst_out(root_dir, fp_lst, dir_out):
    fp_lst_out = []
    for fp in fp_lst:
        rel_dir_in = os.path.dirname(fp).replace(root_dir, '').strip("\\")
        abs_dir_out = os.path.join(dir_out, rel_dir_in)
        if not os.path.isdir(abs_dir_out):
            os.makedirs(abs_dir_out)
        fn_out = os.path.basename(fp) + '.txt'
        fp_out = os.path.join(abs_dir_out, fn_out)
        # breakpoint()
        fp_lst_out.append(fp_out)
    return fp_lst_out

def write_bin(fp, contents):
    contents_type = type(contents)
    if contents_type == bytes:
        with open(fp, 'wb') as f:
            f.write(contents)
    elif contents_type == str:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(contents)

def main():
    global report
    report += f'{ts()} Started XML Formatter\n'

    parser = argparse.ArgumentParser(description='Format XML files with file extension .xml')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--format', action='store_true', help='Format XML file')
    group.add_argument('-t', '--test', action='store_true', help='Test if XML file is corrupted')
    parser.add_argument('-i', '--inputpath', metavar='path_src', required=True, help='Input folder or file with xml file(s)')
    parser.add_argument('-o', '--outputdir', metavar='dir_dst', required=False, help='Empty folder to output files')
    args = parser.parse_args()

    fp_lst_in, root_dir = get_xml_fp_lst(args.inputpath)
    print(f'{ts()} len(fp_lst)={len(fp_lst_in)}; root_dir="{root_dir}";')

    dir_out = None if args.outputdir is None else get_valid_dir(args.outputdir)
    print(f'{ts()} dir_out="{dir_out}"')

    # --test
    if args.test:
        for fp_xml in tqdm(fp_lst_in):
            validate_xml(fp_xml)
    # --format
    elif args.format:
        # popultae fp_lst_out
        if dir_out is None:
            fp_lst_out = [fp + ".txt" for fp in fp_lst_in]
        elif os.path.isdir(dir_out):
            fp_lst_out = create_fp_lst_out(root_dir, fp_lst_in, dir_out)
        # write output
        for fp_in, fp_out in tqdm(zip(fp_lst_in, fp_lst_out), total=len(fp_lst_in), ascii=False):
            txt_out = format_xml(fp_in)
            write_bin(fp_out, txt_out)
    else:
        raise ValueError ('No switch was provided...')

    report += f'{ts()} Finished XML Formatter\n'

    if dir_out is None:
        write_report(root_dir)
    elif os.path.isdir(dir_out):
        write_report(dir_out)
    else:
        raise ValueError(f'INVALID dir_out="{dir_out}"')


if __name__ == '__main__':
    main()
