from repo_types import ScriptConfig
import argparse

parser = argparse.ArgumentParser(prog="anixart patcher repo maker")
parser.add_argument("--input", help="path for `input` dir", default="src")
parser.add_argument("--output", help="path for `output` dir", default="dist")
parser.add_argument("--patches", help="path for `patches` dir", default="patches")
parser.add_argument("--templates", help="path for `templates` dir", default="templates")
args = parser.parse_args()


config = ScriptConfig(
    input_dir=args.input,
    output_dir=args.output,
    patches_dir=args.patches,
    template_dir=args.templates,
)
