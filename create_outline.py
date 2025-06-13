import sys, os, glob, re

def gather_sources(src_dir):
    paths = glob.glob(os.path.join(src_dir, '*.py'))
    return {p: open(p, 'r').read().splitlines() for p in paths}

def annotate_and_extract(sources):
    fn_re = re.compile(r'^def\s+(\w+)\s*\(')
    names = []
    for lines in sources.values():
        for l in lines:
            m = fn_re.match(l)
            if m: names.append(m.group(1))
    annotated = {}
    for path, lines in sources.items():
        out = []
        for l in lines:
            if not l.strip():
                out.append('')
                continue
            marked = False
            if fn_re.match(l):
                l = '|||PLACEHOLDER|||' + l
                marked = True
            else:
                for n in names:
                    if re.search(r'\b' + re.escape(n) + r'\b', l):
                        l = l + '|||PLACEHOLDER|||'
                        marked = True
                        break
            if marked:
                out.append(l)
        annotated[path] = out
    return annotated

def strip_and_write(annotated, out_path):
    with open(out_path, 'w') as o:
        for p, lines in annotated.items():
            o.write(p + '\n')
            for l in lines:
                o.write(l.replace('|||PLACEHOLDER|||', '') + '\n')
            o.write('\n')

def main():
    src_dir = input("Enter path to folder of .py files: ")
    out_file = "output.txt"
    sources = gather_sources(src_dir)
    annotated = annotate_and_extract(sources)
    strip_and_write(annotated, out_file)
    print("Overview written to", out_file)

if __name__ == '__main__':
    main()

